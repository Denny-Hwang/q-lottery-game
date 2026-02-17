import streamlit as st
import pandas as pd
import numpy as np
import datetime

from q_function import (
    q_rng_lotto,
    get_rng_lotto,
    q_rng_lotto_with_birthday,
    get_rng_lotto_with_birthday,
    bits_needed,
)
from intro_doc import intro_1, intro_2, intro_3, intro_4
from game_doc import custom_doc
from games import GAMES

# ─── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://github.com/Denny-Hwang/q-lottery-game/blob/main/src/Q-Lottery-Game-logo-black.png?raw=true",
    width=333,
)

menu_options = ["About Q-Lottery Game"] + list(GAMES.keys()) + ["Custom"]
lot_selection = st.sidebar.selectbox("Select the menu", menu_options)
st.sidebar.write("Selected : ", lot_selection)


# ─── Helper functions ──────────────────────────────────────────────────────────
def generate_numbers(is_birthday, month, day, main_count, main_bits, main_bound,
                     bonus_bits=None, bonus_bound=None):
    """Generate lottery numbers for a single game."""
    if is_birthday:
        numbers = get_rng_lotto_with_birthday(
            month, day, n_get_num=main_count, bits=main_bits, upper_bound=main_bound,
        )
    else:
        numbers = get_rng_lotto(n_get_num=main_count, bits=main_bits, upper_bound=main_bound)

    if bonus_bound is not None:
        if is_birthday:
            _, _, bonus = q_rng_lotto_with_birthday(
                month, day, bits=bonus_bits, upper_bound=bonus_bound,
            )
        else:
            _, _, bonus = q_rng_lotto(bits=bonus_bits, upper_bound=bonus_bound)
        numbers = np.append(numbers, bonus)

    return numbers


def render_game(config):
    """Render a lottery game page with mode selection and number generation."""
    config.doc_fn()
    st.write("---")

    result = pd.DataFrame(index=config.ball_labels)

    mode = st.radio(
        "Select the Q-RNG lottery game mode",
        ("1) Simple Q-RNG", "2) Birth-day entangled Q-RNG"),
    )
    st.write("---")

    is_birthday = mode == "2) Birth-day entangled Q-RNG"

    month, day = None, None
    if is_birthday:
        st.subheader("2) Birth-day entangled Q-RNG")
        birth_day = st.date_input(
            "When's your birthday",
            datetime.datetime.today(),
            min_value=config.min_date,
            max_value=datetime.datetime.today(),
        )
        st.write("Your birthday is:", birth_day)
        month = birth_day.month
        day = birth_day.day
    else:
        st.subheader("1) Simple Q-RNG for Lottery Game")

    num_game = st.selectbox("How many games do you want?", (1, 2, 3, 4, 5))
    go = st.button("Q-Random Number Generation \U0001F448")

    if go:
        main_bits = bits_needed(config.main_upper_bound)
        bonus_bits = bits_needed(config.bonus_upper_bound) if config.bonus_upper_bound else None

        for i in range(num_game):
            numbers = generate_numbers(
                is_birthday, month, day,
                main_count=config.main_count,
                main_bits=main_bits,
                main_bound=config.main_upper_bound,
                bonus_bits=bonus_bits,
                bonus_bound=config.bonus_upper_bound,
            )
            result[f"{config.col_prefix}-{i + 1}"] = numbers
        st.dataframe(data=result)


# ─── Page routing ──────────────────────────────────────────────────────────────
if lot_selection == "About Q-Lottery Game":
    intro_1()

    intro_2()
    bits, u_bound = 6, 45
    st.write("> Example circuit ")
    circuit_example_A, raw_bits_A, decimal_A = q_rng_lotto(bits=bits, upper_bound=u_bound)
    st.pyplot(circuit_example_A)
    st.write(f"     Generated number : {raw_bits_A[:bits]}(binary), {decimal_A}(decimal)")

    intro_3()
    st.write("> Example circuit(birth-day : 8/30)")
    circuit_example_B, raw_bits_B, decimal_B = q_rng_lotto_with_birthday(
        8, 30, bits=bits, upper_bound=u_bound,
    )
    st.pyplot(circuit_example_B)
    st.write(f"     Generated number : {raw_bits_B[:bits]}(binary), {decimal_B}(decimal)")

    intro_4()

elif lot_selection == "Custom":
    custom_doc()
    st.write("---")

    custom_n = st.number_input(
        "How many Q-random numbers you need?     (Min:1, Max:10)",
        step=1, min_value=1, max_value=10,
    )
    u_bound = st.number_input(
        "Choose the upper bound of your Q-random number   (Min:2, Max:9,000,000,000,000,000)",
        step=1, min_value=2, max_value=9000000000000000,
    )

    bits = bits_needed(u_bound)
    index_list = [f"num{i + 1}" for i in range(custom_n)]
    result = pd.DataFrame(index=index_list)

    mode = st.radio(
        "Select the Q-RNG lottery game mode",
        ("1) Simple Q-RNG", "2) Birth-day entangled Q-RNG"),
    )
    st.write("---")

    is_birthday = mode == "2) Birth-day entangled Q-RNG"

    month, day = None, None
    if is_birthday:
        st.subheader("2) Birth-day entangled Q-RNG")
        birth_day = st.date_input(
            "When's your birthday",
            datetime.datetime.today(),
            min_value=datetime.date(1879, 3, 14),  # Albert Einstein's birthday
            max_value=datetime.datetime.today(),
        )
        st.write("Your birthday is:", birth_day)
        month = birth_day.month
        day = birth_day.day
    else:
        st.subheader("1) Simple Q-RNG for Lottery Game")

    num_game = st.selectbox("How many games do you want?", (1, 2, 3, 4, 5))
    go = st.button("Q-Random Number Generation \U0001F448")

    if go:
        for i in range(num_game):
            if is_birthday:
                custom_num = get_rng_lotto_with_birthday(
                    month, day, n_get_num=custom_n, bits=bits, upper_bound=u_bound,
                )
            else:
                custom_num = get_rng_lotto(n_get_num=custom_n, bits=bits, upper_bound=u_bound)
            result[f"Q-lotto-{i + 1}"] = custom_num
        st.dataframe(data=result)

elif lot_selection in GAMES:
    render_game(GAMES[lot_selection])
