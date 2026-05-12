"""Tests for the PNG card exporter."""
from __future__ import annotations

from card_export import render_card_png
from games import KOREAN_LOTTO_PALETTE


def test_returns_png_bytes_with_signature():
    data = render_card_png(
        title="Lotto(Kor)",
        rows=[("Q-lotto-1", [3, 7, 12, 22, 31, 44], None)],
        upper_bound=45,
        palette=KOREAN_LOTTO_PALETTE,
    )
    # PNG magic number: 89 50 4E 47 0D 0A 1A 0A
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    # Non-trivial size
    assert len(data) > 4_000


def test_multiple_rows_increases_height():
    one_row = render_card_png(
        title="t",
        rows=[("a", [1, 2, 3, 4, 5, 6], None)],
        upper_bound=45,
        palette=KOREAN_LOTTO_PALETTE,
    )
    five_rows = render_card_png(
        title="t",
        rows=[(f"row{i}", [1, 2, 3, 4, 5, 6], None) for i in range(5)],
        upper_bound=45,
        palette=KOREAN_LOTTO_PALETTE,
    )
    assert len(five_rows) > len(one_row)


def test_with_bonus_ball():
    data = render_card_png(
        title="Powerball",
        rows=[("Q-powerball-1", [5, 17, 24, 33, 61], 9)],
        upper_bound=69,
        palette=["#FFFFFF"],
        bonus_color="#E11D48",
        bonus_upper_bound=26,
    )
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
