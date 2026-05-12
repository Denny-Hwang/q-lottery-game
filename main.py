"""Streamlit entry point for the Q-Lottery Game.

Responsibilities:
- Page chrome (title, favicon, sidebar language switcher)
- Routing between About / each lottery / Custom
- Generating numbers, rendering them as colored balls, and maintaining a small
  per-session history with a copy-friendly share text.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd
import streamlit as st

import intro_doc
from game_doc import custom_doc
from games import GAMES, GameConfig
from i18n import LANG_LABEL, SUPPORTED, get_lang, set_lang, t
from q_function import (
    QRNGError,
    bits_needed,
    q_rng_lotto,
    q_rng_lotto_with_birthday,
)
from ui import (
    format_share_text,
    inject_styles,
    render_balls,
)

# ── Page setup ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Q-Lottery Game",
    page_icon="🎰",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Report a bug": "https://github.com/Denny-Hwang/q-lottery-game/issues",
        "About": (
            "Quantum-powered lottery number generator built with Streamlit + "
            "IBM Qiskit. https://github.com/Denny-Hwang/q-lottery-game"
        ),
    },
)
inject_styles()


# ── Session state defaults ─────────────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"
if "history" not in st.session_state:
    st.session_state["history"] = []  # list[HistoryEntry]


@dataclass
class HistoryEntry:
    timestamp: str
    game: str
    rows: list  # list[tuple[label, numbers, bonus or None]]
    share_text: str
    palette: list = field(default_factory=list)
    upper_bound: int = 0
    bonus_upper_bound: Optional[int] = None
    bonus_color: Optional[str] = None


# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.image(
    "src/Q-Lottery-Game-logo-black.png",
    width=260,
)
st.sidebar.caption(t("sidebar.tagline"))

lang_options = list(SUPPORTED)
current_lang_idx = lang_options.index(get_lang())
chosen_lang = st.sidebar.radio(
    t("sidebar.language"),
    options=lang_options,
    index=current_lang_idx,
    format_func=lambda c: LANG_LABEL[c],
    horizontal=True,
    key="lang_selector",
)
if chosen_lang != get_lang():
    set_lang(chosen_lang)
    st.rerun()

menu_options = [t("sidebar.about")] + list(GAMES.keys()) + [t("sidebar.custom")]
lot_selection = st.sidebar.radio(t("sidebar.menu"), menu_options)

st.sidebar.divider()
if st.session_state["history"]:
    if st.sidebar.button(t("button.clear_history"), use_container_width=True):
        st.session_state["history"] = []
        st.rerun()


# ── Helpers ────────────────────────────────────────────────────────────────────
def _sample_one(*, is_birthday, month, day, bits, bound, draw):
    if is_birthday:
        return q_rng_lotto_with_birthday(month, day, bits=bits, upper_bound=bound, draw=draw)
    return q_rng_lotto(bits=bits, upper_bound=bound, draw=draw)


def generate_numbers_detailed(
    *,
    is_birthday: bool,
    month: Optional[int],
    day: Optional[int],
    main_count: int,
    main_bits: int,
    main_bound: int,
    bonus_bits: Optional[int] = None,
    bonus_bound: Optional[int] = None,
    draw: bool = False,
):
    """Generate one full game and return (numbers, bit-detail, main_fig, bonus_fig)."""
    lotto: list[int] = []
    details: list[tuple[str, int]] = []
    main_fig = None

    attempts = 0
    max_attempts = main_count * 32
    while len(lotto) < main_count:
        attempts += 1
        if attempts > max_attempts:
            raise QRNGError("Could not generate enough unique numbers.")
        fig, raw, dec = _sample_one(
            is_birthday=is_birthday,
            month=month,
            day=day,
            bits=main_bits,
            bound=main_bound,
            draw=draw and main_fig is None,
        )
        if dec in lotto:
            continue
        binary_str = raw.split(" ")[0][:main_bits]
        lotto.append(dec)
        details.append((binary_str, dec))
        if main_fig is None and fig is not None:
            main_fig = fig

    paired = sorted(zip(lotto, details), key=lambda x: x[0])
    numbers = [p[0] for p in paired]
    details = [p[1] for p in paired]

    bonus_fig = None
    if bonus_bound is not None:
        fig, raw, dec = _sample_one(
            is_birthday=is_birthday,
            month=month,
            day=day,
            bits=bonus_bits,
            bound=bonus_bound,
            draw=draw,
        )
        binary_str = raw.split(" ")[0][:bonus_bits]
        numbers.append(dec)
        details.append((binary_str, dec))
        bonus_fig = fig

    return numbers, details, main_fig, bonus_fig


def _render_history() -> None:
    history = st.session_state["history"]
    if not history:
        return
    with st.expander(t("history.heading"), expanded=False):
        for entry in reversed(history[-10:]):
            st.markdown(f"**{entry.timestamp} · {entry.game}**")
            for label, numbers, bonus in entry.rows:
                render_balls(
                    numbers,
                    upper_bound=entry.upper_bound,
                    palette=entry.palette,
                    bonus=bonus,
                    bonus_color=entry.bonus_color,
                    bonus_upper_bound=entry.bonus_upper_bound,
                    label=label,
                )
            st.divider()


def _push_history(entry: HistoryEntry) -> None:
    history = st.session_state["history"]
    history.append(entry)
    # Keep memory bounded
    del history[:-20]


def _birthday_inputs(min_date: dt.date):
    """Render the birthday picker with sensible defaults."""
    st.markdown(f"#### {t('mode.birthday')}")
    st.caption(t("mode.birthday.help"))
    default = dt.date(1990, 1, 1)
    if default < min_date:
        default = min_date
    birth_day = st.date_input(
        t("birthday.label"),
        value=default,
        min_value=min_date,
        max_value=dt.date.today(),
        format="YYYY-MM-DD",
    )
    st.caption(f"{t('birthday.value')} {birth_day.isoformat()}")
    return birth_day.month, birth_day.day


def _render_game_form(
    *,
    game_label: str,
    ball_labels: list[str],
    main_count: int,
    main_upper_bound: int,
    bonus_upper_bound: Optional[int],
    col_prefix: str,
    main_palette: list[str],
    bonus_color: Optional[str],
    min_date: dt.date,
):
    mode = st.radio(
        t("mode.label"),
        options=("simple", "birthday"),
        format_func=lambda m: t(f"mode.{m}"),
        horizontal=True,
    )
    is_birthday = mode == "birthday"

    month = day = None
    if is_birthday:
        month, day = _birthday_inputs(min_date)
    else:
        st.caption(t("mode.simple.help"))

    num_game = st.selectbox(t("games.count"), options=(1, 2, 3, 4, 5), index=0)
    show_details = st.toggle(
        t("details.toggle"),
        value=False,
        help=t("details.help"),
    )

    if not st.button(t("button.generate"), type="primary", use_container_width=True):
        _render_history()
        return

    main_bits = bits_needed(main_upper_bound)
    bonus_bits = bits_needed(bonus_upper_bound) if bonus_upper_bound else None

    rows_for_share: list[tuple[str, list[int], Optional[int]]] = []
    detail_blocks: list[tuple[str, list, object, object]] = []

    try:
        with st.spinner(t("button.generating")):
            for i in range(num_game):
                numbers, details, main_fig, bonus_fig = generate_numbers_detailed(
                    is_birthday=is_birthday,
                    month=month,
                    day=day,
                    main_count=main_count,
                    main_bits=main_bits,
                    main_bound=main_upper_bound,
                    bonus_bits=bonus_bits,
                    bonus_bound=bonus_upper_bound,
                    draw=show_details,
                )
                main_nums = numbers[:main_count]
                bonus = numbers[main_count] if bonus_upper_bound else None
                label = f"{col_prefix}-{i + 1}"
                rows_for_share.append((label, main_nums, bonus))
                detail_blocks.append((label, details, main_fig, bonus_fig))
    except QRNGError as exc:
        st.error(f"{t('error.qrng')}\n\n```\n{exc}\n```")
        return

    # ── Results ────────────────────────────────────────────────────────────
    st.subheader(t("result.heading"))
    for label, main_nums, bonus in rows_for_share:
        render_balls(
            main_nums,
            upper_bound=main_upper_bound,
            palette=main_palette,
            bonus=bonus,
            bonus_color=bonus_color,
            bonus_upper_bound=bonus_upper_bound,
            label=label,
        )

    # Share-friendly text
    share_text = format_share_text(game_label, rows_for_share)
    st.caption(t("result.share_caption"))
    st.code(share_text, language="text")

    _push_history(
        HistoryEntry(
            timestamp=dt.datetime.now().strftime("%H:%M:%S"),
            game=game_label,
            rows=rows_for_share,
            share_text=share_text,
            palette=main_palette,
            upper_bound=main_upper_bound,
            bonus_upper_bound=bonus_upper_bound,
            bonus_color=bonus_color,
        )
    )

    # ── Details (lazy) ─────────────────────────────────────────────────────
    if show_details:
        st.divider()
        st.subheader(t("details.heading"))
        st.caption(t("details.caption"))
        for label, details, main_fig, bonus_fig in detail_blocks:
            with st.expander(f"{t('result.game')} {label}", expanded=(num_game == 1)):
                if bonus_fig is not None:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**{t('details.circuit.main')}**")
                        st.pyplot(main_fig)
                    with c2:
                        st.markdown(f"**{t('details.circuit.bonus')}**")
                        st.pyplot(bonus_fig)
                else:
                    st.markdown(f"**{t('details.circuit')}**")
                    st.pyplot(main_fig)

                st.markdown(f"**{t('details.decoding')}**")
                mapping = [
                    {
                        t("details.col.ball"): bl,
                        t("details.col.binary"): binary,
                        "→": "→",
                        t("details.col.decimal"): int(decimal),
                    }
                    for bl, (binary, decimal) in zip(ball_labels, details)
                ]
                st.dataframe(
                    pd.DataFrame(mapping),
                    hide_index=True,
                    use_container_width=True,
                )

    _render_history()


def render_game(label: str, config: GameConfig) -> None:
    config.doc_fn()
    st.divider()
    _render_game_form(
        game_label=label,
        ball_labels=config.ball_labels,
        main_count=config.main_count,
        main_upper_bound=config.main_upper_bound,
        bonus_upper_bound=config.bonus_upper_bound,
        col_prefix=config.col_prefix,
        main_palette=config.main_palette,
        bonus_color=config.bonus_color,
        min_date=config.min_date,
    )


def render_custom() -> None:
    custom_doc()
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        custom_n = st.number_input(
            t("custom.count"),
            step=1, min_value=1, max_value=10, value=6,
        )
    with c2:
        u_bound = st.number_input(
            t("custom.upper"),
            step=1, min_value=2, max_value=9_000_000_000_000_000, value=45,
        )

    _render_game_form(
        game_label="Custom",
        ball_labels=[f"num{i + 1}" for i in range(int(custom_n))],
        main_count=int(custom_n),
        main_upper_bound=int(u_bound),
        bonus_upper_bound=None,
        col_prefix="Q-lotto",
        main_palette=[
            "#EF4444", "#F59E0B", "#10B981", "#3B82F6",
            "#8B5CF6", "#EC4899", "#14B8A6",
        ],
        bonus_color=None,
        min_date=dt.date(1925, 1, 1),
    )


def render_about() -> None:
    intro_doc.intro_header()
    st.divider()
    intro_doc.intro_concept()

    intro_doc.intro_modes_simple()
    st.write(intro_doc.example_simple_caption())
    from q_function import random_number  # local import keeps top of module cleaner

    bits = 6
    try:
        fig_a, raw_a, dec_a = random_number(bits=bits, draw=True)
        st.pyplot(fig_a)
        st.markdown(intro_doc.example_result_line(raw_a[:bits], dec_a))
    except Exception as exc:  # pragma: no cover - simulator failure is rare
        st.warning(str(exc))

    intro_doc.intro_modes_birthday()
    st.write(intro_doc.example_birthday_caption())
    from q_function import random_number_with_birthday

    try:
        fig_b, raw_b, dec_b = random_number_with_birthday(
            8, 30, bits=bits, draw=True
        )
        st.pyplot(fig_b)
        st.markdown(intro_doc.example_result_line(raw_b[:bits], dec_b))
    except Exception as exc:  # pragma: no cover
        st.warning(str(exc))

    intro_doc.intro_games()

    st.divider()
    st.markdown(f"### {t('caution.title')}")
    st.warning(t("caution.body"))


# ── Routing ────────────────────────────────────────────────────────────────────
if lot_selection == t("sidebar.about"):
    render_about()
elif lot_selection == t("sidebar.custom"):
    render_custom()
elif lot_selection in GAMES:
    render_game(lot_selection, GAMES[lot_selection])
