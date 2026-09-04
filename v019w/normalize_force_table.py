#!/usr/bin/env python3
from pathlib import Path
import argparse,json,math
from collections import defaultdict


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('raw')
    ap.add_argument('out')
    ap.add_argument('--json-out',default=None)
    args=ap.parse_args()

    raw=Path(args.raw)
    rows=[]
    for line in raw.read_text(errors='replace').splitlines():
        t=line.strip()
        if not t: continue
        p=t.split()
        if len(p)!=3: continue
        try:
            k,tau,f=map(float,p)
        except ValueError:
            continue
        if math.isfinite(k) and math.isfinite(tau) and math.isfinite(f) and k>0 and tau>=0:
            rows.append((k,tau,f))
    if not rows:
        raise RuntimeError(f'no valid forcing rows in {raw}')

    # perturbations_sources is normally called once per (k,tau), but keep this
    # robust against exact duplicates by averaging them.
    acc=defaultdict(lambda:[0.0,0])
    for k,tau,f in rows:
        key=(k,tau)
        acc[key][0]+=f
        acc[key][1]+=1
    clean=[(k,tau,s/n) for (k,tau),(s,n) in acc.items()]
    clean.sort(key=lambda x:(x[0],x[1]))

    out=Path(args.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w') as fp:
        for k,tau,f in clean:
            fp.write(f'{k:.17g} {tau:.17g} {f:.17g}\n')

    ks=sorted({k for k,_,_ in clean})
    taus=[tau for _,tau,_ in clean]
    fs=[f for *_,f in clean]
    counts=defaultdict(int)
    for k,_,_ in clean: counts[k]+=1
    stats={
        'raw_rows':len(rows),
        'unique_rows':len(clean),
        'k_count':len(ks),
        'k_min':min(ks),'k_max':max(ks),
        'tau_min':min(taus),'tau_max':max(taus),
        'force_l2':math.sqrt(sum(x*x for x in fs)),
        'force_max_abs':max(abs(x) for x in fs),
        'min_tau_points_per_k':min(counts.values()),
        'max_tau_points_per_k':max(counts.values()),
    }
    jout=Path(args.json_out) if args.json_out else out.with_suffix(out.suffix+'.json')
    jout.write_text(json.dumps(stats,indent=2))
    print(json.dumps(stats,indent=2))


if __name__=='__main__':
    main()
