#!/usr/bin/env python3
from pathlib import Path
import json,zipfile


def main():
    r=Path('results/v019w_analysis.json')
    if not r.exists(): raise RuntimeError('results/v019w_analysis.json missing')
    data=json.loads(r.read_text())
    lines=[
        'AeST MEMORY EXP tauH0=1 VARIATIONAL TANGENT v0.19w',
        '='*84,
        f"W1  | {'PASS' if data['gates']['lambda_invariance'] else 'CHECK':8s} | lambda-invariant unlensed tangent",
        f"W2  | {'PASS' if data['gates']['bath_force'] else 'CHECK':8s} | N=39/47 eta=0 forcing convergence",
        f"W3  | {'PASS' if data['gates']['forcing_precision'] else 'CHECK':8s} | p3/p4 forcing convergence",
        f"W4  | {'PASS' if data['gates']['spectrum_precision'] else 'CHECK':8s} | p3/p4 tangent-spectrum convergence",
        f"W5  | {data['classification']:45s} | overall",
        '',
        f"TANGENT NORMS: {data['tangent_norms']}",
        f"LAMBDA CONVERGENCE: {data['lambda_convergence']}",
        f"BATH FORCE: {data['bath_force_convergence_39_vs_47']}",
        f"FORCE PRECISION: {data['forcing_precision_convergence_p3_vs_p4']}",
        f"SPECTRUM PRECISION: {data['spectrum_precision_convergence_p3_vs_p4']}",
        f"ETA0 BASELINE: {data['eta0_baseline']}",
        '',
        'IMPORTANT: signed lambda scales the eta=0 tangent forcing only. It is not a physical negative eta model.',
        'Scope: unlensed TT/EE/TE tangent diagnostic; no likelihood or detectability claim.',
    ]
    Path('results/v019w_report.txt').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))

    with zipfile.ZipFile('results_bundle_v019w.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(Path('results').glob('v019w*')):
            if p.is_file(): z.write(p,p.name)
    print('Created results_bundle_v019w.zip')


if __name__=='__main__':
    main()
