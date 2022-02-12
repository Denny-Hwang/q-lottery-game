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

---

### 3) There are two mode for random number generation
        
#### A) Simple random number generation using quantum circuit using qiskit library

#### B) Birth-day entangled random number generation
        
    - Add two qubit for entanglement
    - Applying user's birth-day to initial probability of the qubits
    - Add CNOT gate on birth-day qubit and RNG qubit
    - Your birth-day will change the 50/50 probability of some qubits to another random value 
    
---
    
### 4) Serviced Lottery Game

- **[Lotto(Korea)](https://dhlottery.co.kr/)**

  : Select 6 numbers in range 45  
  <img src="src/Lotto645.jpg" width="600" height="150">

- **[Powerball(USA)](https://www.powerball.com/)**

  : Select 5 numbers in range 70 for 'white ball', 1 more selection in range 25 for 'power ball'  
  <img src="src/Powerball.png" width="600" height="400">
- Customize your lottery game  
  : Select the number and upper bound for Q-rng
  
---
### 5) Caution!!

    - Although real random number generated by QC is more random than pseudo random number, 
      it does not guarantee winning of the lottery!! 
    - Just use it for fun!

---
### 6) Contribution
    
- If you want to add another "Lottery game", follow the form and send PR to **[github](https://github.com/Denny-Hwang/q-lottery-game)**  
(Under construction!)
