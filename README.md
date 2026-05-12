[<img src="src/Q-Lottery-Game-logo-black.png" width="800" height="400">](https://share.streamlit.io/denny-hwang/q-lottery-game/main/main.py)

---

### 1) Generate *real* random numbers with a quantum computer

Real random number generation for lottery games, powered by the **[IBM Qiskit library](https://qiskit.org/)**.

---

### 2) What is *real* random number generation?

> "**Random number generation (RNG)** is a sequence of numbers or symbols that cannot be reasonably predicted better than by random chance. The particular outcome sequence will contain some patterns detectable in hindsight but **unpredictable** to foresight." — Wikipedia

There are two methods of [RNG](https://en.wikipedia.org/wiki/Random_number_generation):

- **True random number generation (TRNG)** uses measurement of a physical phenomenon that is expected to be random, then compensates for possible biases in the measurement process.
- **Pseudo random number generation (PRNG)** uses a computational algorithm that produces long sequences of apparently random results, which are in fact completely determined by a shorter initial value (the seed).

This application uses an IBM-flavored quantum simulator to generate real random numbers via the **superposition** of qubit states.

Two routes to RNG with **[Qiskit](https://qiskit.org/)**:

1. **Qiskit RNG** — requires an IBM Quantum account, so this app skips it. See:
   - https://qiskit.org/documentation/apidoc/ibmq_random.html
   - https://github.com/qiskit-community/qiskit_rng/
2. **Quantum-circuit-based RNG** using the **[IBM Quantum system](https://quantum-computing.ibm.com/services/docs/services/manage/systems/)**.
   - We build a quantum circuit using the **[H (Hadamard) gate](https://learn.qiskit.org/course/ch-states/single-qubit-gates#hgate)** for **[superposition](https://en.wikipedia.org/wiki/Quantum_superposition)** and the **[CRY gate](https://qiskit.org/documentation/stubs/qiskit.circuit.QuantumCircuit.cry.html)** for **[entanglement](https://en.wikipedia.org/wiki/Quantum_entanglement)** between qubits.
   - Because of generation time and IBM Q account constraints, we use the local `AerSimulator` as a backend (it mimics an IBMQ device).

---

### 3) Two modes of random number generation

#### A) Simple Q-RNG

Pure Hadamard-gate-based superposition. Every bit is a fair coin flip.

#### B) Birthday-entangled Q-RNG

- Two extra ancilla qubits are placed in superposition.
- The user's birth month and day are encoded as CRY rotation angles.
- The ancillas entangle with two **distinct** target qubits (no collision), gently biasing the result.
- Your birthday subtly nudges the distribution — without collapsing it.

---

### 4) Supported lottery games

| Game | Rule |
|---|---|
| **[Lotto (Korea)](https://dhlottery.co.kr/)** | Pick 6 numbers from 1–45 |
| **[Powerball (USA)](https://www.powerball.com/)** | 5 white balls from 1–69 + 1 Powerball from 1–26 |
| **[Lotto India (India)](https://www.lotto.in/)** | 6 numbers from 1–50 + 1 Joker ball from 1–5 |
| **[Lotto7 (Japan)](https://en.lottolyzer.com/how-to-play/japan/lotto-7)** | Pick 7 numbers from 1–37 |
| **[French Lottery (France)](http://france-lottery.com/)** | 5 numbers from 1–49 + 1 Lucky number from 1–10 |
| **Custom** | Customize your Q-Lottery game |

---

### 5) Caution

- Quantum-generated random numbers are statistically "more random" than PRNG, but **this does not improve your odds of winning**.
- Use it for fun only.

---

### 6) Run locally

```bash
pip install -r requirements.txt
streamlit run main.py
```

Python 3.11 is recommended (see `runtime.txt`).

---

### 7) Tests

```bash
pip install pytest
pytest
```

---

### 8) Contributing

Want to add another lottery? See [`add_new_game/registration_form.md`](add_new_game/registration_form.md) and open a PR.

---

### 9) License

[MIT](LICENSE)
