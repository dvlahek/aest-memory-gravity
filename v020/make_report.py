#!/usr/bin/env python3
from pathlib import Path
import json, zipfile

p=Path('results/v020_analysis.json')
r=json.loads(p.read_text())
lines=[]
lines.append('AeST MEMORY v0.20 CORE-LambdaCDM REVOLUTION GATE')
lines.append('='*78)
lines.append(f"classification: {r['classification']}")
lines.append(f"memory tangent control: {r['memory_control']}")
lines.append(f"nuisance basis rank: {r['nuisance_basis_rank']}")
lines.append(f"raw CV S/N per unit eta: {r['raw_CV_SNR_per_unit_eta']:.12g}")
lines.append(f"marginalized CV S/N per unit eta: {r['marginalized_CV_SNR_per_unit_eta']:.12g}")
lines.append(f"CV retained fraction after core-LambdaCDM projection: {r['CV_retained_fraction_after_core_LCDM_projection']:.8g}")
lines.append(f"peak-normalized Euclidean retained fraction: {r['peak_normalized_Euclidean_retained_fraction']:.8g}")
lines.append(f"eta for CV S/N=1: {r['eta_for_CV_SNR_1']}")
lines.append(f"eta for CV S/N=3: {r['eta_for_CV_SNR_3']}")
lines.append('')
lines.append('nuisance derivative stability:')
for k,v in r['nuisance_derivative_stability'].items(): lines.append(f"  {k}: {v}")
lines.append('')
lines.append('memory vs nuisance CV cosines:')
for k,v in r['memory_vs_parameter_CV_cosines'].items(): lines.append(f"  {k}: {v:.10g}")
lines.append('')
lines.append('band S/N per unit eta:')
for k,v in r['band_SNR_per_unit_eta'].items(): lines.append(f"  {k}: {v}")
lines.append('')
lines.append('gates: '+str(r['gates']))
lines.append('scope: '+r['scope'])
Path('results/v020_report.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))

with zipfile.ZipFile('results_bundle_v020.zip','w',zipfile.ZIP_DEFLATED) as z:
    for q in Path('results').glob('v020*'):
        if q.is_file(): z.write(q,q.as_posix())
print('Created results_bundle_v020.zip')
