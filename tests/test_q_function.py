"""Unit tests for q_function.

The Qiskit simulator is fast enough to exercise in CI, but matplotlib drawing
is expensive — every test runs with ``draw=False``.
"""
from __future__ import annotations

import pytest

from q_function import (
    QRNGError,
    bits_needed,
    q_rng_lotto,
    q_rng_lotto_with_birthday,
    random_number,
)


class TestBitsNeeded:
    @pytest.mark.parametrize(
        "n,expected",
        [
            (1, 1),
            (2, 2),
            (3, 2),
            (4, 3),
            (45, 6),
            (50, 6),
            (69, 7),
            (1_000_000, 20),
        ],
    )
    def test_known_bounds(self, n, expected):
        assert bits_needed(n) == expected

    def test_invalid(self):
        with pytest.raises(ValueError):
            bits_needed(0)


class TestSimpleSampling:
    @pytest.mark.parametrize("upper", [2, 7, 45, 69])
    def test_in_range(self, upper):
        bits = bits_needed(upper)
        for _ in range(20):
            _, _, dec = q_rng_lotto(bits=bits, upper_bound=upper, draw=False)
            assert 1 <= dec <= upper

    def test_no_figure_when_draw_false(self):
        fig, _, _ = q_rng_lotto(bits=6, upper_bound=45, draw=False)
        assert fig is None

    def test_returns_figure_when_draw_true(self):
        fig, _, _ = q_rng_lotto(bits=6, upper_bound=45, draw=True)
        assert fig is not None

    def test_bitstring_consistent_with_decimal(self):
        for _ in range(20):
            _, raw, dec = random_number(bits=6, draw=False)
            bitstring = raw.split(" ")[0][:6]
            assert int(bitstring, 2) == dec


class TestBirthdaySampling:
    @pytest.mark.parametrize(
        "month,day", [(1, 1), (2, 29), (8, 30), (12, 31), (7, 15)]
    )
    def test_in_range(self, month, day):
        for _ in range(10):
            _, _, dec = q_rng_lotto_with_birthday(
                month, day, bits=6, upper_bound=45, draw=False
            )
            assert 1 <= dec <= 45

    def test_distribution_non_degenerate(self):
        """For a representative birthday, we still want > 1 distinct value."""
        seen = set()
        for _ in range(60):
            _, _, dec = q_rng_lotto_with_birthday(
                8, 30, bits=6, upper_bound=45, draw=False
            )
            seen.add(dec)
        assert len(seen) > 3, "Birthday-entangled RNG collapsed to a single value"

    def test_edge_dates_do_not_collapse(self):
        """Edge dates (1/1 and 12/31) used to fully determine some bits."""
        for month, day in [(1, 1), (12, 31)]:
            seen = set()
            for _ in range(60):
                _, _, dec = q_rng_lotto_with_birthday(
                    month, day, bits=6, upper_bound=45, draw=False
                )
                seen.add(dec)
            assert len(seen) > 3, f"Edge date {month}/{day} collapsed"


class TestRejectionRetry:
    def test_small_bound_eventually_succeeds(self):
        # upper_bound=1 means only "1" is acceptable; with 1 bit there are two
        # outcomes (0 and 1) so retries should resolve in expectation < 256.
        for _ in range(5):
            _, _, dec = q_rng_lotto(bits=1, upper_bound=1, draw=False)
            assert dec == 1

    def test_birthday_requires_min_bits(self):
        with pytest.raises(ValueError):
            q_rng_lotto_with_birthday(8, 30, bits=1, upper_bound=1, draw=False)


class TestPublicExceptions:
    def test_qrng_error_exists(self):
        # Exposed so callers (main.py) can catch it.
        assert issubclass(QRNGError, RuntimeError)
