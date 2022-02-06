import streamlit as st
import numpy as np
import pandas as pd
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import Aer, execute
from tqdm import tqdm


def random_number(bits=6):
    qr = QuantumRegister(bits)
    cr = ClassicalRegister(bits)
    circuit = QuantumCircuit(qr,cr)
    circuit.h(qr)

    circuit.measure_all()

    backend = Aer.get_backend('qasm_simulator')
    result = execute(circuit, backend, shots=1, memory=True).result()
    counts = result.get_memory()
    num = counts[0].split(" ")[0]

    return counts[0], int(num, 2)

def q_rng_lotto(bits=6, upper_bound=45):
    raw_bits, decimal = random_number(bits=bits)

    while (decimal == 0 | decimal > upper_bound):
        raw_bits, decimal = random_number(bits=bits)

    return raw_bits, decimal


def get_rng_lotto(n_get_num = 6, bits=6, upper_bound=45):
    lotto = []
    for i in tqdm(range(n_get_num)):
        _, decimal = q_rng_lotto(bits=bits, upper_bound=upper_bound)

        # 이미 뽑은 숫자가 다시 나올 경우 새로 뽑기
        while (np.isin(decimal, lotto) == 1):
            _, decimal = q_rng_lotto(bits=bits, upper_bound=upper_bound)

        lotto.append(decimal)
        lotto.sort()

    return lotto


def intro():
    st.title("Q-lottery")

    st.write(
        """
        Let's generate real random number using IBM qiskit
        bla bla~
        """)

def lotto_doc():
    st.write("")
    st.subheader("Korean lottery *Lotto 6/45*")
    st.write(
        """
        In the **Lotto 6/45**, you can choose six numbers in the 1~45 range
        """)

def powerball_doc():
    st.write("")
    st.subheader("USA lottery *Power ball*")
    st.write(
        """
        In the **Power ball**, you can choose five *white ball* in the 1~69 range and select one *power ball* in the 1~26 range
        """)


def main():

    intro()

    lot_selection = st.sidebar.selectbox(
                    'Select lottery game',
                    ('Lotto(Kor)', 'Powerball(USA)'))
    st.sidebar.write('Selected game : ', lot_selection)

    if (lot_selection=='Lotto(Kor)'):
        lotto_doc()

        bits, u_bound = 6, 45
        lotto_num = get_rng_lotto(n_get_num=6, bits=bits, upper_bound=u_bound)
        column_name = ['Num_1', 'Num_2', 'Num_3', 'Num_4', 'Num_5', 'Num_6']
        result = pd.DataFrame({'Q-lotto number': lotto_num}, index=column_name)

    elif(lot_selection=='Powerball(USA)'):
        powerball_doc()

        white_ball_bits, w_u_bound = 7, 69
        white_ball = get_rng_lotto(n_get_num=5, bits=white_ball_bits, upper_bound=w_u_bound)

        power_ball_bits, p_u_bound = 6, 26
        _, power_ball = q_rng_lotto(bits=power_ball_bits, upper_bound=p_u_bound)

        result_num = np.append(white_ball, power_ball)
        column_name = ['W1', 'W2', 'W3', 'W4', 'W5', 'Power_ball']

        result = pd.DataFrame({'Q-powerball': result_num}, index=column_name)

    st.dataframe(data=result.T)

main()