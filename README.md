# Q-Lottery-game
## Let's generate real random number using IBM qiskit

Real random number generation for lottery-game using quantum computer(IBM qiskit)

### There are two mode for random number generation.
1) Simple random number generation using quantum circuit using qiskit library.
2) User birth-day entangled random number generation.
  - Applying user's birth-day to initial probability of the each qubit. It changes probability of the state after measurement.
  - Applying random entanglement between qubits using user's information

### Service Lottery Game
- Lotto(Korea)
  : Select 6 numbers in range 45
  ref: https://dhlottery.co.kr
- Powerball(USA)
  : Select 5 numbers in range 70 for 'white ball', 1 more selection in range 25 for 'power ball'
  ref: https://www.powerball.com/
