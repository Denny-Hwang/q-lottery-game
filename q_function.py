"""Quantum random number generation for the Q-Lottery service.

This module wraps Qiskit + AerSimulator to produce uniform random integers in a
configurable range. Two modes are supported:

- ``random_number``: Hadamard-only superposition (true Q-RNG).
- ``random_number_with_birthday``: adds two ancillas controlled by the user's
  birth month/day, gently entangling the result with the birthday.

Circuit drawing is opt-in (``draw=False`` by default) because matplotlib is the
dominant cost when generating many numbers.
"""
from __future__ import annotations

import math
from functools import lru_cache

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit.visualization import circuit_drawer
from qiskit_aer import AerSimulator

# A single simulator instance is reused across calls.
_BACKEND = AerSimulator()

# Bound the rejection-sampling loop. Worst-case 6-bit/45 rejects ~30%, so 64
# attempts gives < 10^-9 failure probability for sane inputs.
_MAX_REJECTION_RETRIES = 256


class QRNGError(RuntimeError):
    """Raised when rejection sampling cannot find a number in range."""


def bits_needed(upper_bound: int) -> int:
    """Minimum number of bits required to represent ``upper_bound``."""
    if upper_bound < 1:
        raise ValueError("upper_bound must be >= 1")
    return max(1, math.ceil(math.log2(upper_bound + 1)))


@lru_cache(maxsize=64)
def _build_simple_circuit(bits: int) -> QuantumCircuit:
    qr = QuantumRegister(bits, "qubit")
    cr = ClassicalRegister(bits, "c_bit")
    circuit = QuantumCircuit(qr, cr)
    circuit.h(qr)
    circuit.measure(qr, cr)
    return circuit


def _build_birthday_circuit(bits: int, month: int, day: int) -> QuantumCircuit:
    """Build a birthday-entangled circuit.

    The ancilla qubits target two *distinct* main qubits to avoid the
    self-collision bug present in earlier versions. Rotation angles stay strictly
    inside ``(0, π/2)`` so that no single bit becomes fully deterministic at the
    edges of the calendar.
    """
    if bits < 2:
        raise ValueError("Birthday mode requires at least 2 bits.")

    qr = QuantumRegister(bits, "qubit")
    q_month = QuantumRegister(1, "q-month")
    q_day = QuantumRegister(1, "q-day")
    cr = ClassicalRegister(bits, "c_bit")

    circuit = QuantumCircuit(qr, q_month, q_day, cr)
    circuit.h(qr)
    circuit.h(q_month)
    circuit.h(q_day)
    circuit.barrier()

    # Pick two distinct main qubits so the ancillas can't collide.
    target_m = (month - 1) % bits
    target_d = (day - 1) % bits
    if target_d == target_m:
        target_d = (target_d + 1) % bits

    # Map month/day to a soft rotation in (0, π/2). The +1 offsets keep edge
    # dates (1/1 and 12/31) from collapsing to fully deterministic bits.
    month_angle = ((month) / 13.0) * (np.pi / 2)
    day_angle = ((day) / 32.0) * (np.pi / 2)

    circuit.cry(month_angle, q_month[0], qr[target_m])
    circuit.cry(day_angle, q_day[0], qr[target_d])
    circuit.barrier()

    circuit.measure(qr, cr)
    return circuit


def _draw(circuit: QuantumCircuit):
    return circuit_drawer(
        circuit,
        output="mpl",
        scale=1,
        vertical_compression="high",
        style={"backgroundcolor": "#EEEEEE"},
    )


def _measure(circuit: QuantumCircuit, bits: int):
    transpiled = transpile(circuit, _BACKEND)
    memory = _BACKEND.run(transpiled, shots=1, memory=True).result().get_memory()
    raw = memory[0]
    bitstring = raw.split(" ")[0][:bits]
    return raw, bitstring, int(bitstring, 2)


def random_number(bits: int = 6, draw: bool = False):
    """Return (figure_or_None, raw_bits, decimal)."""
    circuit = _build_simple_circuit(bits)
    raw, _, decimal = _measure(circuit, bits)
    figure = _draw(circuit) if draw else None
    return figure, raw, decimal


def random_number_with_birthday(month: int, day: int, bits: int = 6, draw: bool = False):
    """Birthday-entangled variant of :func:`random_number`."""
    circuit = _build_birthday_circuit(bits, month, day)
    raw, _, decimal = _measure(circuit, bits)
    figure = _draw(circuit) if draw else None
    return figure, raw, decimal


def _in_range(value: int, upper_bound: int) -> bool:
    return 1 <= value <= upper_bound


def q_rng_lotto(bits: int = 6, upper_bound: int = 45, draw: bool = False):
    """Rejection-sample a single number in ``[1, upper_bound]``."""
    for _ in range(_MAX_REJECTION_RETRIES):
        fig, raw, decimal = random_number(bits=bits, draw=draw)
        if _in_range(decimal, upper_bound):
            return fig, raw, decimal
    raise QRNGError(
        f"Failed to sample a number in [1, {upper_bound}] after "
        f"{_MAX_REJECTION_RETRIES} attempts (bits={bits})."
    )


def q_rng_lotto_with_birthday(
    month: int, day: int, bits: int = 6, upper_bound: int = 45, draw: bool = False
):
    for _ in range(_MAX_REJECTION_RETRIES):
        fig, raw, decimal = random_number_with_birthday(
            month, day, bits=bits, draw=draw
        )
        if _in_range(decimal, upper_bound):
            return fig, raw, decimal
    raise QRNGError(
        f"Failed to sample a birthday-entangled number in [1, {upper_bound}] "
        f"after {_MAX_REJECTION_RETRIES} attempts (bits={bits})."
    )
