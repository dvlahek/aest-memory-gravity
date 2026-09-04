#!/usr/bin/env python3
from pathlib import Path
import argparse,json


def replace_once(path,old,new,label):
    p=Path(path);s=p.read_text();n=s.count(old)
    if n != 1:
        raise RuntimeError(f'{label}: expected one anchor, found {n} in {p}')
    p.write_text(s.replace(old,new,1))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('class_root');args=ap.parse_args()
    root=Path(args.class_root).resolve();repo=Path(__file__).resolve().parents[1]

    # This is a diagnostic tree only. Negative eta is non-passive and is used solely
    # for a symmetric numerical derivative at eta=0. Physical production runs keep
    # the v0.19j eta>=0 guard.
    replace_once(root/'source'/'input.c',
'''  class_test(pba->aest_eta < 0.,errmsg,"AeST memory requires aest_eta >= 0");\n''',
'''  /* v0.19v tangent-limit diagnostic: allow a small signed eta only in this\n     disposable test tree. Negative eta is not a physical/passive model. */\n  class_test(fabs(pba->aest_eta) > 0.05,errmsg,\n             "v0.19v tangent probe requires |aest_eta| <= 0.05");\n''','signed eta diagnostic guard')

    txt=(root/'source'/'input.c').read_text()
    checks={
      'signed_probe_guard':'v0.19v tangent probe requires |aest_eta| <= 0.05' in txt,
      'physical_nonnegative_guard_removed':'AeST memory requires aest_eta >= 0' not in txt,
      'tau1_bath_guard':'validated only for aest_tau_H0 = 1' in txt,
    }
    report={
      'classification':'SIGNED_ETA_TANGENT_LIMIT_DIAGNOSTIC_PATCH',
      'physical_negative_eta':False,
      'purpose':'central derivative at eta=0 only',
      'eta_abs_max':0.05,
      'checks':checks,
    }
    if not all(checks.values()):raise RuntimeError(report)
    (repo/'results').mkdir(exist_ok=True)
    (repo/'results'/'v019v_apply_report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
