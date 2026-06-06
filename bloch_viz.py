"""Interactive Bloch-sphere rendering for the Quantum Lab (Plotly).

Kept separate from :mod:`q_state` (pure math) so the heavy visualization library
stays out of the data layer. Each function returns a ``plotly.graph_objects.Figure``
the Streamlit page drops in with ``st.plotly_chart``.

Color language used across the app:
- **superposition / undecided** → indigo
- **collapsed to |0⟩** → blue
- **collapsed to |1⟩** → red
- a **shrunken** vector (|r| < 1) signals an entangled (mixed) qubit
"""
from __future__ import annotations

import math

import numpy as np
import plotly.graph_objects as go

Vec3 = tuple[float, float, float]

_INDIGO = "#6366F1"
_BLUE = "#2563EB"
_RED = "#DC2626"
_GRID = "#CBD5E1"
_AXIS = "#94A3B8"

# Shared 3D scene so every Bloch figure looks identical and stays oriented.
_SCENE = {
    "xaxis": {"visible": False, "range": [-1.25, 1.25]},
    "yaxis": {"visible": False, "range": [-1.25, 1.25]},
    "zaxis": {"visible": False, "range": [-1.25, 1.25]},
    "aspectmode": "cube",
    "camera": {"eye": {"x": 1.45, "y": 1.45, "z": 0.85}},
    "dragmode": "orbit",
}


def vector_color(vec: Vec3, *, collapsed: bool = False) -> str:
    """Pick the vector color from its state."""
    if collapsed:
        return _BLUE if vec[2] >= 0 else _RED
    return _INDIGO


def _sphere_surface() -> go.Surface:
    u = np.linspace(0, 2 * np.pi, 36)
    v = np.linspace(0, np.pi, 24)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))
    return go.Surface(
        x=x,
        y=y,
        z=z,
        opacity=0.12,
        showscale=False,
        colorscale=[[0, _GRID], [1, _GRID]],
        hoverinfo="skip",
        contours={"x": {"highlight": False}, "y": {"highlight": False}, "z": {"highlight": False}},
        lighting={"ambient": 1.0, "diffuse": 0.0, "specular": 0.0},
    )


def _circle(plane: str) -> go.Scatter3d:
    t = np.linspace(0, 2 * np.pi, 72)
    zeros = np.zeros_like(t)
    if plane == "xy":
        x, y, z = np.cos(t), np.sin(t), zeros
    elif plane == "xz":
        x, y, z = np.cos(t), zeros, np.sin(t)
    else:  # yz
        x, y, z = zeros, np.cos(t), np.sin(t)
    return go.Scatter3d(
        x=x, y=y, z=z, mode="lines",
        line={"color": _GRID, "width": 2},
        hoverinfo="skip", showlegend=False,
    )


def _axes() -> list[go.Scatter3d]:
    out = []
    for ax in ("x", "y", "z"):
        a = {"x": (1.0, 0, 0), "y": (0, 1.0, 0), "z": (0, 0, 1.0)}[ax]
        out.append(
            go.Scatter3d(
                x=[-a[0], a[0]], y=[-a[1], a[1]], z=[-a[2], a[2]],
                mode="lines", line={"color": _AXIS, "width": 2, "dash": "dot"},
                hoverinfo="skip", showlegend=False,
            )
        )
    return out


def _pole_labels() -> go.Scatter3d:
    return go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[1.18, -1.18],
        mode="text", text=["|0⟩", "|1⟩"],
        textfont={"size": 13, "color": _AXIS},
        hoverinfo="skip", showlegend=False,
    )


def _vector_traces(vec: Vec3, color: str, *, always_cone: bool = False):
    """Build the (shaft, arrowhead) traces for a state vector.

    Returns ``(line, cone)``. ``cone`` is ``None`` for a zero-length vector
    unless ``always_cone`` is set (animation frames need a stable trace count).
    """
    x, y, z = (float(c) for c in vec)
    length = math.sqrt(x * x + y * y + z * z)
    line = go.Scatter3d(
        x=[0, x], y=[0, y], z=[0, z], mode="lines",
        line={"color": color, "width": 8}, hoverinfo="skip", showlegend=False,
    )
    if length > 1e-6:
        ux, uy, uz = x / length, y / length, z / length
        cone = go.Cone(
            x=[x], y=[y], z=[z], u=[ux], v=[uy], w=[uz],
            sizemode="absolute", sizeref=0.28, anchor="tip",
            showscale=False, colorscale=[[0, color], [1, color]], hoverinfo="skip",
        )
    elif always_cone:
        cone = go.Cone(
            x=[0], y=[0], z=[0], u=[0], v=[0], w=[1e-3],
            sizemode="absolute", sizeref=1e-6, showscale=False,
            colorscale=[[0, color], [1, color]], hoverinfo="skip", opacity=0.0,
        )
    else:
        cone = None
    return line, cone


def _slerp(a: Vec3, b: Vec3, t: float) -> Vec3:
    """Interpolate from ``a`` to ``b`` along the sphere surface (great circle).

    The tip glides over the sphere instead of cutting through it, and the
    magnitude grows to 1 so a shrunken (entangled) vector lengthens as it
    snaps to the pole.
    """
    av = np.array(a, dtype=float)
    bv = np.array(b, dtype=float)
    na = float(np.linalg.norm(av))
    nb = float(np.linalg.norm(bv))
    ua = av / na if na > 1e-9 else np.array([1.0, 0.0, 0.0])
    ub = bv / nb if nb > 1e-9 else np.array([0.0, 0.0, 1.0])
    dot = float(np.clip(np.dot(ua, ub), -1.0, 1.0))
    omega = math.acos(dot)
    if omega < 1e-6:
        direction = ub
    elif abs(math.pi - omega) < 1e-3:
        # Antipodal: detour through a perpendicular axis so slerp stays stable.
        perp = np.array([1.0, 0.0, 0.0])
        if abs(float(np.dot(ua, perp))) > 0.99:
            perp = np.array([0.0, 1.0, 0.0])
        leg = (1 - 2 * t) * ua + 2 * t * perp if t < 0.5 else (2 - 2 * t) * perp + (2 * t - 1) * ub
        n = float(np.linalg.norm(leg))
        direction = leg / n if n > 1e-9 else ub
    else:
        so = math.sin(omega)
        direction = (math.sin((1 - t) * omega) / so) * ua + (math.sin(t * omega) / so) * ub
    mag = (1 - t) * na + t * 1.0
    v = direction * mag
    return (float(v[0]), float(v[1]), float(v[2]))


def bloch_figure(
    vec: Vec3,
    *,
    label: str = "",
    collapsed: bool = False,
    height: int = 280,
) -> go.Figure:
    """Render one qubit's Bloch sphere with its state vector."""
    x, y, z = (float(c) for c in vec)
    color = vector_color(vec, collapsed=collapsed)
    length = math.sqrt(x * x + y * y + z * z)

    fig = go.Figure()
    fig.add_trace(_sphere_surface())
    for plane in ("xy", "xz", "yz"):
        fig.add_trace(_circle(plane))
    for trace in _axes():
        fig.add_trace(trace)
    fig.add_trace(_pole_labels())

    # State vector: a shaft plus an arrowhead cone at the tip.
    line_trace, cone_trace = _vector_traces((x, y, z), color)
    fig.add_trace(line_trace)
    if cone_trace is not None:
        fig.add_trace(cone_trace)

    title = label
    if collapsed:
        title = f"{label} → {'0' if z >= 0 else '1'}"
    elif length < 0.999:
        title = f"{label}  (|r|={length:.2f})"

    fig.update_layout(
        title={"text": title, "x": 0.5, "y": 0.97, "font": {"size": 13}},
        height=height,
        margin={"l": 0, "r": 0, "t": 24, "b": 0},
        showlegend=False,
        scene=_SCENE,
    )
    return fig


def collapse_animation(
    before: Vec3,
    after: Vec3,
    *,
    label: str = "",
    height: int = 300,
    n_frames: int = 16,
) -> go.Figure:
    """A play-button animation of a qubit collapsing from ``before`` to a pole.

    The arrow starts in superposition (``before``) and, on ▶, glides over the
    sphere to ``after`` (a pole), coloring blue for 0 / red for 1.
    """
    color = vector_color(after, collapsed=True)

    fig = go.Figure()
    fig.add_trace(_sphere_surface())
    for plane in ("xy", "xz", "yz"):
        fig.add_trace(_circle(plane))
    for trace in _axes():
        fig.add_trace(trace)
    fig.add_trace(_pole_labels())

    line0, cone0 = _vector_traces(before, color, always_cone=True)
    line_idx = len(fig.data)
    fig.add_trace(line0)
    cone_idx = len(fig.data)
    fig.add_trace(cone0)

    frames = []
    for k in range(1, n_frames + 1):
        v = _slerp(before, after, k / n_frames)
        line, cone = _vector_traces(v, color, always_cone=True)
        frames.append(go.Frame(name=str(k), data=[line, cone], traces=[line_idx, cone_idx]))
    fig.frames = frames

    target = "0" if after[2] >= 0 else "1"
    title = f"{label} → {target}" if label else f"→ {target}"
    fig.update_layout(
        title={"text": title, "x": 0.5, "y": 0.97, "font": {"size": 13}},
        height=height,
        margin={"l": 0, "r": 0, "t": 24, "b": 30},
        showlegend=False,
        scene=_SCENE,
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "x": 0.5, "y": 0.0, "xanchor": "center", "yanchor": "bottom",
                "pad": {"t": 0, "b": 0},
                "buttons": [
                    {
                        "label": "▶",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {"duration": 55, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                            },
                        ],
                    }
                ],
            }
        ],
    )
    return fig


def probability_bar(p1: float, *, height: int = 90) -> go.Figure:
    """A compact horizontal bar showing P(1) vs P(0) for one qubit."""
    p1 = max(0.0, min(1.0, float(p1)))
    p0 = 1.0 - p1
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[p0], y=[""], orientation="h",
            marker={"color": _BLUE}, name="P(0)",
            hovertemplate="P(0)=%{x:.2f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=[p1], y=[""], orientation="h",
            marker={"color": _RED}, name="P(1)",
            hovertemplate="P(1)=%{x:.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        barmode="stack",
        height=height,
        margin={"l": 8, "r": 8, "t": 8, "b": 8},
        xaxis={"range": [0, 1], "visible": False},
        yaxis={"visible": False},
        showlegend=False,
        annotations=[
            {"x": p0 / 2, "y": 0, "text": f"0 · {p0:.0%}", "showarrow": False,
             "font": {"color": "white", "size": 12}},
            {"x": p0 + p1 / 2, "y": 0, "text": f"1 · {p1:.0%}", "showarrow": False,
             "font": {"color": "white", "size": 12}},
        ],
    )
    return fig
