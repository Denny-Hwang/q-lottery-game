"""Static configuration for every supported lottery."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Callable, Optional

from game_doc import (
    french_lottery_doc,
    lotto7_doc,
    lotto_doc,
    lotto_india_doc,
    powerball_doc,
)

# Palettes used by the ball renderer in ui.py. Each entry maps a (1-indexed)
# decile of the upper bound to a hex color. The Korean Lotto palette is the
# canonical "lottery ball" coloring; other games reuse a clean rainbow.
KOREAN_LOTTO_PALETTE = [
    "#FBC400",  # 1-10  yellow
    "#69C8F2",  # 11-20 blue
    "#FF7272",  # 21-30 red
    "#AAAAAA",  # 31-40 grey
    "#B0D840",  # 41-45 green
]

RAINBOW_PALETTE = [
    "#EF4444",  # red
    "#F59E0B",  # amber
    "#10B981",  # emerald
    "#3B82F6",  # blue
    "#8B5CF6",  # violet
    "#EC4899",  # pink
    "#14B8A6",  # teal
]


@dataclass(frozen=True)
class GameConfig:
    doc_fn: Callable
    ball_labels: list
    main_count: int
    main_upper_bound: int
    bonus_upper_bound: Optional[int]
    col_prefix: str
    main_palette: list
    bonus_color: Optional[str]
    # A reasonable lower bound for birthday input — covers virtually every
    # living user without trapping them in date-picker scroll-purgatory.
    min_date: date = date(1925, 1, 1)


GAMES = {
    "Lotto(Kor)": GameConfig(
        doc_fn=lotto_doc,
        ball_labels=["Num_1", "Num_2", "Num_3", "Num_4", "Num_5", "Num_6"],
        main_count=6,
        main_upper_bound=45,
        bonus_upper_bound=None,
        col_prefix="Q-lotto",
        main_palette=KOREAN_LOTTO_PALETTE,
        bonus_color=None,
    ),
    "Powerball(USA)": GameConfig(
        doc_fn=powerball_doc,
        ball_labels=[
            "W_ball_1",
            "W_ball_2",
            "W_ball_3",
            "W_ball_4",
            "W_ball_5",
            "Power_ball",
        ],
        main_count=5,
        main_upper_bound=69,
        bonus_upper_bound=26,
        col_prefix="Q-powerball",
        main_palette=["#FFFFFF"],  # classic white ball, rendered with a border
        bonus_color="#E11D48",  # red Powerball
    ),
    "Lotto India(India)": GameConfig(
        doc_fn=lotto_india_doc,
        ball_labels=[
            "Ball_1",
            "Ball_2",
            "Ball_3",
            "Ball_4",
            "Ball_5",
            "Ball_6",
            "Joker_ball",
        ],
        main_count=6,
        main_upper_bound=50,
        bonus_upper_bound=5,
        col_prefix="Q-Lotto_India",
        main_palette=RAINBOW_PALETTE,
        bonus_color="#F59E0B",
    ),
    "Lotto7(Japan)": GameConfig(
        doc_fn=lotto7_doc,
        ball_labels=[
            "Num_1",
            "Num_2",
            "Num_3",
            "Num_4",
            "Num_5",
            "Num_6",
            "Num_7",
        ],
        main_count=7,
        main_upper_bound=37,
        bonus_upper_bound=None,
        col_prefix="Q-lotto7",
        main_palette=RAINBOW_PALETTE,
        bonus_color=None,
    ),
    "French lottery(France)": GameConfig(
        doc_fn=french_lottery_doc,
        ball_labels=[
            "Ball_1",
            "Ball_2",
            "Ball_3",
            "Ball_4",
            "Ball_5",
            "Lucky_Number",
        ],
        main_count=5,
        main_upper_bound=49,
        bonus_upper_bound=10,
        col_prefix="Q-French_lottery",
        main_palette=RAINBOW_PALETTE,
        bonus_color="#22C55E",
    ),
}
