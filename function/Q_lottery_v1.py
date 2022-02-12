import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import Aer, execute
from qiskit.visualization import *
from tqdm import tqdm
import datetime

def random_number(bits=6):
    qr = QuantumRegister(bits, 'qubit')
    cr = ClassicalRegister(bits, 'c_bit')
    circuit = QuantumCircuit(qr,cr)
    circuit.reset(range(bits))
    circuit.h(qr)

    circuit.measure_all()

    backend = Aer.get_backend('qasm_simulator')
    result = execute(circuit, backend, shots=1, memory=True).result()
    counts = result.get_memory()
    num = counts[0].split(" ")[0]
    circuit_fig = circuit_drawer(circuit, output='mpl',
                                 scale=1, vertical_compression='high',
                                 style={'backgroundcolor': '#EEEEEE'})

    return circuit_fig, counts[0], int(num, 2)

def random_number_with_birthday(month, day, bits=6):
    qr = QuantumRegister(bits, 'qubit')
    q_birth = QuantumRegister(1, 'q-month')
    q_day = QuantumRegister(1, 'q-day')
    cr = ClassicalRegister(bits)

    circuit = QuantumCircuit(qr, q_birth, q_day, cr)
    circuit.reset(range(bits + 2))
    circuit.h(qr)

    ## birth-day initialization
    month_init = month / 12
    day_30 = [4, 6, 9, 11]
    if month == 2:
        if day == 29:
            day_init = day / 29
        else:
            day_init = day / 28
    elif np.isin(month, day_30):
        day_init = day / 30
    else:
        day_init = day / 31

    print(month_init, day_init)
    circuit.rx(month_init, bits)
    circuit.rx(day_init, bits + 1)

    circuit.barrier()

    circuit.cx(bits, month % bits)
    circuit.cx(bits + 1, day % bits)

    circuit.barrier()

    circuit.measure(qr, cr)

    backend = Aer.get_backend('qasm_simulator')
    result = execute(circuit, backend, shots=1, memory=True).result()
    counts = result.get_memory()
    num = counts[0].split(" ")[0]
    circuit_fig = circuit_drawer(circuit, output='mpl',
                                 scale=1, vertical_compression='high',
                                 style={'backgroundcolor': '#EEEEEE'})

    return circuit_fig, counts[0], int(num, 2)

def q_rng_lotto(bits=6, upper_bound=45):
    circuit_fig, raw_bits, decimal = random_number(bits=bits)

    while ((decimal==0) | (decimal > upper_bound)):
        circuit_fig, raw_bits, decimal = random_number(bits=bits)

    return circuit_fig, raw_bits, decimal

def q_rng_lotto_with_birthday(month, day, bits=6, upper_bound=45):
    circuit_fig, raw_bits, decimal = random_number_with_birthday(month, day, bits=bits)

    while ((decimal == 0) | (decimal > upper_bound)):
        circuit_fig, raw_bits, decimal = random_number_with_birthday(month, day, bits=bits)

    return circuit_fig, raw_bits, decimal

def get_rng_lotto(n_get_num = 6, bits=6, upper_bound=45):
    lotto = []
    for i in tqdm(range(n_get_num)):
        _, _, decimal = q_rng_lotto(bits=bits, upper_bound=upper_bound)

        # If the generated number is already in the list, regenerate the number to avoid duplication.
        while (np.isin(decimal, lotto) == 1):
            _, _, decimal = q_rng_lotto(bits=bits, upper_bound=upper_bound)

        lotto.append(decimal)
        lotto.sort()

    return lotto

def get_rng_lotto_with_birthday(month, day, n_get_num = 6, bits=6, upper_bound=45):
    lotto = []
    for i in tqdm(range(n_get_num)):
        _, _, decimal = q_rng_lotto_with_birthday(month, day, bits=bits, upper_bound=upper_bound)

        # If the generated number is already in the list, regenerate the number to avoid duplication.
        while (np.isin(decimal, lotto) == 1):
            _, _, decimal = q_rng_lotto_with_birthday(month, day, bits=bits, upper_bound=upper_bound)

        lotto.append(decimal)
        lotto.sort()

    return lotto


def intro_1():
    st.title("Quantum Lottery Game")
    st.write(
        """
        ### 1) Let's generate *real random number* using IBM Quantum Computer

        - Real random number generation for lottery-game using IBM quantum computer  
        **[IBM Qiskit library](https://qiskit.org/)**
        
        ---
            
        ### 2) What is *real* random number generation?
        
        - "**Random number generation(RNG)** is a sequence of numbers or symbols that cannot be reasonably predicted better than by random chance is generated. 
        This means that the particular outcome sequence will contain some patterns detectable in hindsight but **unpredictable** to foresight"(Wikipedia)   
             
        - There are two method for [RNG](https://en.wikipedia.org/wiki/Random_number_generation)
        
            - **"True" random number generation(TRNG)** uses measurement of some physical phenomenon that is expected to be random and then compensates 
            for possible biases in the measurement process
            
            - **"Pseudo" random number generation(PRNG)** uses computational algorithm that can produce long sequences of apparently random results, 
            which are in fact completely determined by a shorter initial value, known as a seed value or key
        
  
        - In this application, we use IBM cloud quantum computer to generate real random number using the **superpositon** of the qubit states. 
        - There are some way for generating random number using **[Qiskit(Quantum Information Software Kit)](https://qiskit.org/)**
        
        -  1) **Qiskit RNG**
            - It needed IBM Quantum account for IBM Quantum backends. So, skip this method for this application.
            If you want to use this library, check this links below  
                - https://qiskit.org/documentation/apidoc/ibmq_random.html  
                - https://github.com/qiskit-community/qiskit_rng/
        -  2) **Qauntum circuit** based random number generation. **[IBM Quantum system](https://quantum-computing.ibm.com/services/docs/services/manage/systems/)** services cryogenic based quantum processor
            - Using this cloud based quantum computer, we could make quantum circuit for specific operation
            - In this application we use the "**[H(Hadamard) gate](https://learn.qiskit.org/course/ch-states/single-qubit-gates#hgate)**" for 
            **"[superposition](https://en.wikipedia.org/wiki/Quantum_superposition)"** and "**[CNOT gate](https://qiskit.org/textbook/ch-gates/multiple-qubits-entangled-states.html#cnot)**" for **"[entanglement](https://en.wikipedia.org/wiki/Quantum_entanglement)"** between the qubits  
                * Superposition state of the single qubit has 50/50 measurement probability of |0⟩/|1⟩ state  
                * Entanglement 
                Actually, because of the RNG generation time and IBM Q account problem, we didn't used 'Real' device. 
            
        (Under construction!!, Insert bloch sphere here!)  
            
        """)

def intro_2():
    st.write(
        """
        ---
        ### 3) There are two mode for random number generation
        
        #### A) Simple random number generation using quantum circuit using qiskit library
        """)

def intro_3():
    st.write(
        """
        #### B) Birth-day entangled random number generation
        
            - Add two qubit for entanglement
            - Applying user's birth-day to initial probability of the qubits
            - Add CNOT gate on birth-day qubit and RNG qubit
            - Your birth-day will change the 50/50 probability of some qubits to another random value 
            
        """)
def intro_4():
    st.write(
        """ 
        ---                 
        ### 4) Serviced Lottery Game
    
        - **[Lotto(Korea)](https://dhlottery.co.kr/)**
    
          : Select 6 numbers in range 45
    
        - **[Powerball(USA)](https://www.powerball.com/)**
    
          : Select 5 numbers in range 70 for 'white ball', 1 more selection in range 25 for 'power ball'
    
    
        ---
        ### 5) Caution!!
    
            - Although real random number generated by QC is more random than pseudo random number, 
              it does not guarantee winning of the lottery!! 
            - Just use it for fun!
          
        ---  
        ### 6) Contribution
    
        - If you want to add another "Lottery game", follow the form and send PR to **[github](https://github.com/Denny-Hwang/q-lottery-game)**  
        (Under construction!)
        """)

def lotto_doc():
    st.image("https://www.dhlottery.co.kr/images/company/img_bi_intro_logo1.png", width=300)
    st.title("Korean lottery - *Lotto 6/45*")
    st.write(
        """
        In the **Lotto 6/45**, you can choose six numbers in the 1~45 range
        """)

def powerball_doc():
    st.image("https://s3.amazonaws.com/cdn.powerball.com/drupal/files/2020-02/Powerball%20%2B%20PP%20Horizontal-Flat-Color.jpg", width=400)
    st.title("USA lottery - *Power ball*")

    st.write(
        """       
        In the **Power ball**, you can choose five *white ball* in the 1~69 range and select one *power ball* in the 1~26 range
        """)

def custom_doc():

    st.title("Custom Q-Lottery Game")

    st.write(
        """       
        Customize your Q-Lottery Game
        
        """)

def main():
    st.sidebar.image("https://www.ibm.com/quantum-computing/_nuxt/img/7156eb7.png", width=300)
    st.sidebar.write(" *Ref : https://www.ibm.com* ")
    st.sidebar.title('Q-Lottery Game')
    lot_selection = st.sidebar.selectbox(
                    'Select the menu',
                    ('About Q-Lottery Game',
                     'Lotto(Kor)',
                     'Powerball(USA)',
                     'Custom'))
    st.sidebar.write('Selected : ', lot_selection)


################################### Intro #######################################################################
    if lot_selection=='About Q-Lottery Game':
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
    elif lot_selection=='Lotto(Kor)':
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
                        result[f'Q-lotto game-{i+1}'] = lotto_num
                    st.dataframe(data=result.T)
                elif num_game == '2':
                    for i in range(int(num_game)):
                        lotto_num = get_rng_lotto(n_get_num=6, bits=bits, upper_bound=u_bound)
                        result[f'Q-lotto game-{i+1}'] = lotto_num
                    st.dataframe(data=result.T)
                elif num_game == '3':
                    for i in range(int(num_game)):
                        lotto_num = get_rng_lotto(n_get_num=6, bits=bits, upper_bound=u_bound)
                        result[f'Q-lotto game-{i+1}'] = lotto_num
                    st.dataframe(data=result.T)
                elif num_game == '4':
                    for i in range(int(num_game)):
                        lotto_num = get_rng_lotto(n_get_num=6, bits=bits, upper_bound=u_bound)
                        result[f'Q-lotto game-{i+1}'] = lotto_num
                    st.dataframe(data=result.T)
                elif num_game == '5':
                    for i in range(int(num_game)):
                        lotto_num = get_rng_lotto(n_get_num=6, bits=bits, upper_bound=u_bound)
                        result[f'Q-lotto-{i+1}'] = lotto_num
                    st.dataframe(data=result.T)

        else:
            st.subheader('2) Birth-day entangled Q-RNG')

            birth_day = st.date_input(
                "When's your birthday",
                datetime.datetime.today(), min_value=datetime.date(1887, 8, 12),   ## Erwin Schrodinger's birth day
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
                        lotto_num = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=bits, upper_bound=u_bound)
                        result[f'Q-lotto game-{i+1}'] = lotto_num
                    st.dataframe(data=result.T)
                elif num_game == '2':
                    for i in range(int(num_game)):
                        lotto_num = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=bits, upper_bound=u_bound)
                        result[f'Q-lotto game-{i+1}'] = lotto_num
                    st.dataframe(data=result.T)
                elif num_game == '3':
                    for i in range(int(num_game)):
                        lotto_num = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=bits, upper_bound=u_bound)
                        result[f'Q-lotto game-{i+1}'] = lotto_num
                    st.dataframe(data=result.T)
                elif num_game == '4':
                    for i in range(int(num_game)):
                        lotto_num = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=bits, upper_bound=u_bound)
                        result[f'Q-lotto game-{i+1}'] = lotto_num
                    st.dataframe(data=result.T)
                elif num_game == '5':
                    for i in range(int(num_game)):
                        lotto_num = get_rng_lotto_with_birthday(month, day, n_get_num=6, bits=bits, upper_bound=u_bound)
                        result[f'Q-lotto-{i+1}'] = lotto_num
                    st.dataframe(data=result.T)

################################### Powerball(USA) #####################################################################
    elif lot_selection=='Powerball(USA)':
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
                        powerball_num = np.append(white_ball, power_ball)
                        result[f'Q-powerball-{i+1}'] = powerball_num
                    st.dataframe(data=result.T)
                elif num_game == '2':
                    for i in range(int(num_game)):
                        white_ball = get_rng_lotto(n_get_num=5, bits=white_ball_bits, upper_bound=w_u_bound)
                        _, _, power_ball = q_rng_lotto(bits=power_ball_bits, upper_bound=p_u_bound)
                        powerball_num = np.append(white_ball, power_ball)
                        result[f'Q-powerball-{i+1}'] = powerball_num
                    st.dataframe(data=result.T)
                elif num_game == '3':
                    for i in range(int(num_game)):
                        white_ball = get_rng_lotto(n_get_num=5, bits=white_ball_bits, upper_bound=w_u_bound)
                        _, _, power_ball = q_rng_lotto(bits=power_ball_bits, upper_bound=p_u_bound)
                        powerball_num = np.append(white_ball, power_ball)
                        result[f'Q-powerball-{i+1}'] = powerball_num
                    st.dataframe(data=result.T)
                elif num_game == '4':
                    for i in range(int(num_game)):
                        white_ball = get_rng_lotto(n_get_num=5, bits=white_ball_bits, upper_bound=w_u_bound)
                        _, _, power_ball = q_rng_lotto(bits=power_ball_bits, upper_bound=p_u_bound)
                        powerball_num = np.append(white_ball, power_ball)
                        result[f'Q-powerball-{i+1}'] = powerball_num
                    st.dataframe(data=result.T)
                elif num_game == '5':
                    for i in range(int(num_game)):
                        white_ball = get_rng_lotto(n_get_num=5, bits=white_ball_bits, upper_bound=w_u_bound)
                        _, _, power_ball = q_rng_lotto(bits=power_ball_bits, upper_bound=p_u_bound)
                        powerball_num = np.append(white_ball, power_ball)
                        result[f'Q-powerball-{i+1}'] = powerball_num
                    st.dataframe(data=result.T)

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
                        powerball_num = np.append(white_ball, power_ball)
                        result[f'Q-powerball-{i+1}'] = powerball_num
                    st.dataframe(data=result.T)
                elif num_game == '2':
                    for i in range(int(num_game)):
                        white_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=white_ball_bits,
                                                                 upper_bound=w_u_bound)
                        _, _, power_ball = q_rng_lotto_with_birthday(month, day, bits=power_ball_bits,
                                                                     upper_bound=p_u_bound)
                        powerball_num = np.append(white_ball, power_ball)
                        result[f'Q-powerball-{i+1}'] = powerball_num
                    st.dataframe(data=result.T)
                elif num_game == '3':
                    for i in range(int(num_game)):
                        white_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=white_ball_bits,
                                                                 upper_bound=w_u_bound)
                        _, _, power_ball = q_rng_lotto_with_birthday(month, day, bits=power_ball_bits,
                                                                     upper_bound=p_u_bound)
                        powerball_num = np.append(white_ball, power_ball)
                        result[f'Q-powerball-{i+1}'] = powerball_num
                    st.dataframe(data=result.T)
                elif num_game == '4':
                    for i in range(int(num_game)):
                        white_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=white_ball_bits,
                                                                 upper_bound=w_u_bound)
                        _, _, power_ball = q_rng_lotto_with_birthday(month, day, bits=power_ball_bits,
                                                                     upper_bound=p_u_bound)
                        powerball_num = np.append(white_ball, power_ball)
                        result[f'Q-powerball-{i+1}'] = powerball_num
                    st.dataframe(data=result.T)
                elif num_game == '5':
                    for i in range(int(num_game)):
                        white_ball = get_rng_lotto_with_birthday(month, day, n_get_num=5, bits=white_ball_bits,
                                                                 upper_bound=w_u_bound)
                        _, _, power_ball = q_rng_lotto_with_birthday(month, day, bits=power_ball_bits,
                                                                     upper_bound=p_u_bound)
                        powerball_num = np.append(white_ball, power_ball)
                        result[f'Q-powerball-{i+1}'] = powerball_num
                    st.dataframe(data=result.T)

################################### Custom #####################################################################
    elif lot_selection=='Custom':
        custom_doc()
        st.write("---")

        custom_n = st.number_input('How many Q-random numbers you need?     '  
                                   '(Min:1, Max:10)', step=1, min_value=1, max_value=10)
        u_bound = st.number_input('Choose the upper bound of your Q-random number   '
                                  '(Min:2, Max:9,000,000,000,000,000)', step=1, min_value=2, max_value=9000000000000000)

        bits=1
        while(2**bits <= u_bound):
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
                        result[f'Q-lotto game-{i + 1}'] = custom_num
                    st.dataframe(data=result.T)
                elif num_game == '2':
                    for i in range(int(num_game)):
                        custom_num = get_rng_lotto(n_get_num=custom_n, bits=bits, upper_bound=u_bound)
                        result[f'Q-lotto game-{i + 1}'] = custom_num
                    st.dataframe(data=result.T)
                elif num_game == '3':
                    for i in range(int(num_game)):
                        custom_num = get_rng_lotto(n_get_num=custom_n, bits=bits, upper_bound=u_bound)
                        result[f'Q-lotto game-{i + 1}'] = custom_num
                    st.dataframe(data=result.T)
                elif num_game == '4':
                    for i in range(int(num_game)):
                        custom_num = get_rng_lotto(n_get_num=custom_n, bits=bits, upper_bound=u_bound)
                        result[f'Q-lotto game-{i + 1}'] = custom_num
                    st.dataframe(data=result.T)
                elif num_game == '5':
                    for i in range(int(num_game)):
                        custom_num = get_rng_lotto(n_get_num=custom_n, bits=bits, upper_bound=u_bound)
                        result[f'Q-lotto game-{i + 1}'] = custom_num
                    st.dataframe(data=result.T)

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
                        result[f'Q-lotto game-{i + 1}'] = custom_num
                    st.dataframe(data=result.T)
                elif num_game == '2':
                    for i in range(int(num_game)):
                        custom_num = get_rng_lotto_with_birthday(month, day, n_get_num=custom_n, bits=bits,
                                                                 upper_bound=u_bound)
                        result[f'Q-lotto game-{i + 1}'] = custom_num
                    st.dataframe(data=result.T)
                elif num_game == '3':
                    for i in range(int(num_game)):
                        custom_num = get_rng_lotto_with_birthday(month, day, n_get_num=custom_n, bits=bits,
                                                                 upper_bound=u_bound)
                        result[f'Q-lotto game-{i + 1}'] = custom_num
                    st.dataframe(data=result.T)
                elif num_game == '4':
                    for i in range(int(num_game)):
                        custom_num = get_rng_lotto_with_birthday(month, day, n_get_num=custom_n, bits=bits,
                                                                 upper_bound=u_bound)
                        result[f'Q-lotto game-{i + 1}'] = custom_num
                    st.dataframe(data=result.T)
                elif num_game == '5':
                    for i in range(int(num_game)):
                        custom_num = get_rng_lotto_with_birthday(month, day, n_get_num=custom_n, bits=bits,
                                                                 upper_bound=u_bound)
                        result[f'Q-lotto game-{i + 1}'] = custom_num
                    st.dataframe(data=result.T)


#########################################################################################3
main()