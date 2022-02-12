from qiskit import *

def random_number():
    qr = QuantumRegister(5)
    cr = ClassicalRegister(5)
    circuit = QuantumCircuit(qr,cr)
    circuit.h(qr)

    circuit.measure_all()

    backend = Aer.get_backend('qasm_simulator')
    result = execute(circuit, backend, shots=1, memory=True).result()
    counts = result.get_memory()
    num = counts[0].split(" ")[0]

    return int(num, 2)
