#!/usr/bin/env python3
from pathlib import Path
import argparse, json


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()

    src=Path(args.input)
    d=json.loads(src.read_text())
    if d.get('classification')!='NL1C7A_NATIVE_TRACE_COVERAGE_PASS':
        raise RuntimeError('dense parent coverage is not PASS')
    r=d.get('repair01',{})
    required={
        'source_sampling_only':True,
        'perturbations_sampling_stepsize':0.025,
        'perturbations_integration_stepsize_overridden':False,
        'integration_tolerance_overridden':False,
        'interpolation_used':False,
        'nearest_neighbour_substitution_used':False,
    }
    for k,v in required.items():
        if r.get(k)!=v:
            raise RuntimeError(f'dense Repair01 metadata mismatch: {k}={r.get(k)!r}, expected {v!r}')
    before=json.dumps(d,sort_keys=True,separators=(',',':'))
    if 'repair05' in d:
        raise RuntimeError('compat field already present; refusing ambiguous rewrite')
    d['repair05']={'interpolation_used':r['interpolation_used']}
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')

    # Prove that deleting the compatibility alias gives byte-equivalent canonical JSON.
    check=json.loads(out.read_text())
    alias=check.pop('repair05')
    after=json.dumps(check,sort_keys=True,separators=(',',':'))
    if before!=after:
        raise RuntimeError('compatibility conversion altered dense coverage content')
    if alias!={'interpolation_used':False}:
        raise RuntimeError('unexpected compatibility alias content')
    print(json.dumps({
        'classification':'NL1C7A_REPAIR01_COVERAGE_METADATA_COMPAT_PASS',
        'source_coverage_classification':d['classification'],
        'compatibility_alias':alias,
        'dense_content_otherwise_identical':True,
        'physics_modified':False,
        'trace_modified':False,
        'science_gates_modified':False,
    },indent=2,sort_keys=True))

if __name__=='__main__':
    main()
