"""Smoke + correctness tests for the Plotly Bloch rendering layer.

We don't render to pixels in CI; we assert the figures are well-formed
(non-empty, finite data) and that the state→color mapping is right.
"""
from __future__ import annotations

import math

import numpy as np
import plotly.graph_objects as go
import pytest

import bloch_viz


def _all_finite(fig: go.Figure) -> bool:
    for trace in fig.data:
        for attr in ("x", "y", "z", "u", "v", "w"):
            vals = getattr(trace, attr, None)
            if vals is None:
                continue
            arr = np.array([v for v in vals if isinstance(v, (int, float))], dtype=float)
            if arr.size and not np.all(np.isfinite(arr)):
                return False
    return True


class TestBlochFigure:
    def test_returns_nonempty_figure(self):
        fig = bloch_viz.bloch_figure((1.0, 0.0, 0.0), label="q0")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        assert _all_finite(fig)

    def test_zero_vector_has_no_arrowhead(self):
        # Fully mixed state at the origin: a Cone with a zero direction is invalid,
        # so it must be skipped.
        fig = bloch_viz.bloch_figure((0.0, 0.0, 0.0), label="q0")
        assert not any(isinstance(tr, go.Cone) for tr in fig.data)
        assert _all_finite(fig)

    @pytest.mark.parametrize("z,expected", [(1.0, bloch_viz._BLUE), (-1.0, bloch_viz._RED)])
    def test_collapsed_color(self, z, expected):
        assert bloch_viz.vector_color((0.0, 0.0, z), collapsed=True) == expected

    def test_superposition_is_indigo(self):
        assert bloch_viz.vector_color((1.0, 0.0, 0.0), collapsed=False) == bloch_viz._INDIGO


class TestCollapseAnimation:
    def _shaft_color(self, fig):
        for d in fig.data:
            if isinstance(d, go.Scatter3d) and d.mode == "lines" and d.line.width == 8:
                return d.line.color
        return None

    def test_has_frames_and_lands_on_pole(self):
        fig = bloch_viz.collapse_animation((1.0, 0.0, 0.0), (0.0, 0.0, -1.0), label="q0")
        assert isinstance(fig, go.Figure)
        assert len(fig.frames) >= 2
        assert _all_finite(fig)
        last_line = next(d for d in fig.frames[-1].data if isinstance(d, go.Scatter3d))
        assert float(last_line.z[-1]) < -0.9  # ends near the south pole

    @pytest.mark.parametrize("after,expected", [((0, 0, 1), bloch_viz._BLUE), ((0, 0, -1), bloch_viz._RED)])
    def test_color_matches_target_pole(self, after, expected):
        fig = bloch_viz.collapse_animation((1.0, 0.0, 0.0), after)
        assert self._shaft_color(fig) == expected

    def test_has_play_button(self):
        fig = bloch_viz.collapse_animation((1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
        assert fig.layout.updatemenus  # a ▶ button exists


class TestProbabilityBar:
    def test_stacks_to_one(self):
        fig = bloch_viz.probability_bar(0.3)
        assert isinstance(fig, go.Figure)
        widths = [float(tr.x[0]) for tr in fig.data if isinstance(tr, go.Bar)]
        assert math.isclose(sum(widths), 1.0, abs_tol=1e-9)

    @pytest.mark.parametrize("p1", [-0.5, 0.0, 0.5, 1.0, 1.5])
    def test_clamps_probability(self, p1):
        fig = bloch_viz.probability_bar(p1)
        widths = [float(tr.x[0]) for tr in fig.data if isinstance(tr, go.Bar)]
        assert all(0.0 <= w <= 1.0 for w in widths)
        assert math.isclose(sum(widths), 1.0, abs_tol=1e-9)
