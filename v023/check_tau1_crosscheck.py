#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math

V020_MARG = 1.9398420148928963e-7
V020_RETAINED = 0.5978222583759274
V020_RAW = 3.244847423651913e-7


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('analysis')
    ap.add_argument('--json-out', default='results/v023_tau1_crosscheck.json')
    args = ap.parse_args()
    d = json.loads(Path(args.analysis).read_text())
    mem = d['memory_tangent_control_lambda300_vs1000']
    rel_marg = abs(d['marginalized_CV_SNR_per_unit_eta']-V020_MARG)/V020_MARG
    rel_raw = abs(d['raw_CV_SNR_per_unit_eta']-V020_RAW)/V020_RAW
    abs_ret = abs(d['CV_retained_fraction_after_core_LCDM_projection']-V020_RETAINED)
    gates = {
        'offline_quadrature': bool(d['gates']['bath_convergence']),
        'lambda_linearity': bool(mem['relative_CV_norm'] < 0.05 and mem['cosine_CV'] > 0.999),
        'nuisance_rank': bool(d['nuisance_basis_rank'] == 6),
        'tau1_marginalized_vs_v020': bool(rel_marg < 0.10),
        'tau1_retained_vs_v020': bool(abs_ret < 0.10),
    }
    out = {
        'classification': 'V023_TAU1_SOURCE_GRID_CROSSCHECK_PASS' if all(gates.values()) else 'V023_TAU1_SOURCE_GRID_CROSSCHECK_FAIL',
        'tauH0': d['tauH0'],
        'lambda_control': mem,
        'raw_CV_SNR_per_unit_eta': d['raw_CV_SNR_per_unit_eta'],
        'marginalized_CV_SNR_per_unit_eta': d['marginalized_CV_SNR_per_unit_eta'],
        'retained_fraction': d['CV_retained_fraction_after_core_LCDM_projection'],
        'relative_raw_difference_vs_v020': rel_raw,
        'relative_marginalized_difference_vs_v020': rel_marg,
        'absolute_retained_difference_vs_v020': abs_ret,
        'gates': gates,
    }
    q = Path(args.json_out); q.parent.mkdir(parents=True, exist_ok=True); q.write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
    if not all(gates.values()):
        raise SystemExit(2)


if __name__ == '__main__':
    main()
