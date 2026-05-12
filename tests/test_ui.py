"""Unit tests for the ball renderer helpers."""
from __future__ import annotations

from games import KOREAN_LOTTO_PALETTE, RAINBOW_PALETTE
from ui import _ball_color, _text_color_for, format_share_text


class TestBallColor:
    def test_korean_palette_buckets(self):
        # 1-10 yellow, 11-20 blue, 21-30 red, 31-40 grey, 41-45 green
        assert _ball_color(1, 45, KOREAN_LOTTO_PALETTE) == "#FBC400"
        assert _ball_color(10, 45, KOREAN_LOTTO_PALETTE) == "#FBC400"
        assert _ball_color(11, 45, KOREAN_LOTTO_PALETTE) == "#69C8F2"
        assert _ball_color(20, 45, KOREAN_LOTTO_PALETTE) == "#69C8F2"
        assert _ball_color(45, 45, KOREAN_LOTTO_PALETTE) == "#B0D840"

    def test_rainbow_palette_does_not_crash_for_any_number(self):
        for n in range(1, 70):
            color = _ball_color(n, 69, RAINBOW_PALETTE)
            assert color.startswith("#")

    def test_single_color_palette(self):
        assert _ball_color(5, 99, ["#FFFFFF"]) == "#FFFFFF"

    def test_empty_palette_has_fallback(self):
        assert _ball_color(5, 10, []).startswith("#")


class TestTextColorFor:
    def test_white_background_yields_dark_text(self):
        assert _text_color_for("#FFFFFF") == "#111111"

    def test_black_background_yields_light_text(self):
        assert _text_color_for("#000000") == "#FFFFFF"


class TestShareText:
    def test_basic_format(self):
        text = format_share_text(
            "Lotto(Kor)",
            [
                ("Q-lotto-1", [3, 7, 12, 22, 31, 44], None),
                ("Q-lotto-2", [1, 2, 3, 4, 5, 6], None),
            ],
        )
        assert "Q-lotto-1" in text
        assert "Q-lotto-2" in text
        assert "Lotto(Kor)" in text

    def test_with_bonus(self):
        text = format_share_text(
            "Powerball",
            [("Q-powerball-1", [5, 17, 24, 33, 61], 9)],
        )
        assert "+ 9" in text
