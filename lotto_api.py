"""Korean Lotto (Dong-Haeng Bok-Gwon) draw fetcher and comparator.

The public endpoint we use:

    https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=<N>

It returns JSON like:

    {
      "returnValue": "success",
      "drwNoDate": "2024-01-06",
      "drwNo": 1100,
      "drwtNo1": 7, ..., "drwtNo6": 38,
      "bnusNo": 21
    }

This module is dependency-free (uses ``urllib`` from the stdlib) so it can be
unit-tested via monkeypatching without spinning up a real HTTP server.
"""
from __future__ import annotations

import datetime as dt
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Callable, Optional

FIRST_DRAW_DATE = dt.date(2002, 12, 7)  # draw #1, a Saturday
DRAW_URL = (
    "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={n}"
)
_USER_AGENT = "Mozilla/5.0 (Q-Lottery-Game)"


@dataclass(frozen=True)
class LottoDraw:
    draw_no: int
    date: dt.date
    numbers: tuple[int, ...]  # length 6, sorted
    bonus: int


# ── Draw number estimation ─────────────────────────────────────────────────────
def estimate_latest_draw_no(today: Optional[dt.date] = None) -> int:
    """Best guess of the most recent draw number based on the calendar.

    Korean Lotto draws happen every Saturday at 20:35 KST. We don't model the
    exact draw time here — callers should be prepared for the API to answer
    ``returnValue == "fail"`` on the latest week and walk back one.
    """
    today = today or dt.date.today()
    # weekday(): Mon=0 ... Sat=5, Sun=6
    days_since_saturday = (today.weekday() - 5) % 7
    last_saturday = today - dt.timedelta(days=days_since_saturday)
    weeks = (last_saturday - FIRST_DRAW_DATE).days // 7
    return max(1, weeks + 1)


# ── HTTP layer (injectable for tests) ──────────────────────────────────────────
def _default_http_get(url: str, timeout: float) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # nosec - public API
        return response.read().decode("utf-8")


def fetch_draw(
    draw_no: int,
    *,
    timeout: float = 4.0,
    http_get: Callable[[str, float], str] = _default_http_get,
) -> Optional[LottoDraw]:
    """Fetch a specific draw. Returns ``None`` on any failure or fail status."""
    if draw_no < 1:
        return None
    try:
        body = http_get(DRAW_URL.format(n=draw_no), timeout)
        data = json.loads(body)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get("returnValue") != "success":
        return None
    try:
        numbers = tuple(sorted(int(data[f"drwtNo{i}"]) for i in range(1, 7)))
        return LottoDraw(
            draw_no=int(data["drwNo"]),
            date=dt.date.fromisoformat(data["drwNoDate"]),
            numbers=numbers,
            bonus=int(data["bnusNo"]),
        )
    except (KeyError, TypeError, ValueError):
        return None


def fetch_latest_draw(
    *,
    timeout: float = 4.0,
    http_get: Callable[[str, float], str] = _default_http_get,
    today: Optional[dt.date] = None,
    max_walkback: int = 3,
) -> Optional[LottoDraw]:
    """Fetch the most recent draw, walking back if the estimate is too high."""
    estimate = estimate_latest_draw_no(today=today)
    for offset in range(max_walkback + 1):
        candidate = estimate - offset
        if candidate < 1:
            break
        draw = fetch_draw(candidate, timeout=timeout, http_get=http_get)
        if draw is not None:
            return draw
    return None


# ── Comparison ─────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Comparison:
    match_main: int
    bonus_hit: bool
    rank: Optional[str]  # "1st" .. "5th" or None
    matched_numbers: tuple[int, ...]


_RANK_LABEL_EN = {
    "1st": "1st prize",
    "2nd": "2nd prize",
    "3rd": "3rd prize",
    "4th": "4th prize",
    "5th": "5th prize",
}


def compare(user_numbers: list[int], draw: LottoDraw) -> Comparison:
    """Compare a single set of user numbers to an official draw."""
    user = set(int(n) for n in user_numbers)
    winning = set(draw.numbers)
    match_main = len(user & winning)
    bonus_hit = draw.bonus in user
    rank: Optional[str] = None
    if match_main == 6:
        rank = "1st"
    elif match_main == 5 and bonus_hit:
        rank = "2nd"
    elif match_main == 5:
        rank = "3rd"
    elif match_main == 4:
        rank = "4th"
    elif match_main == 3:
        rank = "5th"
    return Comparison(
        match_main=match_main,
        bonus_hit=bonus_hit,
        rank=rank,
        matched_numbers=tuple(sorted(user & winning)),
    )


def rank_label(rank: Optional[str]) -> str:
    """English label for a rank code (UI layer handles Korean separately)."""
    return _RANK_LABEL_EN.get(rank or "", "No prize")
