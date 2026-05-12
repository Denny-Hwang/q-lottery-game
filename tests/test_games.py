"""Sanity tests for the game registry."""
from __future__ import annotations

from games import GAMES, GameConfig


def test_all_games_well_formed():
    assert GAMES, "Registry must not be empty"
    for name, cfg in GAMES.items():
        assert isinstance(cfg, GameConfig), name
        assert len(cfg.ball_labels) == cfg.main_count + (
            1 if cfg.bonus_upper_bound else 0
        ), f"{name}: ball_labels length doesn't match main+bonus count"
        assert cfg.main_upper_bound >= 2, name
        if cfg.bonus_upper_bound is not None:
            assert cfg.bonus_upper_bound >= 2, name
        assert cfg.main_palette, f"{name}: palette must be non-empty"
        assert callable(cfg.doc_fn), name


def test_palette_supports_full_range():
    """Confirm we can color every legal ball without index errors."""
    from ui import _ball_color

    for cfg in GAMES.values():
        for n in (1, cfg.main_upper_bound // 2 or 1, cfg.main_upper_bound):
            color = _ball_color(n, cfg.main_upper_bound, cfg.main_palette)
            assert color.startswith("#") and len(color) in (4, 7)
