"""Tests for the Korean Lotto fetcher + comparator.

Network is mocked with an injected ``http_get`` so the suite is hermetic.
"""
from __future__ import annotations

import datetime as dt
import json

import pytest

from lotto_api import (
    Comparison,
    FIRST_DRAW_DATE,
    LottoDraw,
    compare,
    estimate_latest_draw_no,
    fetch_draw,
    fetch_latest_draw,
    rank_label,
)


# ── Estimation ────────────────────────────────────────────────────────────────
class TestEstimateLatestDrawNo:
    def test_first_saturday_is_draw_one(self):
        assert estimate_latest_draw_no(today=FIRST_DRAW_DATE) == 1

    def test_week_later_is_draw_two(self):
        assert (
            estimate_latest_draw_no(today=FIRST_DRAW_DATE + dt.timedelta(days=7))
            == 2
        )

    def test_friday_uses_previous_saturday(self):
        # Friday after first draw should still be draw #1.
        friday = FIRST_DRAW_DATE + dt.timedelta(days=6)
        assert estimate_latest_draw_no(today=friday) == 1

    def test_never_below_one(self):
        assert estimate_latest_draw_no(today=dt.date(1990, 1, 1)) == 1


# ── HTTP-mocked fetching ──────────────────────────────────────────────────────
def _fake_http(payload):
    """Return an http_get-compatible callable that always answers with ``payload``."""

    def _get(url, timeout):
        if callable(payload):
            return payload(url, timeout)
        return payload

    return _get


_SUCCESS_PAYLOAD = json.dumps(
    {
        "returnValue": "success",
        "drwNoDate": "2024-01-06",
        "drwNo": 1100,
        "drwtNo1": 7,
        "drwtNo2": 13,
        "drwtNo3": 18,
        "drwtNo4": 36,
        "drwtNo5": 39,
        "drwtNo6": 45,
        "bnusNo": 21,
    }
)

_FAIL_PAYLOAD = json.dumps({"returnValue": "fail"})


class TestFetchDraw:
    def test_success(self):
        draw = fetch_draw(1100, http_get=_fake_http(_SUCCESS_PAYLOAD))
        assert isinstance(draw, LottoDraw)
        assert draw.draw_no == 1100
        assert draw.numbers == (7, 13, 18, 36, 39, 45)
        assert draw.bonus == 21
        assert draw.date == dt.date(2024, 1, 6)

    def test_fail_status(self):
        assert fetch_draw(99999, http_get=_fake_http(_FAIL_PAYLOAD)) is None

    def test_invalid_json(self):
        assert fetch_draw(1, http_get=_fake_http("not json")) is None

    def test_invalid_draw_no(self):
        assert fetch_draw(0, http_get=_fake_http(_SUCCESS_PAYLOAD)) is None
        assert fetch_draw(-5, http_get=_fake_http(_SUCCESS_PAYLOAD)) is None

    def test_http_error_is_swallowed(self):
        def _raise(url, timeout):
            raise OSError("network is the computer")

        assert fetch_draw(1, http_get=_raise) is None


class TestFetchLatestDraw:
    def test_walks_back_on_fail(self):
        calls = []

        def _get(url, timeout):
            calls.append(url)
            # First few attempts return "fail" (latest draw not yet posted)
            if len(calls) < 3:
                return _FAIL_PAYLOAD
            return _SUCCESS_PAYLOAD

        result = fetch_latest_draw(http_get=_get, today=dt.date(2024, 1, 10))
        assert result is not None
        assert result.draw_no == 1100
        # We expect a walkback over distinct draw numbers
        assert len(calls) == 3

    def test_returns_none_when_all_fail(self):
        result = fetch_latest_draw(
            http_get=_fake_http(_FAIL_PAYLOAD), today=dt.date(2024, 1, 10)
        )
        assert result is None


# ── Comparator ────────────────────────────────────────────────────────────────
@pytest.fixture
def reference_draw():
    return LottoDraw(
        draw_no=1100,
        date=dt.date(2024, 1, 6),
        numbers=(7, 13, 18, 36, 39, 45),
        bonus=21,
    )


class TestCompare:
    def test_first_prize(self, reference_draw):
        result = compare([7, 13, 18, 36, 39, 45], reference_draw)
        assert result.match_main == 6
        assert result.rank == "1st"

    def test_second_prize_requires_bonus(self, reference_draw):
        # 5 matches + bonus = 2nd
        result = compare([7, 13, 18, 36, 39, 21], reference_draw)
        assert result.match_main == 5
        assert result.bonus_hit is True
        assert result.rank == "2nd"

    def test_third_prize(self, reference_draw):
        # 5 matches, no bonus
        result = compare([7, 13, 18, 36, 39, 1], reference_draw)
        assert result.match_main == 5
        assert result.bonus_hit is False
        assert result.rank == "3rd"

    def test_fourth_prize(self, reference_draw):
        result = compare([7, 13, 18, 36, 2, 3], reference_draw)
        assert result.rank == "4th"

    def test_fifth_prize(self, reference_draw):
        result = compare([7, 13, 18, 2, 3, 4], reference_draw)
        assert result.rank == "5th"

    def test_no_prize(self, reference_draw):
        result = compare([1, 2, 3, 4, 5, 6], reference_draw)
        assert result.rank is None
        assert isinstance(result, Comparison)

    def test_bonus_only_no_main_match_is_no_prize(self, reference_draw):
        result = compare([21, 1, 2, 3, 4, 5], reference_draw)
        assert result.match_main == 0
        assert result.bonus_hit is True
        assert result.rank is None


class TestRankLabel:
    def test_known(self):
        assert rank_label("1st") == "1st prize"

    def test_none(self):
        assert rank_label(None) == "No prize"
