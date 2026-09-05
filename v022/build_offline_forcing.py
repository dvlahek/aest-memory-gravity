#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math
from collections import defaultdict
import numpy as np
from scipy.special import roots_legendre

TAUS = [
    ('t0001',0.001),('t0003',0.003),('t001',0.01),('t003',0.03),
    ('t01',0.1),('t03',0.3),('t1',1.0),('t3',3.0),('t10',10.0),
]
_NODE_CACHE = {}


def tan_gl_nodes(n):
    n = int(n)
    if n not in _NODE_CACHE:
        z,w = roots_legendre(n)
        theta = 0.25*np.pi*(z+1.0)
        _NODE_CACHE[n] = (np.tan(theta),0.5*w)
    return _NODE_CACHE[n]


def _step_linear(q,v,omega,h,x0,x1,dt):
    # Exact propagation for z_xixi + 3 h z_xi + omega^2 z = omega^2 x(xi),
    # with frozen h and linearly varying x over one interval. This is the
    # cancellation-safe v0.19r propagator, now applied to x=chi/a, which is
    # algebraically equivalent to the CLASS q_j bath used in v0.19j/v0.21.
    c = 3.0*h
    d = 0.5*c
    r = (x1-x0)/dt
    u0 = q-x0
    vu0 = v-r
    force = -c*r
    om2 = omega*omega
    disc = om2-d*d
    scale = np.maximum(om2+d*d,1.0)
    under = disc > 1.e-12*scale
    over = disc < -1.e-12*scale
    crit = ~(under|over)
    un = np.empty_like(q)
    vn = np.empty_like(v)

    if np.any(under):
        O = np.sqrt(disc[under]); z = O*dt; ed = np.exp(-d*dt)
        C = np.cos(z); S = np.sin(z)
        uu = u0[under]; vv = vu0[under]; oo2 = om2[under]
        hu = ed*(uu*C+(vv+d*uu)/O*S)
        hv = ed*(vv*C-(d*vv+oo2*uu)/O*S)
        one = 1.0-ed*(C+d/O*S)
        G = ed*S/O
        un[under] = hu+force/oo2*one
        vn[under] = hv+force*G

    if np.any(over):
        oo2 = om2[over]; delta = np.sqrt(-disc[over])
        lam1 = -oo2/(d+delta)
        lam2 = -d-delta
        den = lam1-lam2
        e1 = np.exp(lam1*dt); e2 = np.exp(lam2*dt)
        uu = u0[over]; vv = vu0[over]
        c1 = (vv-lam2*uu)/den
        c2 = (lam1*uu-vv)/den
        hu = c1*e1+c2*e2
        hv = lam1*c1*e1+lam2*c2*e2
        one = (-lam2*(-np.expm1(lam1*dt))+lam1*(-np.expm1(lam2*dt)))/den
        G = (e1-e2)/den
        un[over] = hu+force/oo2*one
        vn[over] = hv+force*G

    if np.any(crit):
        oo2 = om2[crit]; z = d*dt; ed = np.exp(-z)
        uu = u0[crit]; vv = vu0[crit]
        hu = ed*(uu+(vv+d*uu)*dt)
        hv = ed*(vv-(d*vv+oo2*uu)*dt)
        one = -np.expm1(-z)-z*ed
        G = ed*dt
        un[crit] = hu+force/oo2*one
        vn[crit] = hv+force*G

    return x1+un, vn+r


def simulate_response(N,H,x,tauH0,n):
    omega,weights = tan_gl_nodes(n)
    q = np.zeros(int(n)); v = np.zeros(int(n))
    out = np.empty(len(N))
    out[0] = x[0]  # q_j=0 regular initial condition
    hgrid = H*tauH0
    for i in range(len(N)-1):
        dN = N[i+1]-N[i]
        if not (dN > 0):
            out[i+1] = out[i]
            continue
        hm = math.sqrt(hgrid[i]*hgrid[i+1])
        dt = dN/hm
        q,v = _step_linear(q,v,omega,hm,x[i],x[i+1],dt)
        out[i+1] = x[i+1]-float(np.dot(weights,q))
    return out


def read_trace(path):
    groups = defaultdict(list)
    with open(path,'r',errors='replace') as f:
        for line in f:
            p=line.strip().split()
            if len(p) != 6: continue
            try:
                k,tau,a,H,chi,Q = map(float,p)
            except ValueError:
                continue
            if not all(math.isfinite(z) for z in (k,tau,a,H,chi,Q)): continue
            if k<=0 or tau<0 or a<=0 or H<=0: continue
            groups[k].append((tau,a,H,chi,Q))
    if not groups:
        raise RuntimeError('no valid v0.22 trace rows')

    clean = {}
    for k,rows in groups.items():
        # Collapse exact duplicate (k,tau) evaluations by averaging. Sorting
        # removes rejected-step/backtracking order from the adaptive solver.
        acc = defaultdict(lambda:[0.,0.,0.,0.,0])
        for tau,a,H,chi,Q in rows:
            v=acc[tau]; v[0]+=a; v[1]+=H; v[2]+=chi; v[3]+=Q; v[4]+=1
        seq=[]
        for tau,(sa,sH,sc,sQ,n) in acc.items():
            seq.append((tau,sa/n,sH/n,sc/n,sQ/n))
        seq.sort(key=lambda r:r[0])
        # Enforce strictly increasing a as a second monotonicity guard.
        good=[]; last_a=-1.
        for r in seq:
            if r[1] > last_a*(1.+1e-14):
                good.append(r); last_a=r[1]
        if len(good)>=8:
            clean[k]=good
    if len(clean)<20:
        raise RuntimeError(f'too few usable k histories: {len(clean)}')
    return clean


def rel_cos(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    nb=np.linalg.norm(bb); na=np.linalg.norm(aa)
    return float(np.linalg.norm(aa-bb)/max(nb,1e-300)), float(np.dot(aa,bb)/max(na*nb,1e-300))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('trace')
    ap.add_argument('--out-dir',default='results')
    ap.add_argument('--KB',type=float,default=0.1)
    ap.add_argument('--control-order',type=int,default=512)
    ap.add_argument('--primary-order',type=int,default=1024)
    ap.add_argument('--summary',default=None)
    args=ap.parse_args()
    out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    histories=read_trace(args.trace)

    summary={'classification':'V022_OFFLINE_EXACT_DRUDE_CONTINUUM','KB':args.KB,
             'control_order':args.control_order,'primary_order':args.primary_order,
             'k_histories':len(histories),'tau_points':{},
             'derivation':{
               'class_bath':'u_j_ddot + 3H u_j_dot + omega_j^2 u_j = (k omega_j/a) chi',
               'offline_variable':'z_j=(omega_j/k)u_j',
               'offline_equation':'z_j_ddot + 3H z_j_dot + omega_j^2 z_j = omega_j^2 chi/a',
               'closure':'B_raw = chi - a <z>_mu',
               'variational_force':'f_E = -a Q B_raw/(2 KB)'
             }}

    for tag,T in TAUS:
        rows_primary=[]; rows_control=[]
        allp=[]; allc=[]; per_k=[]
        for k in sorted(histories):
            seq=histories[k]
            ct=np.array([r[0] for r in seq],float)
            a=np.array([r[1] for r in seq],float)
            H=np.array([r[2] for r in seq],float)
            chi=np.array([r[3] for r in seq],float)
            Q=np.array([r[4] for r in seq],float)
            N=np.log(a); x=chi/a
            rc=simulate_response(N,H,x,T,args.control_order)
            rp=simulate_response(N,H,x,T,args.primary_order)
            # B_raw = a * (chi/a - <z>); f_E = -a Q B_raw/(2 KB).
            fc=-0.5*a*a*Q*rc/args.KB
            fp=-0.5*a*a*Q*rp/args.KB
            rr,cc=rel_cos(fc,fp)
            per_k.append((k,rr,cc,len(seq)))
            for ti,ui,vi in zip(ct,fc,fp):
                rows_control.append((k,ti,ui)); rows_primary.append((k,ti,vi))
            allc.extend(fc.tolist()); allp.extend(fp.tolist())

        rel,cos=rel_cos(allc,allp)
        # Ignore essentially zero-force histories when quoting worst per-k L2.
        finite_rel=[r[1] for r in per_k if math.isfinite(r[1]) and r[1] < 1e6]
        min_cos=min(r[2] for r in per_k if math.isfinite(r[2]))
        p95=float(np.quantile(np.asarray(finite_rel),0.95)) if finite_rel else None
        maxrel=max(finite_rel) if finite_rel else None
        force_path=out/f'v022_{tag}_force.dat'
        with force_path.open('w') as f:
            for k,t,v in rows_primary:
                f.write(f'{k:.17g} {t:.17g} {v:.17g}\n')
        ctrl_path=out/f'v022_{tag}_force_control.dat'
        with ctrl_path.open('w') as f:
            for k,t,v in rows_control:
                f.write(f'{k:.17g} {t:.17g} {v:.17g}\n')
        summary['tau_points'][tag]={
            'tauH0':T,'global_relative_L2_control_vs_primary':rel,'global_cosine':cos,
            'per_k_relative_L2_p95':p95,'per_k_relative_L2_max':maxrel,
            'per_k_min_cosine':min_cos,'samples':len(rows_primary),
            'force_file':str(force_path),
            'gate':bool(rel<0.01 and cos>0.9999),
        }
        print(tag,T,rel,cos,p95,maxrel,min_cos,len(rows_primary),flush=True)

    summary['all_tau_quadrature_gate']=all(x['gate'] for x in summary['tau_points'].values())
    q=Path(args.summary) if args.summary else out/'v022_offline_forcing_summary.json'
    q.write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
