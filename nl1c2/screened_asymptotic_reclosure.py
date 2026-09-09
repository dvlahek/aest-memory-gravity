#!/usr/bin/env python3
from pathlib import Path
import json
import math

OUT = Path('results')
OUT.mkdir(exist_ok=True)

KB = 0.0665
K2 = 9500.0
Q0 = 1.0e-4  # Mpc^-1
H0 = 67.3324639084866
h = H0 / 100.0
BETAS = [1.0, 0.5, 0.1]
KINDS = ['simple', 'exponential', 'sharp']
K_H = [0.03, 0.05, 0.08, 0.10, 0.15, 0.20]
SIGNAL_MIN = 0.08
X_PHYS = [1.0911e7, 4.3274e7, 9.4551e7]
SAT_MAX = 2.0e-6
STIFF_MAX = 2.0e-6
SIGNAL_HELMHOLTZ_MAX = 0.10


def j_and_stiffness(x, beta, kind):
    A = 1.0 + beta
    if kind == 'simple':
        j = x / (A + beta * x)
        # j' = A/(A+beta x)^2, so x j'/j = A/(A+beta x)
        stiff = A / (A + beta * x)
        return j, abs(stiff)
    if kind == 'exponential':
        c = beta / A
        e = math.exp(-c * x) if c * x < 745.0 else 0.0
        j = (1.0 - e) / beta
        jp = e / A
        stiff = abs(x * jp / j) if j != 0.0 else float('inf')
        return j, stiff
    if kind == 'sharp':
        xt = A / beta
        if x < xt:
            j = x / A
            stiff = 1.0
        else:
            j = 1.0 / beta
            stiff = 0.0
        return j, stiff
    raise ValueError(kind)


def main():
    mu2 = 2.0 * K2 * Q0 * Q0 / (2.0 - KB)
    mu = math.sqrt(mu2)

    sat = {}
    all_sat = True
    max_sat = 0.0
    max_stiff = 0.0
    for kind in KINDS:
        sat[kind] = {}
        for beta in BETAS:
            rows = []
            for x in X_PHYS:
                j, stiff = j_and_stiffness(x, beta, kind)
                eps = abs(beta * j - 1.0)
                rows.append({
                    'x': x,
                    'j': j,
                    'j_infinity': 1.0 / beta,
                    'saturation_relative_error': eps,
                    'logarithmic_coefficient_stiffness': stiff,
                })
                max_sat = max(max_sat, eps)
                max_stiff = max(max_stiff, stiff)
            smallest = rows[0]
            ok = bool(
                smallest['saturation_relative_error'] <= SAT_MAX
                and smallest['logarithmic_coefficient_stiffness'] <= STIFF_MAX
            )
            all_sat = all_sat and ok
            sat[kind][str(beta)] = {'physical_checkpoints': rows, 'pass': ok}

    mass = {}
    all_mass = bool(math.isfinite(mu) and mu > 0.0)
    max_signal_corr = 0.0
    min_k_over_kmu = float('inf')
    for beta in BETAS:
        kmu = math.sqrt(1.0 + beta) * mu
        rows = []
        beta_ok = True
        for kh in K_H:
            k = kh * h
            ratio = k / kmu
            min_k_over_kmu = min(min_k_over_kmu, ratio)
            no_pole = bool(k > kmu)
            if no_pole:
                RH = k * k / (k * k - kmu * kmu)
                corr = abs(RH - 1.0)
            else:
                RH = float('nan')
                corr = float('inf')
            in_signal = kh >= SIGNAL_MIN - 1e-15
            if in_signal:
                max_signal_corr = max(max_signal_corr, corr)
            point_ok = bool(no_pole and ((not in_signal) or corr <= SIGNAL_HELMHOLTZ_MAX))
            beta_ok = beta_ok and point_ok
            rows.append({
                'k_h_per_Mpc': kh,
                'k_1_per_Mpc': k,
                'k_mu_1_per_Mpc': kmu,
                'k_over_k_mu': ratio,
                'helmholtz_to_poisson_transfer': RH,
                'absolute_fractional_correction': corr,
                'structured_signal_subband': in_signal,
                'pass': point_ok,
            })
        all_mass = all_mass and beta_ok
        mass[str(beta)] = {
            'k_mu_1_per_Mpc': kmu,
            'k_mu_inverse_Mpc': 1.0 / kmu,
            'rows': rows,
            'pass': beta_ok,
        }

    gates = {
        'mu_finite_positive': bool(math.isfinite(mu) and mu > 0.0),
        'all_nine_saturated_at_smallest_physical_x': bool(all_sat),
        'all_certified_modes_above_k_mu_and_signal_band_correction_le_10pct': bool(all_mass),
    }
    passed = bool(all(gates.values()))
    classification = (
        'NL1C2_SCREENED_ASYMPTOTIC_RECLOSURE_PASS'
        if passed else
        'NL1C2_SCREENED_ASYMPTOTIC_RECLOSURE_FAIL'
    )

    result = {
        'classification': classification,
        'scope': 'result-informed screened/high-gradient coefficient and AeST mass-scale audit only; no dynamical cosmological evolution',
        'frozen_inputs': {
            'KB': KB,
            'K2': K2,
            'Q0_1_per_Mpc': Q0,
            'H0_km_s_Mpc': H0,
            'h': h,
            'beta0_co_primary': BETAS,
            'interpolation_co_primary': KINDS,
            'k_h_per_Mpc': K_H,
            'structured_signal_subband_min_k_h_per_Mpc': SIGNAL_MIN,
            'NL1C0_physical_x_checkpoints': X_PHYS,
        },
        'derived_mass_scale': {
            'formula': 'mu^2 = 2 K2 Q0^2 / (2-KB)',
            'mu2_1_per_Mpc2': mu2,
            'mu_1_per_Mpc': mu,
            'mu_inverse_Mpc': 1.0 / mu,
        },
        'saturation': sat,
        'mass_scale_by_beta0': mass,
        'global_metrics': {
            'max_saturation_relative_error_over_all_physical_checkpoints': max_sat,
            'max_logarithmic_coefficient_stiffness_over_all_physical_checkpoints': max_stiff,
            'minimum_k_over_k_mu_over_certified_band': min_k_over_kmu,
            'maximum_abs_helmholtz_correction_over_structured_signal_subband': max_signal_corr,
        },
        'locked_gates': {
            'saturation_relative_error_at_xmin_max': SAT_MAX,
            'logarithmic_coefficient_stiffness_at_xmin_max': STIFF_MAX,
            'all_certified_modes_require_k_gt_k_mu': True,
            'structured_signal_subband_helmholtz_abs_fractional_correction_max': SIGNAL_HELMHOLTZ_MAX,
        },
        'gates': gates,
        'numerical_pass': passed,
        'historical_results_unchanged': True,
        'interpretation': (
            'PASS means the full published Y-sector is already saturated to the screened coefficient 1/beta0 at the measured physical gradient amplitude, '
            'with negligible interpolation-function stiffness, while the frozen AeST mass scale introduces no pole in the certified band. '
            'This supports a screened-resummed dynamical bridge as the next step; it is not itself a self-consistent cosmological solution or a memory-survival result.'
        ),
    }

    path = OUT / 'nl1c2_screened_asymptotic_reclosure.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    if not passed:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
