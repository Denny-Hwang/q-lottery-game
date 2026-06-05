"""Quantum-state data layer for the interactive "Quantum Lab" visualization.

This module is deliberately **pure**: it depends only on Qiskit's
``quantum_info`` (no Streamlit, no matplotlib, no AerSimulator), so the math can
be unit-tested quickly in CI. Rendering lives in ``bloch_viz.py`` and the page
flow in ``lab.py``.

It mirrors the circuits in :mod:`q_function` but, instead of measuring once,
exposes the *intermediate* statevector after each stage so the UI can show how
every qubit moves on the Bloch sphere:

    |0⟩ (north pole)  --H-->  superposition (equator)  --T/S/Z-->  phase rotation
                                                        --CRY-->   entanglement
                                                        --measure--> collapse

Bloch coordinates come from the single-qubit *reduced* density matrix, so an
entangled qubit correctly shows a **shrunken** vector (|r| < 1) — the visual
heart of "if you only look at part of an entangled system, its state is fuzzy."
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, Pauli, Statevector, partial_trace

# (x, y, z) Bloch-sphere coordinates. North pole (0,0,+1) = |0⟩, south = |1⟩.
Vec3 = tuple[float, float, float]

# Teaching cap: statevector size is 2**n, so keep the lab small and snappy.
MAX_LAB_BITS = 6

# The phase-demo gate. T = diag(1, e^{iπ/4}) rotates the equator vector by 45°
# *without* changing measurement probabilities — exactly the point we teach.
_PHASE_GATE_LABEL = "T"
_PHASE_ANGLE = math.pi / 4


@dataclass(frozen=True)
class StageState:
    """A snapshot of the circuit after one teaching stage (before measurement)."""

    key: str  # "init" | "superposition" | "phase" | "entangle"
    circuit: QuantumCircuit  # partial circuit up to this stage (for drawing)
    statevector: Statevector
    bloch: list[Vec3]  # per-qubit Bloch vector; entangled qubits have |r| < 1
    p0p1: list[tuple[float, float]]  # per-qubit (P0, P1)
    gate_added: Optional[str]  # gate introduced by this stage, e.g. "H"
    num_main: int  # number of result qubits (decoded into the number)
    num_ancilla: int  # birthday ancillas, shown but not decoded


@dataclass(frozen=True)
class BitContribution:
    """One bit's contribution to the decoded decimal number."""

    qubit: int  # 0 = least-significant
    bit: int  # 0 or 1
    place_value: int  # 2 ** qubit
    contribution: int  # bit * place_value


def _qubit_bloch_and_probs(dm: DensityMatrix, qubit: int, n: int) -> tuple[Vec3, tuple[float, float]]:
    """Reduce ``dm`` to ``qubit`` and read off its Bloch vector and (P0, P1)."""
    others = [i for i in range(n) if i != qubit]
    rho = partial_trace(dm, others) if others else dm
    x = float(rho.expectation_value(Pauli("X")).real)
    y = float(rho.expectation_value(Pauli("Y")).real)
    z = float(rho.expectation_value(Pauli("Z")).real)
    p0 = float(rho.data[0, 0].real)
    p1 = float(rho.data[1, 1].real)
    return (x, y, z), (p0, p1)


def bloch_length(vec: Vec3) -> float:
    """Length of a Bloch vector. 1.0 = pure state, < 1.0 = mixed (entangled)."""
    x, y, z = vec
    return math.sqrt(x * x + y * y + z * z)


def circuit_stages(
    bits: int,
    *,
    birthday: Optional[tuple[int, int]] = None,
    phase_demo: bool = False,
) -> list[StageState]:
    """Build the teaching circuit one stage at a time and snapshot each state.

    Stages: ``init`` → ``superposition`` → (``phase``) → (``entangle``).
    The optional stages mirror :func:`q_function._build_birthday_circuit` and the
    phase-gate demo. No measurement is applied; sampling happens in
    :func:`sample_main_bits`.
    """
    if bits < 1:
        raise ValueError("bits must be >= 1")
    if bits > MAX_LAB_BITS:
        raise ValueError(f"Lab is capped at {MAX_LAB_BITS} bits (got {bits}).")

    has_birthday = birthday is not None
    if has_birthday and bits < 2:
        raise ValueError("Birthday mode requires at least 2 bits.")

    n_main = bits
    n_ancilla = 2 if has_birthday else 0
    n = n_main + n_ancilla

    qc = QuantumCircuit(n)
    stages: list[StageState] = []

    def snapshot(key: str, gate_added: Optional[str]) -> None:
        sv = Statevector(qc)
        dm = DensityMatrix(sv)
        bloch: list[Vec3] = []
        p0p1: list[tuple[float, float]] = []
        for q in range(n):
            vec, probs = _qubit_bloch_and_probs(dm, q, n)
            bloch.append(vec)
            p0p1.append(probs)
        stages.append(
            StageState(
                key=key,
                circuit=qc.copy(),
                statevector=sv,
                bloch=bloch,
                p0p1=p0p1,
                gate_added=gate_added,
                num_main=n_main,
                num_ancilla=n_ancilla,
            )
        )

    # Stage 0 — every qubit starts at |0⟩ (north pole).
    snapshot("init", None)

    # Stage 1 — Hadamard on every qubit → 50/50 superposition (equator).
    for q in range(n):
        qc.h(q)
    snapshot("superposition", "H")

    # Stage 2 (optional) — a phase gate rotates the equator vector without
    # touching P0/P1. Applied to the result qubits only.
    if phase_demo:
        for q in range(n_main):
            qc.t(q)
        snapshot("phase", _PHASE_GATE_LABEL)

    # Stage 3 (optional) — entangle birthday ancillas into two distinct result
    # qubits, mirroring _build_birthday_circuit. The reduced Bloch vectors of
    # the targeted qubits shrink, visualizing entanglement.
    if has_birthday:
        month, day = birthday  # type: ignore[misc]
        target_m = (month - 1) % bits
        target_d = (day - 1) % bits
        if target_d == target_m:
            target_d = (target_d + 1) % bits
        month_angle = (month / 13.0) * (math.pi / 2)
        day_angle = (day / 32.0) * (math.pi / 2)
        q_month = n_main
        q_day = n_main + 1
        qc.cry(month_angle, q_month, target_m)
        qc.cry(day_angle, q_day, target_d)
        snapshot("entangle", "CRY")

    return stages


def collapse_to_poles(bitstring: str) -> list[Vec3]:
    """Map a measured bitstring to per-qubit poles (index 0 = least-significant).

    ``bitstring`` is most-significant-first (the natural reading order and the
    same order Qiskit prints), so ``bitstring[0]`` is the highest qubit.
    """
    bits = len(bitstring)
    poles: list[Vec3] = []
    for q in range(bits):
        bit = bitstring[bits - 1 - q]
        poles.append((0.0, 0.0, 1.0) if bit == "0" else (0.0, 0.0, -1.0))
    return poles


def decode_bits(bitstring: str) -> tuple[list[BitContribution], int]:
    """Break a measured bitstring into place-value contributions and the total.

    Returns contributions ordered least-significant-first and the decimal sum,
    which equals ``int(bitstring, 2)``.
    """
    bits = len(bitstring)
    contributions: list[BitContribution] = []
    total = 0
    for q in range(bits):
        bit = int(bitstring[bits - 1 - q])
        place = 2 ** q
        contributions.append(
            BitContribution(qubit=q, bit=bit, place_value=place, contribution=bit * place)
        )
        total += bit * place
    return contributions, total


def sample_main_bits(
    state: Statevector,
    num_main: int,
    *,
    seed: Optional[int] = None,
) -> str:
    """Sample one measurement and return the result qubits as an MSB-first string.

    Sampling from the final statevector reproduces the same marginal
    distribution as measuring the real circuit (ancillas are traced out), so the
    birthday bias is preserved. The result qubits are the lowest indices, which
    appear on the right of Qiskit's MSB-first outcome string.
    """
    if seed is not None:
        state = state.copy()
        state.seed(seed)
    outcome = state.sample_memory(shots=1)[0]
    return outcome[-num_main:]
