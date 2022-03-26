import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import Aer, execute
from qiskit.visualization import *
from tqdm import tqdm


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

    ###
    ## birth-day initialization
    month_init = (month-1) / (12-1)
    day_30 = [4, 6, 9, 11]
    if month == 2:
        if day == 29:
            day_init = (day-1) / (29-1)
        else:
            day_init = (day-1) / (28-1)
    elif np.isin(month, day_30):
        day_init = (day-1) / (30-1)
    else:
        day_init = (day-1) / (31-1)

    print(month_init*np.pi, day_init*np.pi)
    circuit.rx(month_init*np.pi, bits)
    circuit.rx(day_init*np.pi, bits + 1)

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
