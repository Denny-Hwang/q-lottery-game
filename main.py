import streamlit as st
import pandas as pd
import numpy as np
import datetime

from q_function import random_number, q_rng_lotto, get_rng_lotto
from q_function import random_number_with_birthday, q_rng_lotto_with_birthday, get_rng_lotto_with_birthday

from intro_doc import intro_1, intro_2, intro_3, intro_4
from game_doc import lotto_doc, powerball_doc, lotto7_doc, lotto_India_doc, french_lottery_doc, custom_doc

st.sidebar.image("https://github.com/Denny-Hwang/q-lottery-game/blob/main/src/Q-Lottery-Game-logo-black.png?raw=true",
                 width=300)
#st.sidebar.title('Q-Lottery Game')
lot_selection = st.sidebar.selectbox(
                'Select the menu',
                ('About Q-Lottery Game',
                 'Lotto(Kor)',
                 'Powerball(USA)',
                 'Lotto India(India)',
                 'Lotto7(Japan)',
                 'French lottery(France)',
                 'Custom'))
st.sidebar.write('Selected : ', lot_selection)


################################### Intro #######################################################################
if lot_selection == 'About Q-Lottery Game':
    intro_1()

    intro_2()
    bits, u_bound = 6, 45
    st.write(f"> Example circuit ")
    circuit_example_A, raw_bits_A, decimal_A = q_rng_lotto(bits=bits, upper_bound=u_bound)
    st.pyplot(circuit_example_A)
    st.write(f"     Generated number : {raw_bits_A[:bits]}(binary), {decimal_A}(decimal)")

    intro_3()
    st.write(f"> Example circuit(birth-day : 8/30)")
    circuit_example_B, raw_bits_B, decimal_B = q_rng_lotto_with_birthday(8, 30, bits=bits, upper_bound=u_bound)
    st.pyplot(circuit_example_B)
    st.write(f"     Generated number : {raw_bits_B[:bits]}(binary), {decimal_B}(decimal)")

    intro_4()

################################### Lotto(Kor) #######################################################################
elif lot_selection == 'Lotto(Kor)':
    lotto_doc()
    st.write("---")

    bits, u_bound = 6, 45
    result = pd.DataFrame(index=['Num_1', 'Num_2', 'Num_3', 'Num_4', 'Num_5', 'Num_6'])

    mode = st.radio(
        "Select the Q-RNG lottery game mode",
        ('1) Simple Q-RNG',
         '2) Birth-day entangled Q-RNG')
    )

    st.write("---")

    if mode == '1) Simple Q-RNG':
        st.subheader('1) Simple Q-RNG for Lottery Game')

        num_game = st.selectbox(
            'How many games do you want?',
            ('1', '2', '3', '4', '5'))

        go = st.button("Q-Random Number Generation 👈")

        if go:
            if num_game == '1':
                for i in range(int(num_game)):
                    lotto_num = get_rng_lotto(n_get_num=6, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i+1}'] = lotto_num
                st.dataframe(data=result)
            elif num_game == '2':
                for i in range(int(num_game)):
                    lotto_num = get_rng_lotto(n_get_num=6, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i+1}'] = lotto_num
                st.dataframe(data=result)
            elif num_game == '3':
                for i in range(int(num_game)):
                    lotto_num = get_rng_lotto(n_get_num=6, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i+1}'] = lotto_num
                st.dataframe(data=result)
            elif num_game == '4':
                for i in range(int(num_game)):
                    lotto_num = get_rng_lotto(n_get_num=6, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i+1}'] = lotto_num
                st.dataframe(data=result)
            elif num_game == '5':
                for i in range(int(num_game)):
                    lotto_num = get_rng_lotto(n_get_num=6, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i+1}'] = lotto_num
                st.dataframe(data=result)

    else:
        st.subheader('2) Birth-day entangled Q-RNG')

        birth_day = st.date_input(
            "When's your birthday",             ## Erwin Schrodinger's birth day
            datetime.datetime.today(), min_value=datetime.date(1887, 8, 12), max_value=datetime.datetime.today())
        st.write('Your birthday is:', birth_day)

        month = birth_day.month
        day = birth_day.day

        num_game = st.selectbox(
            'How many games do you want?',
            ('1', '2', '3', '4', '5'))

        go = st.button("Q-Random Number Generation 👈")

        if go:
            if num_game == '1':
                for i in range(int(num_game)):
                    lotto_num = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i+1}'] = lotto_num
                st.dataframe(data=result)
            elif num_game == '2':
                for i in range(int(num_game)):
                    lotto_num = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i+1}'] = lotto_num
                st.dataframe(data=result)
            elif num_game == '3':
                for i in range(int(num_game)):
                    lotto_num = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i+1}'] = lotto_num
                st.dataframe(data=result)
            elif num_game == '4':
                for i in range(int(num_game)):
                    lotto_num = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i+1}'] = lotto_num
                st.dataframe(data=result)
            elif num_game == '5':
                for i in range(int(num_game)):
                    lotto_num = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i+1}'] = lotto_num
                st.dataframe(data=result)

################################### Powerball(USA) #####################################################################
elif lot_selection == 'Powerball(USA)':
    powerball_doc()
    st.write("---")

    white_ball_bits, w_u_bound = 7, 69
    power_ball_bits, p_u_bound = 6, 26
    result = pd.DataFrame(index=['W_ball_1', 'W_ball_2', 'W_ball_3', 'W_ball_4', 'W_ball_5', 'Power_ball'])

    mode = st.radio(
        "Select the Q-RNG lottery game mode",
        ('1) Simple Q-RNG',
         '2) Birth-day entangled Q-RNG')
    )

    st.write("---")

    if mode == '1) Simple Q-RNG':
        st.subheader('1) Simple Q-RNG for Lottery Game')

        num_game = st.selectbox(
            'How many games do you want?',
            ('1', '2', '3', '4', '5'))

        go = st.button("Q-Random Number Generation 👈")

        if go:
            if num_game == '1':
                for i in range(int(num_game)):
                    white_ball = get_rng_lotto(n_get_num=5, bits=white_ball_bits, upper_bound=w_u_bound)
                    _, _, power_ball = q_rng_lotto(bits=power_ball_bits, upper_bound=p_u_bound)
                    white_ball = np.append(white_ball, power_ball)
                    result[f'Q-powerball-{i+1}'] = white_ball
                st.dataframe(data=result)
            elif num_game == '2':
                for i in range(int(num_game)):
                    white_ball = get_rng_lotto(n_get_num=5, bits=white_ball_bits, upper_bound=w_u_bound)
                    _, _, power_ball = q_rng_lotto(bits=power_ball_bits, upper_bound=p_u_bound)
                    white_ball = np.append(white_ball, power_ball)
                    result[f'Q-powerball-{i + 1}'] = white_ball
                st.dataframe(data=result)
            elif num_game == '3':
                for i in range(int(num_game)):
                    white_ball = get_rng_lotto(n_get_num=5, bits=white_ball_bits, upper_bound=w_u_bound)
                    _, _, power_ball = q_rng_lotto(bits=power_ball_bits, upper_bound=p_u_bound)
                    white_ball = np.append(white_ball, power_ball)
                    result[f'Q-powerball-{i + 1}'] = white_ball
                st.dataframe(data=result)
            elif num_game == '4':
                for i in range(int(num_game)):
                    white_ball = get_rng_lotto(n_get_num=5, bits=white_ball_bits, upper_bound=w_u_bound)
                    _, _, power_ball = q_rng_lotto(bits=power_ball_bits, upper_bound=p_u_bound)
                    white_ball = np.append(white_ball, power_ball)
                    result[f'Q-powerball-{i + 1}'] = white_ball
                st.dataframe(data=result)
            elif num_game == '5':
                for i in range(int(num_game)):
                    white_ball = get_rng_lotto(n_get_num=5, bits=white_ball_bits, upper_bound=w_u_bound)
                    _, _, power_ball = q_rng_lotto(bits=power_ball_bits, upper_bound=p_u_bound)
                    white_ball = np.append(white_ball, power_ball)
                    result[f'Q-powerball-{i + 1}'] = white_ball
                st.dataframe(data=result)

    else:
        st.subheader('2) Birth-day entangled Q-RNG')

        birth_day = st.date_input(
            "When's your birthday",
            datetime.datetime.today(), min_value=datetime.date(1918, 5, 11),  ## Feynman's birth day
            max_value=datetime.datetime.today())
        st.write('Your birthday is:', birth_day)

        month = birth_day.month
        day = birth_day.day

        num_game = st.selectbox(
            'How many games do you want?',
            ('1', '2', '3', '4', '5'))

        go = st.button("Q-Random Number Generation 👈")

        if go:
            if num_game == '1':
                for i in range(int(num_game)):
                    white_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=white_ball_bits,
                                                             upper_bound=w_u_bound)
                    _, _, power_ball = q_rng_lotto_with_birthday(month, day, bits=power_ball_bits,
                                                                 upper_bound=p_u_bound)
                    white_ball = np.append(white_ball, power_ball)
                    result[f'Q-powerball-{i+1}'] = white_ball
                st.dataframe(data=result)
            elif num_game == '2':
                for i in range(int(num_game)):
                    white_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=white_ball_bits,
                                                             upper_bound=w_u_bound)
                    _, _, power_ball = q_rng_lotto_with_birthday(month, day, bits=power_ball_bits,
                                                                 upper_bound=p_u_bound)
                    white_ball = np.append(white_ball, power_ball)
                    result[f'Q-powerball-{i + 1}'] = white_ball
                st.dataframe(data=result)
            elif num_game == '3':
                for i in range(int(num_game)):
                    white_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=white_ball_bits,
                                                             upper_bound=w_u_bound)
                    _, _, power_ball = q_rng_lotto_with_birthday(month, day, bits=power_ball_bits,
                                                                 upper_bound=p_u_bound)
                    white_ball = np.append(white_ball, power_ball)
                    result[f'Q-powerball-{i + 1}'] = white_ball
                st.dataframe(data=result)
            elif num_game == '4':
                for i in range(int(num_game)):
                    white_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=white_ball_bits,
                                                             upper_bound=w_u_bound)
                    _, _, power_ball = q_rng_lotto_with_birthday(month, day, bits=power_ball_bits,
                                                                 upper_bound=p_u_bound)
                    white_ball = np.append(white_ball, power_ball)
                    result[f'Q-powerball-{i + 1}'] = white_ball
                st.dataframe(data=result)
            elif num_game == '5':
                for i in range(int(num_game)):
                    white_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=white_ball_bits,
                                                             upper_bound=w_u_bound)
                    _, _, power_ball = q_rng_lotto_with_birthday(month, day, bits=power_ball_bits,
                                                                 upper_bound=p_u_bound)
                    white_ball = np.append(white_ball, power_ball)
                    result[f'Q-powerball-{i + 1}'] = white_ball
                st.dataframe(data=result)

################################### Lotto India(India) #####################################################################
elif lot_selection == 'Lotto India(India)':
    lotto_India_doc()
    st.write("---")

    n_u_bound = 50
    j_u_bound = 5

    normal_ball_bits = 1
    while (2 ** normal_ball_bits <= n_u_bound):
        normal_ball_bits += 1
    joker_ball_bits = 1
    while (2 ** joker_ball_bits <= j_u_bound):
        joker_ball_bits += 1

    result = pd.DataFrame(index=['Ball_1', 'Ball_2', 'Ball_3', 'Ball_4', 'Ball_5', 'Ball_6', 'Joker_ball'])
    ball_name = 'Q-Lotto_India'

    mode = st.radio(
        "Select the Q-RNG lottery game mode",
        ('1) Simple Q-RNG',
         '2) Birth-day entangled Q-RNG')
    )

    st.write("---")

    if mode == '1) Simple Q-RNG':
        st.subheader('1) Simple Q-RNG for Lottery Game')

        num_game = st.selectbox(
            'How many games do you want?',
            ('1', '2', '3', '4', '5'))

        go = st.button("Q-Random Number Generation 👈")

        if go:
            if num_game == '1':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto(n_get_num=6, bits=normal_ball_bits, upper_bound=n_u_bound)
                    _, _, joker_ball = q_rng_lotto(bits=joker_ball_bits, upper_bound=j_u_bound)
                    normal_ball = np.append(normal_ball, joker_ball)
                    result[f'{ball_name}-{i+1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '2':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto(n_get_num=6, bits=normal_ball_bits, upper_bound=n_u_bound)
                    _, _, joker_ball = q_rng_lotto(bits=joker_ball_bits, upper_bound=j_u_bound)
                    normal_ball = np.append(normal_ball, joker_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '3':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto(n_get_num=6, bits=normal_ball_bits, upper_bound=n_u_bound)
                    _, _, joker_ball = q_rng_lotto(bits=joker_ball_bits, upper_bound=j_u_bound)
                    normal_ball = np.append(normal_ball, joker_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '4':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto(n_get_num=6, bits=normal_ball_bits, upper_bound=n_u_bound)
                    _, _, joker_ball = q_rng_lotto(bits=joker_ball_bits, upper_bound=j_u_bound)
                    normal_ball = np.append(normal_ball, joker_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '5':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto(n_get_num=6, bits=normal_ball_bits, upper_bound=n_u_bound)
                    _, _, joker_ball = q_rng_lotto(bits=joker_ball_bits, upper_bound=j_u_bound)
                    normal_ball = np.append(normal_ball, joker_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)

    else:
        st.subheader('2) Birth-day entangled Q-RNG')

        birth_day = st.date_input(
            "When's your birthday",
            datetime.datetime.today(), min_value=datetime.date(1918, 5, 11),  ## Feynman's birth day
            max_value=datetime.datetime.today())
        st.write('Your birthday is:', birth_day)

        month = birth_day.month
        day = birth_day.day

        num_game = st.selectbox(
            'How many games do you want?',
            ('1', '2', '3', '4', '5'))

        go = st.button("Q-Random Number Generation 👈")

        if go:
            if num_game == '1':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=normal_ball_bits,
                                                              upper_bound=n_u_bound)
                    _, _, joker_ball = q_rng_lotto_with_birthday(month, day, bits=joker_ball_bits,
                                                                 upper_bound=j_u_bound)
                    normal_ball = np.append(normal_ball, joker_ball)
                    result[f'{ball_name}-{i+1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '2':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=normal_ball_bits,
                                                              upper_bound=n_u_bound)
                    _, _, joker_ball = q_rng_lotto_with_birthday(month, day, bits=joker_ball_bits,
                                                                 upper_bound=j_u_bound)
                    normal_ball = np.append(normal_ball, joker_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '3':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=normal_ball_bits,
                                                              upper_bound=n_u_bound)
                    _, _, joker_ball = q_rng_lotto_with_birthday(month, day, bits=joker_ball_bits,
                                                                 upper_bound=j_u_bound)
                    normal_ball = np.append(normal_ball, joker_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '4':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=normal_ball_bits,
                                                              upper_bound=n_u_bound)
                    _, _, joker_ball = q_rng_lotto_with_birthday(month, day, bits=joker_ball_bits,
                                                                 upper_bound=j_u_bound)
                    normal_ball = np.append(normal_ball, joker_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '5':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=normal_ball_bits,
                                                              upper_bound=n_u_bound)
                    _, _, joker_ball = q_rng_lotto_with_birthday(month, day, bits=joker_ball_bits,
                                                                 upper_bound=j_u_bound)
                    normal_ball = np.append(normal_ball, joker_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)

################################### Lotto7(Japan) #######################################################################
elif lot_selection == 'Lotto7(Japan)':
    lotto7_doc()
    st.write("---")

    u_bound = 37

    bits = 1
    while (2 ** bits <= u_bound):
        bits += 1


    result = pd.DataFrame(index=['Num_1', 'Num_2', 'Num_3', 'Num_4', 'Num_5', 'Num_6', 'Num_7'])
    ball_name = 'Q-lotto7'

    mode = st.radio(
        "Select the Q-RNG lottery game mode",
        ('1) Simple Q-RNG',
         '2) Birth-day entangled Q-RNG')
    )

    st.write("---")

    if mode == '1) Simple Q-RNG':
        st.subheader('1) Simple Q-RNG for Lottery Game')

        num_game = st.selectbox(
            'How many games do you want?',
            ('1', '2', '3', '4', '5'))

        go = st.button("Q-Random Number Generation 👈")

        if go:
            if num_game == '1':
                for i in range(int(num_game)):
                    lotto7_num = get_rng_lotto(n_get_num=7, bits=bits, upper_bound=u_bound)
                    result[f'{ball_name} game-{i+1}'] = lotto7_num
                st.dataframe(data=result)
            elif num_game == '2':
                for i in range(int(num_game)):
                    lotto7_num = get_rng_lotto(n_get_num=7, bits=bits, upper_bound=u_bound)
                    result[f'{ball_name} game-{i + 1}'] = lotto7_num
                st.dataframe(data=result)
            elif num_game == '3':
                for i in range(int(num_game)):
                    lotto7_num = get_rng_lotto(n_get_num=7, bits=bits, upper_bound=u_bound)
                    result[f'{ball_name} game-{i + 1}'] = lotto7_num
                st.dataframe(data=result)
            elif num_game == '4':
                for i in range(int(num_game)):
                    lotto7_num = get_rng_lotto(n_get_num=7, bits=bits, upper_bound=u_bound)
                    result[f'{ball_name} game-{i + 1}'] = lotto7_num
                st.dataframe(data=result)
            elif num_game == '5':
                for i in range(int(num_game)):
                    lotto7_num = get_rng_lotto(n_get_num=7, bits=bits, upper_bound=u_bound)
                    result[f'{ball_name} game-{i + 1}'] = lotto7_num
                st.dataframe(data=result)

    else:
        st.subheader('2) Birth-day entangled Q-RNG')

        birth_day = st.date_input(
            "When's your birthday",           ## Erwin Schrodinger's birth day
            datetime.datetime.today(), min_value=datetime.date(1887, 8, 12), max_value=datetime.datetime.today())
        st.write('Your birthday is:', birth_day)

        month = birth_day.month
        day = birth_day.day

        num_game = st.selectbox(
            'How many games do you want?',
            ('1', '2', '3', '4', '5'))

        go = st.button("Q-Random Number Generation 👈")

        if go:
            if num_game == '1':
                for i in range(int(num_game)):
                    lotto7_num = get_rng_lotto_with_birthday(month, day, n_get_num=7, bits=bits, upper_bound=u_bound)
                    result[f'{ball_name} game-{i + 1}'] = lotto7_num
                st.dataframe(data=result)
            elif num_game == '2':
                for i in range(int(num_game)):
                    lotto7_num = get_rng_lotto_with_birthday(month, day, n_get_num=7, bits=bits, upper_bound=u_bound)
                    result[f'{ball_name} game-{i + 1}'] = lotto7_num
                st.dataframe(data=result)
            elif num_game == '3':
                for i in range(int(num_game)):
                    lotto7_num = get_rng_lotto_with_birthday(month, day, n_get_num=7, bits=bits, upper_bound=u_bound)
                    result[f'{ball_name} game-{i + 1}'] = lotto7_num
                st.dataframe(data=result)
            elif num_game == '4':
                for i in range(int(num_game)):
                    lotto7_num = get_rng_lotto_with_birthday(month, day, n_get_num=7, bits=bits, upper_bound=u_bound)
                    result[f'{ball_name} game-{i + 1}'] = lotto7_num
                st.dataframe(data=result)
            elif num_game == '5':
                for i in range(int(num_game)):
                    lotto7_num = get_rng_lotto_with_birthday(month, day, n_get_num=7, bits=bits, upper_bound=u_bound)
                    result[f'{ball_name} game-{i + 1}'] = lotto7_num
                st.dataframe(data=result)

################################### French lottery(France) #####################################################################
elif lot_selection == 'French lottery(France)':
    french_lottery_doc()
    st.write("---")

    n_u_bound = 49
    l_u_bound = 10

    normal_ball_bits = 1
    while (2 ** normal_ball_bits <= n_u_bound):
        normal_ball_bits += 1
    lucky_ball_bits = 1
    while (2 ** lucky_ball_bits <= l_u_bound):
        lucky_ball_bits += 1


    result = pd.DataFrame(index=['Ball_1', 'Ball_2', 'Ball_3', 'Ball_4', 'Ball_5', 'Lucky_Number'])
    ball_name = 'Q-French_lottery'

    mode = st.radio(
        "Select the Q-RNG lottery game mode",
        ('1) Simple Q-RNG',
         '2) Birth-day entangled Q-RNG')
    )

    st.write("---")

    if mode == '1) Simple Q-RNG':
        st.subheader('1) Simple Q-RNG for Lottery Game')

        num_game = st.selectbox(
            'How many games do you want?',
            ('1', '2', '3', '4', '5'))

        go = st.button("Q-Random Number Generation 👈")

        if go:
            if num_game == '1':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto(n_get_num=5, bits=normal_ball_bits, upper_bound=n_u_bound)
                    _, _, lucky_ball = q_rng_lotto(bits=lucky_ball_bits, upper_bound=l_u_bound)
                    normal_ball = np.append(normal_ball, lucky_ball)
                    result[f'{ball_name}-{i+1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '2':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto(n_get_num=5, bits=normal_ball_bits, upper_bound=n_u_bound)
                    _, _, lucky_ball = q_rng_lotto(bits=lucky_ball_bits, upper_bound=l_u_bound)
                    normal_ball = np.append(normal_ball, lucky_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '3':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto(n_get_num=5, bits=normal_ball_bits, upper_bound=n_u_bound)
                    _, _, lucky_ball = q_rng_lotto(bits=lucky_ball_bits, upper_bound=l_u_bound)
                    normal_ball = np.append(normal_ball, lucky_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '4':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto(n_get_num=5, bits=normal_ball_bits, upper_bound=n_u_bound)
                    _, _, lucky_ball = q_rng_lotto(bits=lucky_ball_bits, upper_bound=l_u_bound)
                    normal_ball = np.append(normal_ball, lucky_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '5':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto(n_get_num=5, bits=normal_ball_bits, upper_bound=n_u_bound)
                    _, _, lucky_ball = q_rng_lotto(bits=lucky_ball_bits, upper_bound=l_u_bound)
                    normal_ball = np.append(normal_ball, lucky_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)

    else:
        st.subheader('2) Birth-day entangled Q-RNG')

        birth_day = st.date_input(
            "When's your birthday",
            datetime.datetime.today(), min_value=datetime.date(1918, 5, 11),  ## Feynman's birth day
            max_value=datetime.datetime.today())
        st.write('Your birthday is:', birth_day)

        month = birth_day.month
        day = birth_day.day

        num_game = st.selectbox(
            'How many games do you want?',
            ('1', '2', '3', '4', '5'))

        go = st.button("Q-Random Number Generation 👈")

        if go:
            if num_game == '1':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=normal_ball_bits,
                                                              upper_bound=n_u_bound)
                    _, _, lucky_ball = q_rng_lotto(bits=lucky_ball_bits, upper_bound=l_u_bound)
                    normal_ball = np.append(normal_ball, lucky_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '2':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=normal_ball_bits,
                                                              upper_bound=n_u_bound)
                    _, _, lucky_ball = q_rng_lotto(bits=lucky_ball_bits, upper_bound=l_u_bound)
                    normal_ball = np.append(normal_ball, lucky_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '3':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=normal_ball_bits,
                                                              upper_bound=n_u_bound)
                    _, _, lucky_ball = q_rng_lotto(bits=lucky_ball_bits, upper_bound=l_u_bound)
                    normal_ball = np.append(normal_ball, lucky_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '4':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=normal_ball_bits,
                                                              upper_bound=n_u_bound)
                    _, _, lucky_ball = q_rng_lotto(bits=lucky_ball_bits, upper_bound=l_u_bound)
                    normal_ball = np.append(normal_ball, lucky_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)
            elif num_game == '5':
                for i in range(int(num_game)):
                    normal_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=normal_ball_bits,
                                                              upper_bound=n_u_bound)
                    _, _, lucky_ball = q_rng_lotto(bits=lucky_ball_bits, upper_bound=l_u_bound)
                    normal_ball = np.append(normal_ball, lucky_ball)
                    result[f'{ball_name}-{i + 1}'] = normal_ball
                st.dataframe(data=result)

################################### Custom #####################################################################
elif lot_selection == 'Custom':
    custom_doc()
    st.write("---")

    custom_n = st.number_input('How many Q-random numbers you need?     '  
                               '(Min:1, Max:10)', step=1, min_value=1, max_value=10)
    u_bound = st.number_input('Choose the upper bound of your Q-random number   '
                              '(Min:2, Max:9,000,000,000,000,000)', step=1, min_value=2, max_value=9000000000000000)

    bits = 1
    while 2**bits <= u_bound:
        bits += 1
    print(f"bits : {bits}")

    index_list=[]
    for i in range(np.int(custom_n)):
        index_list.append(f"num{i+1}")
    result = pd.DataFrame(index=index_list)
    print(index_list)

    mode = st.radio(
        "Select the Q-RNG lottery game mode",
        ('1) Simple Q-RNG',
         '2) Birth-day entangled Q-RNG')
    )

    st.write("---")

    if mode == '1) Simple Q-RNG':
        st.subheader('1) Simple Q-RNG for Lottery Game')

        num_game = st.selectbox(
            'How many games do you want?',
            ('1', '2', '3', '4', '5'))

        go = st.button("Q-Random Number Generation 👈")

        if go:
            if num_game == '1':
                for i in range(int(num_game)):
                    custom_num = get_rng_lotto(n_get_num=custom_n, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i + 1}'] = custom_num
                st.dataframe(data=result)
            elif num_game == '2':
                for i in range(int(num_game)):
                    custom_num = get_rng_lotto(n_get_num=custom_n, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i + 1}'] = custom_num
                st.dataframe(data=result)
            elif num_game == '3':
                for i in range(int(num_game)):
                    custom_num = get_rng_lotto(n_get_num=custom_n, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i + 1}'] = custom_num
                st.dataframe(data=result)
            elif num_game == '4':
                for i in range(int(num_game)):
                    custom_num = get_rng_lotto(n_get_num=custom_n, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i + 1}'] = custom_num
                st.dataframe(data=result)
            elif num_game == '5':
                for i in range(int(num_game)):
                    custom_num = get_rng_lotto(n_get_num=custom_n, bits=bits, upper_bound=u_bound)
                    result[f'Q-lotto-{i + 1}'] = custom_num
                st.dataframe(data=result)

    else:
        st.subheader('2) Birth-day entangled Q-RNG')

        birth_day = st.date_input(
            "When's your birthday",
            datetime.datetime.today(), min_value=datetime.date(1879, 3, 14),  ## Albert Einstein's birth day
            max_value=datetime.datetime.today())
        st.write('Your birthday is:', birth_day)

        month = birth_day.month
        day = birth_day.day

        num_game = st.selectbox(
            'How many games do you want?',
            ('1', '2', '3', '4', '5'))

        go = st.button("Q-Random Number Generation 👈")

        if go:
            if num_game == '1':
                for i in range(int(num_game)):
                    custom_num = get_rng_lotto_with_birthday(month, day, n_get_num=custom_n, bits=bits,
                                                             upper_bound=u_bound)
                    result[f'Q-lotto-{i + 1}'] = custom_num
                st.dataframe(data=result)
            elif num_game == '2':
                for i in range(int(num_game)):
                    custom_num = get_rng_lotto_with_birthday(month, day, n_get_num=custom_n, bits=bits,
                                                             upper_bound=u_bound)
                    result[f'Q-lotto-{i + 1}'] = custom_num
                st.dataframe(data=result)
            elif num_game == '3':
                for i in range(int(num_game)):
                    custom_num = get_rng_lotto_with_birthday(month, day, n_get_num=custom_n, bits=bits,
                                                             upper_bound=u_bound)
                    result[f'Q-lotto-{i + 1}'] = custom_num
                st.dataframe(data=result)
            elif num_game == '4':
                for i in range(int(num_game)):
                    custom_num = get_rng_lotto_with_birthday(month, day, n_get_num=custom_n, bits=bits,
                                                             upper_bound=u_bound)
                    result[f'Q-lotto-{i + 1}'] = custom_num
                st.dataframe(data=result)
            elif num_game == '5':
                for i in range(int(num_game)):
                    custom_num = get_rng_lotto_with_birthday(month, day, n_get_num=custom_n, bits=bits,
                                                             upper_bound=u_bound)
                    result[f'Q-lotto-{i + 1}'] = custom_num
                st.dataframe(data=result)
