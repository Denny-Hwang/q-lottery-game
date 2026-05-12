"""Reusable UI components for the Q-Lottery Streamlit app."""
from __future__ import annotations

import html
from typing import Iterable, Optional

import streamlit as st


def _ball_color(number: int, upper_bound: int, palette: list[str]) -> str:
    """Map a number to a color in the palette.

    Real lottery balls are canonically colored by decile (1-10, 11-20, …),
    so we honor that look as long as it fits the palette. For larger ranges
    (e.g. Custom with millions) we fall back to evenly-sized slices.
    """
    if not palette:
        return "#4F46E5"
    if len(palette) == 1:
        return palette[0]
    bucket_size = max(10, (upper_bound + len(palette) - 1) // len(palette))
    idx = min((number - 1) // bucket_size, len(palette) - 1)
    return palette[idx]


def _text_color_for(bg: str) -> str:
    """Pick black or white text based on background luminance."""
    bg = bg.lstrip("#")
    if len(bg) != 6:
        return "#FFFFFF"
    r, g, b = int(bg[0:2], 16), int(bg[2:4], 16), int(bg[4:6], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#111111" if luminance > 0.65 else "#FFFFFF"


def _ball_html(number: int, bg: str, *, animate_delay_ms: int = 0) -> str:
    fg = _text_color_for(bg)
    border = "1px solid #E5E7EB" if bg.upper() == "#FFFFFF" else "none"
    safe_number = html.escape(str(number))
    return (
        "<span class='qlb-ball' style='"
        f"background:{bg};color:{fg};border:{border};"
        f"animation-delay:{animate_delay_ms}ms"
        "'>"
        f"{safe_number}</span>"
    )


def inject_styles() -> None:
    """Inject the shared CSS once per session."""
    if st.session_state.get("_qlb_styles_injected"):
        return
    st.markdown(
        """
        <style>
        .qlb-row {
            display: flex; flex-wrap: wrap; gap: 8px;
            align-items: center; margin: 6px 0 14px 0;
        }
        .qlb-ball {
            display: inline-flex; align-items: center; justify-content: center;
            width: 46px; height: 46px; border-radius: 50%;
            font-weight: 700; font-size: 18px;
            box-shadow: 0 2px 6px rgba(0,0,0,.18);
            animation: qlb-pop .45s cubic-bezier(.2,.9,.3,1.4) both;
            font-variant-numeric: tabular-nums;
        }
        .qlb-bonus-sep {
            font-size: 22px; color: #9CA3AF; margin: 0 4px;
        }
        .qlb-label {
            font-size: 13px; color: #6B7280;
            min-width: 64px;
        }
        @keyframes qlb-pop {
            0%   { transform: scale(.2) rotate(-20deg); opacity: 0; }
            70%  { transform: scale(1.08) rotate(2deg);  opacity: 1; }
            100% { transform: scale(1)    rotate(0);     opacity: 1; }
        }
        .qlb-card {
            border: 1px solid #E5E7EB; border-radius: 12px;
            padding: 12px 16px; margin: 8px 0;
            background: rgba(250,250,255,.6);
        }
        @media (prefers-color-scheme: dark) {
            .qlb-card { background: rgba(30,30,40,.4); border-color:#374151; }
            .qlb-label { color:#9CA3AF; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.session_state["_qlb_styles_injected"] = True


def render_balls(
    numbers: Iterable[int],
    *,
    upper_bound: int,
    palette: list[str],
    bonus: Optional[int] = None,
    bonus_color: Optional[str] = None,
    bonus_upper_bound: Optional[int] = None,
    label: str = "",
) -> None:
    """Render a row of lottery balls with an optional bonus ball."""
    inject_styles()
    pieces: list[str] = ["<div class='qlb-row'>"]
    if label:
        pieces.append(f"<span class='qlb-label'>{html.escape(label)}</span>")
    for i, n in enumerate(numbers):
        pieces.append(_ball_html(n, _ball_color(n, upper_bound, palette), animate_delay_ms=i * 70))
    if bonus is not None:
        pieces.append("<span class='qlb-bonus-sep'>+</span>")
        color = bonus_color or _ball_color(bonus, bonus_upper_bound or 1, palette)
        pieces.append(_ball_html(bonus, color, animate_delay_ms=len(list(numbers)) * 70 + 100))
    pieces.append("</div>")
    st.markdown("".join(pieces), unsafe_allow_html=True)


def render_card_open(title: str) -> None:
    safe = html.escape(title)
    st.markdown(
        f"<div class='qlb-card'><strong>{safe}</strong>",
        unsafe_allow_html=True,
    )


def render_card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def format_share_text(
    title: str,
    rows: list[tuple[str, list[int], Optional[int]]],
) -> str:
    """Plain-text formatter suitable for clipboard / sharing."""
    out = [f"🎰 {title}"]
    for label, numbers, bonus in rows:
        body = "  ".join(f"{n:>2}" for n in numbers)
        if bonus is not None:
            body += f"   + {bonus}"
        out.append(f"{label}:  {body}")
    out.append("")
    out.append("via Q-Lottery Game (IBM Quantum simulator)")
    return "\n".join(out)
