#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math
import numpy as np


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input-dir',required=True); ap.add_argument('--json-out',required=True); z=ap.parse_args()
    inp=Path(z.input_dir)
    rows=[]
    for p in sorted(inp.glob('v058_eta_*.json')):
        d=json.loads(p.read_text()); rows.append((float(d['eta_fixed']),float(d['final_chi2']),d['final_state']))
    if len(rows)!=7: raise RuntimeError(f'expected 7 eta profile members, found {len(rows)}')
    rows.sort(key=lambda x:x[0]); eta=np.array([r[0] for r in rows]); chi=np.array([r[1] for r in rows])
    z0=np.where(np.isclose(eta,0.0))[0]
    if len(z0)!=1: raise RuntimeError('eta=0 profile member missing or duplicated')
    chi0=float(chi[z0[0]]); delta=chi-chi0
    ib=int(np.argmin(chi)); best_eta=float(eta[ib]); best_chi=float(chi[ib])
    order=np.argsort(np.abs(eta-best_eta))[:5]; order=np.sort(order)
    coeff=np.polyfit(eta[order],chi[order],2); a,b,c=[float(x) for x in coeff]
    if a>0:
        eta_hat=-b/(2*a); sigma=1/math.sqrt(a)
    else:
        eta_hat=None; sigma=None
    table=[]
    for e,q,d,s in zip(eta,chi,delta,[r[2] for r in rows]):
        table.append({'eta':float(e),'chi2':float(q),'delta_chi2_vs_eta0':float(d),'final_state':s})
    gates={
      'all_seven_members_present':len(rows)==7,
      'eta0_present':len(z0)==1,
      'all_chi2_finite':bool(np.all(np.isfinite(chi))),
      'local_quadratic_convex':bool(a>0),
      'best_grid_not_at_boundary':bool(ib not in (0,len(rows)-1))
    }
    res={
      'classification':'V058_PLANCK_ETA_PROFILE_COMPLETE' if all(gates.values()) else 'V058_PLANCK_ETA_PROFILE_FOLLOWUP',
      'eta_grid':eta.tolist(),'profile':table,'chi2_eta0':chi0,'best_grid_eta':best_eta,'best_grid_chi2':best_chi,
      'delta_chi2_improvement_best_grid':float(chi0-best_chi),
      'quadratic_local_fit':{'indices':order.tolist(),'eta_values':eta[order].tolist(),'a':a,'b':b,'c':c,'eta_hat':eta_hat,'sigma_eta':sigma,
                             'eta_hat_over_sigma':(eta_hat/sigma if eta_hat is not None and sigma else None)},
      'gates':gates,
      'scope':'Planck 2018 high-l TTTEEE plus low-l TT/EE fixed-eta profile with six LambdaCDM parameters plus A_planck refitted at every grid point; frozen v0.53 physics.',
      'note':'Profile likelihood only. The quadratic summary is diagnostic and does not replace a full posterior.'
    }
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not all(gates.values()): raise SystemExit(2)

if __name__=='__main__': main()
