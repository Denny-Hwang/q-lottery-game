"""Render a downloadable PNG "ticket" of a Q-Lottery result.

The card is drawn with matplotlib so we don't add a heavy dependency (matplotlib
is already pulled in for circuit drawing). Output is PNG bytes suitable for
``st.download_button``.
"""
from __future__ import annotations

from io import BytesIO
from typing import Iterable, Optional

import matplotlib

matplotlib.use("Agg", force=False)
import matplotlib.patches as mpatches  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

from ui import _ball_color, _text_color_for  # reuse the same color logic

# Card dimensions (in inches). Output PNG = dimensions × dpi.
_DPI = 160
_CARD_W = 6.4
_ROW_HEIGHT = 0.95
_HEADER_HEIGHT = 1.4
_FOOTER_HEIGHT = 0.7


def render_card_png(
    *,
    title: str,
    rows: Iterable[tuple[str, list[int], Optional[int]]],
    upper_bound: int,
    palette: list[str],
    bonus_color: Optional[str] = None,
    bonus_upper_bound: Optional[int] = None,
    footer: str = "via Q-Lottery Game · IBM Quantum simulator",
) -> bytes:
    """Render rows of (label, numbers, bonus) into a PNG ticket and return bytes."""
    rows = list(rows)
    n_rows = max(1, len(rows))
    height = _HEADER_HEIGHT + n_rows * _ROW_HEIGHT + _FOOTER_HEIGHT

    fig = plt.figure(figsize=(_CARD_W, height), dpi=_DPI)
    fig.patch.set_facecolor("#FFFFFF")
    ax = fig.add_axes((0, 0, 1, 1))  # full-figure axes
    ax.set_xlim(0, _CARD_W)
    ax.set_ylim(0, height)
    ax.axis("off")

    # Decorative outer card border
    ax.add_patch(
        mpatches.FancyBboxPatch(
            (0.18, 0.18),
            _CARD_W - 0.36,
            height - 0.36,
            boxstyle="round,pad=0.02,rounding_size=0.18",
            linewidth=1.4,
            edgecolor="#E5E7EB",
            facecolor="#FFFFFF",
        )
    )

    # Header
    header_y = height - 0.55
    ax.text(
        _CARD_W / 2,
        header_y,
        title,
        ha="center",
        va="center",
        fontsize=20,
        fontweight="bold",
        color="#111827",
    )
    ax.text(
        _CARD_W / 2,
        header_y - 0.45,
        "Q-Lottery Game",
        ha="center",
        va="center",
        fontsize=10,
        color="#6B7280",
    )

    # Rows
    label_x = 0.55
    balls_origin_x = 1.55
    ball_radius = 0.30
    ball_pitch = 0.72

    for i, (label, numbers, bonus) in enumerate(rows):
        row_center_y = height - _HEADER_HEIGHT - (i + 0.5) * _ROW_HEIGHT

        ax.text(
            label_x,
            row_center_y,
            label,
            ha="left",
            va="center",
            fontsize=10,
            color="#6B7280",
        )

        for j, n in enumerate(numbers):
            cx = balls_origin_x + j * ball_pitch
            color = _ball_color(n, upper_bound, palette)
            _draw_ball(ax, cx, row_center_y, ball_radius, n, color)

        if bonus is not None:
            sep_x = balls_origin_x + len(numbers) * ball_pitch - 0.10
            ax.text(
                sep_x,
                row_center_y,
                "+",
                ha="center",
                va="center",
                fontsize=18,
                color="#9CA3AF",
            )
            bonus_cx = sep_x + ball_pitch * 0.85
            bonus_col = bonus_color or _ball_color(
                bonus, bonus_upper_bound or 1, palette
            )
            _draw_ball(ax, bonus_cx, row_center_y, ball_radius, bonus, bonus_col)

    # Footer
    ax.text(
        _CARD_W / 2,
        0.42,
        footer,
        ha="center",
        va="center",
        fontsize=8.5,
        color="#9CA3AF",
        style="italic",
    )

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=_DPI, facecolor="#FFFFFF")
    plt.close(fig)
    return buf.getvalue()


def _draw_ball(ax, cx: float, cy: float, radius: float, number: int, color: str) -> None:
    """Draw a single colored ball with its number."""
    edge = "#D1D5DB" if color.upper() == "#FFFFFF" else "none"
    ax.add_patch(
        mpatches.Circle(
            (cx, cy),
            radius,
            facecolor=color,
            edgecolor=edge,
            linewidth=1.2,
        )
    )
    ax.text(
        cx,
        cy,
        str(number),
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color=_text_color_for(color),
    )
