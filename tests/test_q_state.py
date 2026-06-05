"""Unit tests for the q_state quantum-state data layer.

These are pure-math checks against Qiskit's quantum_info — no Streamlit, no
matplotlib — so they run fast in CI and pin down the Bloch-sphere narrative the
Quantum Lab teaches.
"""
from __future__ import annotations

import math

import pytest

from q_state import (
    MAX_LAB_BITS,
    bloch_length,
    circuit_stages,
    collapse_to_poles,
    decode_bits,
    sample_main_bits,
)

_TOL = 1e-9


def _stage(stages, key):
    return next(s for s in stages if s.key == key)


class TestInit:
    def test_all_qubits_at_north_pole(self):
        stages = circuit_stages(3)
        init = stages[0]
        assert init.key == "init"
        for x, y, z in init.bloch:
            assert abs(x) < _TOL and abs(y) < _TOL
            assert abs(z - 1.0) < _TOL  # |0⟩ = north pole
        for p0, p1 in init.p0p1:
            assert abs(p0 - 1.0) < _TOL and abs(p1) < _TOL


class TestSuperposition:
    def test_hadamard_moves_to_equator(self):
        sup = _stage(circuit_stages(3), "superposition")
        assert sup.gate_added == "H"
        for x, y, z in sup.bloch:
            assert abs(z) < _TOL  # on the equator
            assert abs(x - 1.0) < _TOL  # |+⟩ points along +X
            assert abs(y) < _TOL
        for p0, p1 in sup.p0p1:
            assert abs(p0 - 0.5) < _TOL and abs(p1 - 0.5) < _TOL

    def test_superposition_is_pure(self):
        sup = _stage(circuit_stages(4), "superposition")
        for vec in sup.bloch:
            assert abs(bloch_length(vec) - 1.0) < _TOL


class TestPhase:
    def test_t_gate_rotates_azimuth_only(self):
        stages = circuit_stages(2, phase_demo=True)
        phase = _stage(stages, "phase")
        assert phase.gate_added == "T"
        for x, y, z in phase.bloch[:2]:  # result qubits
            assert abs(z) < _TOL  # still on the equator
            assert abs(x - math.cos(math.pi / 4)) < 1e-6
            assert abs(y - math.sin(math.pi / 4)) < 1e-6
        # Phase must NOT change measurement probabilities.
        for p0, p1 in phase.p0p1[:2]:
            assert abs(p0 - 0.5) < _TOL and abs(p1 - 0.5) < _TOL

    def test_phase_stage_absent_by_default(self):
        assert all(s.key != "phase" for s in circuit_stages(3))


class TestEntanglement:
    def test_entanglement_shrinks_some_bloch_vectors(self):
        stages = circuit_stages(6, birthday=(8, 30))
        ent = _stage(stages, "entangle")
        assert ent.gate_added == "CRY"
        lengths = [bloch_length(v) for v in ent.bloch[: ent.num_main]]
        # The two CRY-targeted qubits become mixed (|r| < 1) ...
        assert min(lengths) < 0.99
        # ... while untouched qubits stay pure (|r| ≈ 1).
        assert max(lengths) > 0.999

    def test_ancilla_count(self):
        ent = _stage(circuit_stages(6, birthday=(1, 1)), "entangle")
        assert ent.num_ancilla == 2
        assert ent.num_main == 6
        assert len(ent.bloch) == 8

    def test_birthday_requires_two_bits(self):
        with pytest.raises(ValueError):
            circuit_stages(1, birthday=(1, 1))


class TestGuards:
    def test_zero_bits_rejected(self):
        with pytest.raises(ValueError):
            circuit_stages(0)

    def test_over_cap_rejected(self):
        with pytest.raises(ValueError):
            circuit_stages(MAX_LAB_BITS + 1)


class TestCollapse:
    def test_poles_follow_bits(self):
        # MSB-first "101" → q2=1, q1=0, q0=1; output indexed q0..q2
        poles = collapse_to_poles("101")
        assert poles[0] == (0.0, 0.0, -1.0)  # q0 = 1 → south
        assert poles[1] == (0.0, 0.0, 1.0)  # q1 = 0 → north
        assert poles[2] == (0.0, 0.0, -1.0)  # q2 = 1 → south


class TestDecode:
    def test_decimal_matches_builtin(self):
        contribs, total = decode_bits("101011")
        assert total == int("101011", 2) == 43
        # least-significant first
        assert contribs[0].place_value == 1
        assert contribs[5].place_value == 32
        assert sum(c.contribution for c in contribs) == total

    @pytest.mark.parametrize("bitstring", ["0", "1", "111111", "000000", "100000"])
    def test_roundtrip(self, bitstring):
        _, total = decode_bits(bitstring)
        assert total == int(bitstring, 2)


class TestSampling:
    def test_sample_length_and_alphabet(self):
        stages = circuit_stages(4)
        final = stages[-1]
        bits = sample_main_bits(final.statevector, final.num_main, seed=7)
        assert len(bits) == 4
        assert set(bits) <= {"0", "1"}

    def test_sample_is_deterministic_with_seed(self):
        final = circuit_stages(5)[-1]
        a = sample_main_bits(final.statevector, final.num_main, seed=123)
        b = sample_main_bits(final.statevector, final.num_main, seed=123)
        assert a == b

    def test_sample_drops_ancillas(self):
        # Birthday adds 2 ancillas; sampled result must still be `bits` wide.
        final = circuit_stages(6, birthday=(8, 30))[-1]
        bits = sample_main_bits(final.statevector, final.num_main, seed=1)
        assert len(bits) == 6
