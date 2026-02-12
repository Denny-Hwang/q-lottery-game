from dataclasses import dataclass
from datetime import date
from typing import Optional, Callable

from game_doc import (
    lotto_doc,
    powerball_doc,
    lotto_india_doc,
    lotto7_doc,
    french_lottery_doc,
)


@dataclass
class GameConfig:
    doc_fn: Callable
    ball_labels: list
    main_count: int
    main_upper_bound: int
    bonus_upper_bound: Optional[int]
    col_prefix: str
    min_date: date


GAMES = {
    "Lotto(Kor)": GameConfig(
        doc_fn=lotto_doc,
        ball_labels=["Num_1", "Num_2", "Num_3", "Num_4", "Num_5", "Num_6"],
        main_count=6,
        main_upper_bound=45,
        bonus_upper_bound=None,
        col_prefix="Q-lotto",
        min_date=date(1887, 8, 12),  # Schrödinger's birthday
    ),
    "Powerball(USA)": GameConfig(
        doc_fn=powerball_doc,
        ball_labels=["W_ball_1", "W_ball_2", "W_ball_3", "W_ball_4", "W_ball_5", "Power_ball"],
        main_count=5,
        main_upper_bound=69,
        bonus_upper_bound=26,
        col_prefix="Q-powerball",
        min_date=date(1918, 5, 11),  # Feynman's birthday
    ),
    "Lotto India(India)": GameConfig(
        doc_fn=lotto_india_doc,
        ball_labels=["Ball_1", "Ball_2", "Ball_3", "Ball_4", "Ball_5", "Ball_6", "Joker_ball"],
        main_count=6,
        main_upper_bound=50,
        bonus_upper_bound=5,
        col_prefix="Q-Lotto_India",
        min_date=date(1918, 5, 11),  # Feynman's birthday
    ),
    "Lotto7(Japan)": GameConfig(
        doc_fn=lotto7_doc,
        ball_labels=["Num_1", "Num_2", "Num_3", "Num_4", "Num_5", "Num_6", "Num_7"],
        main_count=7,
        main_upper_bound=37,
        bonus_upper_bound=None,
        col_prefix="Q-lotto7",
        min_date=date(1887, 8, 12),  # Schrödinger's birthday
    ),
    "French lottery(France)": GameConfig(
        doc_fn=french_lottery_doc,
        ball_labels=["Ball_1", "Ball_2", "Ball_3", "Ball_4", "Ball_5", "Lucky_Number"],
        main_count=5,
        main_upper_bound=49,
        bonus_upper_bound=10,
        col_prefix="Q-French_lottery",
        min_date=date(1918, 5, 11),  # Feynman's birthday
    ),
}
