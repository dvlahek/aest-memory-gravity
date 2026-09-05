#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math


def stats(x):
    x=[float(v) for v in x if math.isfinite(float(v))]
    if not x: return {'n':0,'rms':None,'max_abs':None,'median_abs':None}
    ax=sorted(abs(v) for v in x)
    return {
        'n':len(x),
        'rms':math.sqrt(sum(v*v for v in x)/len(x)),
        'max_abs':max(ax),
        'median_abs':ax[len(ax)//2]
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('trace')
    ap.add_argument('force')
    ap.add_argument('--kb',type=float,required=True)
    ap.add_argument('--json-out',required=True)
    a=ap.parse_args()

    rows=[]
    with open(a.trace) as f:
        for line in f:
            t=line.strip()
            if not t or t.startswith('k '): continue
            p=t.split()
            if len(p)<6: continue
            k,tau,aa,H,chi,Q=map(float,p[:6])
            rows.append((k,tau,aa,H,chi,Q))

    force=[]
    with open(a.force) as f:
        for line in f:
            t=line.strip()
            if not t or t.startswith('#'): continue
            p=t.split()
            if len(p)<3: continue
            force.append(float(p[2]))

    if len(force)!=len(rows):
        raise RuntimeError(f'trace/force sample mismatch {len(rows)} vs {len(force)}')

    bins={
      'very_early':lambda aa: aa<3e-4,
      'recombination_window':lambda aa: 3e-4<=aa<3e-3,
      'post_recombination':lambda aa: 3e-3<=aa<3e-2,
      'late':lambda aa: aa>=3e-2,
    }

    outbins={}
    for name,fn in bins.items():
        idx=[i for i,r in enumerate(rows) if fn(r[2])]
        chis=[rows[i][4] for i in idx]
        x=[rows[i][4]/rows[i][2] for i in idx]
        fs=[force[i] for i in idx]
        outbins[name]={
          'chi':stats(chis),
          'chi_over_a':stats(x),
          'force_Eprime_per_eta':stats(fs),
          'KB_times_force':stats([a.kb*v for v in fs]),
        }

    fs=stats(force)
    kbf=stats([a.kb*v for v in force])
    res={
      'classification':'V035_KB_FORCING_SCALING_DIAGNOSTIC',
      'KB':a.kb,
      'samples':len(rows),
      'all_samples':{
        'chi':stats([r[4] for r in rows]),
        'chi_over_a':stats([r[4]/r[2] for r in rows]),
        'force_Eprime_per_eta':fs,
        'KB_times_force':kbf,
      },
      'epoch_bins':outbins,
      'interpretation_note':'If force grows approximately as 1/KB while KB*force stays smooth, amplification is mainly explicit kinetic prefactor. If KB*force also rises sharply, the eta0 AeST state/history Bchi is itself becoming amplified.'
    }
    Path(a.json_out).write_text(json.dumps(res,indent=2))
    print(json.dumps(res,indent=2))

if __name__=='__main__': main()
