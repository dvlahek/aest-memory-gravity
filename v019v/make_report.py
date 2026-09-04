#!/usr/bin/env python3
from pathlib import Path
import json,zipfile


def main():
    r=Path('results/v019v_tangent.json')
    data=json.loads(r.read_text())
    lines=[
      'AeST MEMORY EXP tauH0=1 TANGENT-LIMIT DIAGNOSTIC v0.19v',
      '='*88,
      f"V1  | {data['gate_status']:<8} | symmetric signed-eta tangent limit",
      f"V2  | {'PASS' if data['gates']['bath_order'] else 'CHECK':<8} | 39/47 bath-order derivative convergence",
      f"V3  | {'PASS' if data['gates']['precision'] else 'CHECK':<8} | p3/p4 derivative convergence",
      f"V4  | {data['classification']:<44} | overall",
      '',
      'TANGENT NORMS: '+repr(data['tangent_norms']),
      'H CONVERGENCE: '+repr(data['h_convergence']),
      'ODD SCALING: '+repr(data['odd_scaling']),
      'BATH ORDER: '+repr(data['bath_order_convergence']),
      'PRECISION: '+repr(data['precision_convergence']),
      'EVEN CONTAMINATION: '+repr(data['even_contamination_norms']),
      '',
      'IMPORTANT: negative eta is non-physical/non-passive and is used only as a numerical tangent diagnostic at eta=0.',
    ]
    txt='\n'.join(lines)+'\n'
    Path('results/v019v_report.txt').write_text(txt)
    print(txt)
    files=[p for p in Path('results').glob('v019v*') if p.is_file()]
    with zipfile.ZipFile('results_bundle_v019v.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.as_posix())
    print('Created results_bundle_v019v.zip')

if __name__=='__main__':main()
