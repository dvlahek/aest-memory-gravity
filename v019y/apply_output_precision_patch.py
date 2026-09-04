#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re


def replace_once(path,old,new,label):
    p=Path(path);s=p.read_text();n=s.count(old)
    if n!=1: raise RuntimeError(f'{label}: expected one anchor, found {n} in {p}')
    p.write_text(s.replace(old,new,1))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('class_root');args=ap.parse_args()
    root=Path(args.class_root).resolve();repo=Path(__file__).resolve().parents[1]
    common=root/'include'/'common.h'
    replace_once(common,
                 '#define _OUTPUTPRECISION_ 12 /**< Number of significant digits in some output files */',
                 '#define _OUTPUTPRECISION_ 17 /**< Number of significant digits in some output files */',
                 'output precision')
    replace_once(common,
                 '#define _COLUMNWIDTH_ 24 /**< Must be at least _OUTPUTPRECISION_+8 for guaranteed fixed width columns */',
                 '#define _COLUMNWIDTH_ 28 /**< Must be at least _OUTPUTPRECISION_+8 for guaranteed fixed width columns */',
                 'column width')
    txt=common.read_text()
    checks={
      'output_precision_17':'#define _OUTPUTPRECISION_ 17' in txt,
      'column_width_28':'#define _COLUMNWIDTH_ 28' in txt,
      'old_precision_absent':'#define _OUTPUTPRECISION_ 12' not in txt,
    }
    report={
      'classification':'CLASS_HIGH_OUTPUT_PRECISION_PATCH',
      'physics_modified':False,
      'solver_tolerances_modified':False,
      'output_precision_digits':17,
      'column_width':28,
      'checks':checks,
    }
    if not all(checks.values()): raise RuntimeError(report)
    (repo/'results').mkdir(exist_ok=True)
    (repo/'results'/'v019y_output_precision_patch.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
