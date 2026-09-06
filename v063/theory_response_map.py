#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math, os, subprocess, sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'v019/ini/aest_exp.ini'
KB = 0.0665
TAUH0 = 10.0
LAMBDA = 10.0
ZMAX = 5.0
PKMAX_H = 2.0

START = {
    'H0': 67.3324639084866,
    'omega_b': 0.022377376877682164,
    'omega_cdm': 0.12006705327635288,
    'tau_reio': 0.06174082364515668,
    'n_s': 0.9666229454895277,
    'A_s': 2.1308864352626987e-9,
}

RSD_Z = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5], dtype=float)
RSD_K = np.array([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], dtype=float)


def rewrite_ini(text, root):
    ch = dict(START)
    ch['aest_KB'] = KB
    out = []
    seen = set()
    have_zmax = False
    have_pkmax = False
    have_output = False
    have_nl = False
    for line in text.splitlines():
        st = line.strip()
        key = st.split('=', 1)[0].strip() if '=' in st else None
        if st.startswith('root ='):
            out.append(f'root = {root}')
        elif st.startswith('output ='):
            out.append('output = mPk,mTk')
            have_output = True
        elif key == 'z_max_pk':
            out.append(f'z_max_pk = {ZMAX:.17g}')
            have_zmax = True
        elif key == 'P_k_max_h/Mpc':
            out.append(f'P_k_max_h/Mpc = {PKMAX_H:.17g}')
            have_pkmax = True
        elif key == 'non linear':
            out.append('non linear = none')
            have_nl = True
        elif key in ch:
            out.append(f'{key} = {ch[key]:.17g}')
            seen.add(key)
        else:
            out.append(line)
    missing = set(ch) - seen
    if missing:
        raise RuntimeError(f'missing CLASS parameters in base ini: {sorted(missing)}')
    if not have_output:
        out.append('output = mPk,mTk')
    if not have_zmax:
        out.append(f'z_max_pk = {ZMAX:.17g}')
    if not have_pkmax:
        out.append(f'P_k_max_h/Mpc = {PKMAX_H:.17g}')
    if not have_nl:
        out.append('non linear = none')
    out += [
        '# v0.63 predeclared theory-first response map',
        'aest_memory_enabled = no',
        'aest_memory_order = 16',
        'aest_eta = 0',
        f'aest_tau_H0 = {TAUH0:.17g}',
    ]
    return '\n'.join(out) + '\n'


def build_forcing(class_root):
    results = ROOT / 'results'
    results.mkdir(exist_ok=True)
    trace = results / 'v063_theory_trace.dat'
    ini = class_root / 'v063_theory_trace.ini'
    ini.write_text(rewrite_ini(BASE.read_text(), 'output/v063_theory_trace_'))
    env = os.environ.copy()
    env['OMP_NUM_THREADS'] = '1'
    env['AEST_OFFLINE_TRACE_FILE'] = str(trace.resolve())
    log = results / 'v063_theory_trace.log'
    with log.open('w') as f:
        subprocess.run(
            [str(class_root / 'class'), ini.name, str(ROOT / 'v019p/pre/p3.pre')],
            cwd=class_root,
            env=env,
            stdout=f,
            stderr=subprocess.STDOUT,
            check=True,
        )
    if not trace.exists() or trace.stat().st_size == 0:
        raise RuntimeError('v0.63 base trace was not produced')
    prefix = results / 'v063_theory'
    summary = results / 'v063_theory_forcing.json'
    subprocess.run(
        [
            sys.executable,
            str(ROOT / 'v039/build_tau_forcing.py'),
            str(trace),
            '--KB', str(KB),
            '--tauH0', str(TAUH0),
            '--out-prefix', str(prefix),
            '--control-order', '512',
            '--primary-order', '1024',
            '--summary', str(summary),
        ],
        check=True,
    )
    force = Path(str(prefix) + '_force.dat')
    if not force.exists() or force.stat().st_size == 0:
        raise RuntimeError('v0.63 tangent forcing was not produced')
    return force.resolve(), summary


def class_params():
    return {
        'H0': START['H0'],
        'omega_b': START['omega_b'],
        'N_ur': 2.046,
        'omega_cdm': START['omega_cdm'],
        'N_ncdm': 1,
        'm_ncdm': 0.06,
        'T_ncdm': 0.7137658555036082,
        'YHe': 0.2454006,
        'tau_reio': START['tau_reio'],
        'n_s': START['n_s'],
        'A_s': START['A_s'],
        'gauge': 'newtonian',
        'aest_enabled': 'yes',
        'aest_model': 'Exp',
        'aest_KB': KB,
        'aest_Q0': 1e-4,
        'aest_K2': 9500,
        'aest_Z0': 1e-17,
        'output': 'mPk,mTk',
        'z_max_pk': ZMAX,
        'P_k_max_h/Mpc': PKMAX_H,
        'aest_memory_enabled': 'no',
        'aest_memory_order': 16,
        'aest_eta': 0.0,
        'aest_tau_H0': TAUH0,
    }


def compute_model(force_file, lam):
    from classy import Class

    keys = ['AEST_TANGENT_FORCE_FILE', 'AEST_TANGENT_LAMBDA']
    saved = {k: os.environ.get(k) for k in keys}
    try:
        if lam is None:
            for k in keys:
                os.environ.pop(k, None)
        else:
            os.environ['AEST_TANGENT_FORCE_FILE'] = str(force_file)
            os.environ['AEST_TANGENT_LAMBDA'] = str(float(lam))
        os.environ['OMP_NUM_THREADS'] = '1'

        c = Class()
        c.set(class_params())
        c.compute()

        pk, k, z = c.get_pk_and_k_and_z(nonlinear=False, only_clustering_species=False, h_units=True)
        wpk, kw, zw = c.get_Weyl_pk_and_k_and_z(nonlinear=False, h_units=True)
        tk, kt, zt = c.get_transfer_and_k_and_z(output_format='class', h_units=True)

        if not (np.allclose(k, kw, rtol=0, atol=1e-13) and np.allclose(k, kt, rtol=0, atol=1e-13)):
            raise RuntimeError('CLASS k grids differ between Pm/Weyl/transfer outputs')
        if not (np.allclose(z, zw, rtol=0, atol=1e-12) and np.allclose(z, zt, rtol=0, atol=1e-12)):
            raise RuntimeError('CLASS z grids differ between Pm/Weyl/transfer outputs')
        if 'phi' not in tk or 'psi' not in tk:
            raise RuntimeError(f'CLASS transfer output lacks phi/psi; keys={sorted(tk)}')

        phi = np.asarray(tk['phi'], dtype=float)
        psi = np.asarray(tk['psi'], dtype=float)
        weyl = 0.5 * (phi + psi)

        sigma8 = np.array([float(c.sigma(8.0, float(zz), h_units=True)) for zz in RSD_Z])
        growth_D = np.empty((len(RSD_K), len(RSD_Z)), dtype=float)
        growth_f = np.empty_like(growth_D)
        for ik, kk in enumerate(RSD_K):
            for iz, zz in enumerate(RSD_Z):
                growth_D[ik, iz] = float(c.scale_dependent_growth_factor_D(float(kk), float(zz), h_units=True, nonlinear=False))
                growth_f[ik, iz] = float(c.scale_dependent_growth_factor_f(float(kk), float(zz), h_units=True, nonlinear=False))
        fs8 = growth_f * sigma8[None, :]

        result = {
            'pk': np.asarray(pk, dtype=float).copy(),
            'weyl_pk': np.asarray(wpk, dtype=float).copy(),
            'phi': phi.copy(),
            'psi': psi.copy(),
            'weyl': weyl.copy(),
            'k': np.asarray(k, dtype=float).copy(),
            'z': np.asarray(z, dtype=float).copy(),
            'sigma8': sigma8,
            'growth_D': growth_D,
            'growth_f': growth_f,
            'fs8': fs8,
        }
        c.struct_cleanup()
        c.empty()
        return result
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def frac_response(base, plus, minus):
    b = np.asarray(base, dtype=float)
    p = np.asarray(plus, dtype=float)
    m = np.asarray(minus, dtype=float)
    scale = np.nanmax(np.abs(b))
    floor = max(scale * 1e-14, 1e-300)
    out = np.full_like(b, np.nan, dtype=float)
    mask = np.isfinite(b) & np.isfinite(p) & np.isfinite(m) & (np.abs(b) > floor)
    out[mask] = (p[mask] - m[mask]) / (2.0 * LAMBDA * b[mask])
    return out


def window_summary(field, k, z, krange, zrange):
    f = np.asarray(field, dtype=float)
    kk = np.asarray(k, dtype=float)[:, None]
    zz = np.asarray(z, dtype=float)[None, :]
    mask = (
        np.isfinite(f)
        & (kk >= krange[0]) & (kk <= krange[1])
        & (zz >= zrange[0]) & (zz <= zrange[1])
    )
    vals = f[mask]
    if vals.size == 0:
        raise RuntimeError(f'empty theory-response window k={krange}, z={zrange}')
    af = np.where(mask, np.abs(f), -np.inf)
    flat = int(np.nanargmax(af))
    ik, iz = np.unravel_index(flat, f.shape)
    return {
        'rms_abs_fractional_response_per_eta': float(np.sqrt(np.mean(vals * vals))),
        'mean_abs_fractional_response_per_eta': float(np.mean(np.abs(vals))),
        'max_abs_fractional_response_per_eta': float(abs(f[ik, iz])),
        'max_location': {'k_h_per_Mpc': float(k[ik]), 'z': float(z[iz]), 'signed_response': float(f[ik, iz])},
        'n_grid_points': int(vals.size),
    }


def grid_summary(field, k, z):
    f = np.asarray(field, dtype=float)
    mask = np.isfinite(f)
    vals = f[mask]
    if vals.size == 0:
        raise RuntimeError('empty fixed response grid')
    flat = int(np.nanargmax(np.abs(f)))
    ik, iz = np.unravel_index(flat, f.shape)
    return {
        'rms_abs_fractional_response_per_eta': float(np.sqrt(np.mean(vals * vals))),
        'mean_abs_fractional_response_per_eta': float(np.mean(np.abs(vals))),
        'max_abs_fractional_response_per_eta': float(abs(f[ik, iz])),
        'max_location': {'k_h_per_Mpc': float(k[ik]), 'z': float(z[iz]), 'signed_response': float(f[ik, iz])},
        'n_grid_points': int(vals.size),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--class-root', required=True)
    ap.add_argument('--json-out', required=True)
    ap.add_argument('--npz-out', required=True)
    a = ap.parse_args()

    class_root = Path(a.class_root).resolve()
    force, forcing_summary = build_forcing(class_root)

    base = compute_model(force, None)
    plus = compute_model(force, +LAMBDA)
    minus = compute_model(force, -LAMBDA)

    if not (np.allclose(base['k'], plus['k'], rtol=0, atol=1e-13) and np.allclose(base['k'], minus['k'], rtol=0, atol=1e-13)):
        raise RuntimeError('base/+lambda/-lambda k grids differ')
    if not (np.allclose(base['z'], plus['z'], rtol=0, atol=1e-12) and np.allclose(base['z'], minus['z'], rtol=0, atol=1e-12)):
        raise RuntimeError('base/+lambda/-lambda z grids differ')

    dln_pk = frac_response(base['pk'], plus['pk'], minus['pk'])
    dln_wpk = frac_response(base['weyl_pk'], plus['weyl_pk'], minus['weyl_pk'])
    dln_phi = frac_response(base['phi'], plus['phi'], minus['phi'])
    dln_psi = frac_response(base['psi'], plus['psi'], minus['psi'])
    dln_weyl = frac_response(base['weyl'], plus['weyl'], minus['weyl'])
    dln_D = frac_response(base['growth_D'], plus['growth_D'], minus['growth_D'])
    dln_fs8 = frac_response(base['fs8'], plus['fs8'], minus['fs8'])
    dln_sigma8 = frac_response(base['sigma8'], plus['sigma8'], minus['sigma8'])

    scores = {
        'cosmic_shear_weyl': window_summary(dln_wpk, base['k'], base['z'], (0.01, 0.30), (0.2, 1.5)),
        'linear_galaxy_clustering': window_summary(dln_pk, base['k'], base['z'], (0.01, 0.20), (0.2, 1.5)),
        'RSD_fsigma8': grid_summary(dln_fs8, RSD_K, RSD_Z),
    }
    cmb_lensing = window_summary(dln_wpk, base['k'], base['z'], (0.01, 0.50), (0.5, 5.0))

    selected = max(scores, key=lambda key: scores[key]['rms_abs_fractional_response_per_eta'])

    diagnostics = {
        'weyl_amplitude_shear_window': window_summary(dln_weyl, base['k'], base['z'], (0.01, 0.30), (0.2, 1.5)),
        'phi_shear_window': window_summary(dln_phi, base['k'], base['z'], (0.01, 0.30), (0.2, 1.5)),
        'psi_shear_window': window_summary(dln_psi, base['k'], base['z'], (0.01, 0.30), (0.2, 1.5)),
        'growth_D_fixed_RSD_grid': grid_summary(dln_D, RSD_K, RSD_Z),
        'sigma8_response_by_z': [
            {'z': float(z), 'dln_sigma8_deta': float(x)} for z, x in zip(RSD_Z, dln_sigma8)
        ],
    }

    result = {
        'classification': 'V063_THEORY_FIRST_TARGET_SELECTION_COMPLETE',
        'predata_classification': 'V063_PREDATA_THEORY_FIRST_TARGET_SELECTION',
        'uses_observational_data': False,
        'locked_model': {
            'KB': KB,
            'tauH0': TAUH0,
            'p': 0.0,
            'lambda': LAMBDA,
            'CLASS_commit': 'e85808324f51fc694d12e3ed7439552a3c3f9540',
            'cosmology': START,
        },
        'response_definition': '(X(+lambda)-X(-lambda))/(2 lambda X0), i.e. fractional response per unit eta at eta=0',
        'theory_domain': {'z_max_pk': ZMAX, 'P_k_max_h_per_Mpc': PKMAX_H, 'linear_theory_only': True},
        'scores': scores,
        'selected_next_observable_class': selected,
        'selection_rule': 'Largest predeclared RMS absolute fractional response per unit eta among cosmic shear/Weyl, linear galaxy clustering/Pm, and RSD f-sigma8.',
        'cmb_lensing_weyl_proxy_not_ranked': cmb_lensing,
        'diagnostics': diagnostics,
        'RSD_grid': {'z': RSD_Z.tolist(), 'k_h_per_Mpc': RSD_K.tolist(), 'dln_fsigma8_deta': dln_fs8.tolist(), 'dln_D_deta': dln_D.tolist()},
        'forcing_summary_file': str(forcing_summary.relative_to(ROOT)),
        'interpretation_caution': 'Response-only observable-class selection. Scores are not signal-to-noise forecasts and do not use survey residuals, covariances, or anomaly significances.',
        'anti_tuning': 'The observable-class windows and ranking rule were committed before this response calculation and before fitting any new late-time dataset.',
    }

    Path(a.json_out).write_text(json.dumps(result, indent=2))
    np.savez_compressed(
        a.npz_out,
        k_h_per_Mpc=base['k'],
        z=base['z'],
        dln_Pm_deta=dln_pk,
        dln_WeylPk_deta=dln_wpk,
        dln_phi_deta=dln_phi,
        dln_psi_deta=dln_psi,
        dln_WeylAmplitude_deta=dln_weyl,
        rsd_k_h_per_Mpc=RSD_K,
        rsd_z=RSD_Z,
        dln_D_deta=dln_D,
        dln_fsigma8_deta=dln_fs8,
        dln_sigma8_deta=dln_sigma8,
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
