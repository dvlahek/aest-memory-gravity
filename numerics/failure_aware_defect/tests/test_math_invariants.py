#!/usr/bin/env python3
from __future__ import annotations

import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve()
MODULE_DIR = HERE.parents[1]
sys.path.insert(0, str(MODULE_DIR))

import audited_certificates as ac
from stable_tail_integrals import (
    integral_inv_1pr2,
    integral_inv_r_1pr2,
    integral_inv_r2_1pr2,
)


class TestFD8Algebra(unittest.TestCase):
    def test_exact_moments(self) -> None:
        m = ac.fd8_exact_moments()
        self.assertEqual(m[0], Fraction(0))
        self.assertEqual(m[1], Fraction(1))
        for p in range(2, 9):
            self.assertEqual(m[p], Fraction(0))
        self.assertEqual(m[9], Fraction(-576))

    def test_remainder_constant(self) -> None:
        m9 = abs(ac.fd8_exact_moments()[9])
        self.assertEqual(m9 / math.factorial(9), Fraction(1, 630))

    def test_symbol_constants(self) -> None:
        self.assertAlmostEqual(ac.FD8_L1, 25.0 / 12.0, places=15)
        self.assertAlmostEqual(ac.FD8_SYMBOL_ABS, 25.0 / 12.0, places=15)
        self.assertAlmostEqual(ac.FD8_SMALL_XI_C9, 1957.0 / 198450.0, places=15)


class TestStableTailIntegrals(unittest.TestCase):
    def test_i1_closed_form(self) -> None:
        a, b = 3.0, 17.0
        primitive = lambda r: math.log(r) - 0.5 * math.log1p(r * r)
        expected = primitive(b) - primitive(a)
        self.assertAlmostEqual(integral_inv_r_1pr2(a, b), expected, places=15)

    def test_i2_closed_form(self) -> None:
        a, b = 3.0, 17.0
        primitive = lambda r: -1.0 / r - math.atan(r)
        expected = primitive(b) - primitive(a)
        self.assertAlmostEqual(integral_inv_r2_1pr2(a, b), expected, places=15)

    def test_atan_closed_form(self) -> None:
        a, b = 3.0, 17.0
        expected = math.atan(b) - math.atan(a)
        self.assertAlmostEqual(integral_inv_1pr2(a, b), expected, places=15)

    def test_extreme_tail_positive(self) -> None:
        a = 1e8
        self.assertGreater(integral_inv_r_1pr2(a), 0.0)
        self.assertGreater(integral_inv_r2_1pr2(a), 0.0)
        self.assertGreater(integral_inv_1pr2(a), 0.0)


class TestAsymptoticConstants(unittest.TestCase):
    def test_rho_stars(self) -> None:
        expected = {
            "b1": 4.0427609317859824,
            "b2": 2.1305793530674105,
            "b3": 2.2589104840641232,
        }
        for key, target in expected.items():
            got = ac.asymptotic_rho_star(key)
            self.assertAlmostEqual(got, target, places=12)

    def test_root_residuals(self) -> None:
        pairs = {
            "b1": (ac.b1_asym_taylor, ac.b1_asym_direct),
            "b2": (ac.b2_asym_taylor, ac.b2_asym_direct),
            "b3": (ac.b3_asym_taylor, ac.b3_asym_direct),
        }
        for key, (bt, bd) in pairs.items():
            q = ac.asymptotic_rho_star(key)
            self.assertLess(abs(bt(q) - bd(q)), 1e-13)

    def test_crossover_amplitudes(self) -> None:
        targets = {
            "b1": 1.1549855770600449,
            "b2": 0.04519031920039301,
            "b3": 0.03514813830095348,
        }
        funcs = {
            "b1": ac.b1_asym_taylor,
            "b2": ac.b2_asym_taylor,
            "b3": ac.b3_asym_taylor,
        }
        for key, target in targets.items():
            q = ac.asymptotic_rho_star(key)
            self.assertAlmostEqual(funcs[key](q), target, places=12)


class TestFiniteCrossovers(unittest.TestCase):
    def test_h001_crossovers(self) -> None:
        expected_rho = {
            "b1": 4.042727714436494,
            "b2": 2.1305694651565745,
            "b3": 2.258896621495771,
        }
        h = 0.01
        for key, target in expected_rho.items():
            R = ac.finite_crossover(key, h)
            self.assertAlmostEqual(h * R, target, places=10)

    def test_small_h_crossovers(self) -> None:
        expected_rho = {
            "b1": 4.042760599594705,
            "b2": 2.130579254181833,
            "b3": 2.258910345429267,
        }
        h = 0.001
        for key, target in expected_rho.items():
            R = ac.finite_crossover(key, h)
            self.assertAlmostEqual(h * R, target, places=9)


class TestCutoffUniformity(unittest.TestCase):
    def test_direct_below_uniform_limit(self) -> None:
        h = 0.01
        cases = [
            (ac.b1_direct, ac.b1_direct_limit),
            (ac.b2_direct, ac.b2_direct_limit),
            (ac.b3_direct, ac.b3_direct_limit),
        ]
        for direct, limit in cases:
            L = limit(h)
            previous = -1.0
            for R in (100.0, 200.0, 300.0, 1e3, 3e3, 1e4):
                value = direct(R, h)
                self.assertLessEqual(value, L * (1.0 + 1e-12))
                self.assertGreaterEqual(value, previous)
                previous = value

    def test_scaled_asymptotics(self) -> None:
        rho = 3.0
        h = 1e-4
        R = rho / h
        self.assertLess(abs(ac.b1_taylor(R, h) / h**2 - ac.b1_asym_taylor(rho)), 1e-6)
        self.assertLess(abs(ac.b1_direct(R, h) / h**2 - ac.b1_asym_direct(rho)), 1e-6)
        self.assertLess(abs(ac.b2_taylor(R, h) / h - ac.b2_asym_taylor(rho)), 1e-6)
        self.assertLess(abs(ac.b2_direct(R, h) / h - ac.b2_asym_direct(rho)), 1e-6)
        self.assertLess(abs(ac.b3_taylor(R, h) / h**2 - ac.b3_asym_taylor(rho)), 1e-6)
        self.assertLess(abs(ac.b3_direct(R, h) / h**2 - ac.b3_asym_direct(rho)), 1e-6)


if __name__ == "__main__":
    unittest.main()
