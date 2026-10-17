#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

FD8_OFFSETS=np.arange(-4,5,dtype=float)
FD8_WEIGHTS=np.asarray([
    1/280,-4/105,1/5,-4/5,0,4/5,-1/5,4/105,-1/280
],dtype=float)
FD8_LEADING_K=1.0/630.0


def log_grid(rmax,n):
    r=np.geomspace(1.0,float(rmax),int(n))
    x=np.log(r)
    dx=np.diff(x)
    w=np.empty_like(r)
    w[0]=0.5*dx[0]
    w[-1]=0.5*dx[-1]
    w[1:-1]=0.5*(dx[:-1]+dx[1:])
    # dr = r d(log r); continuum measure dr/(1+r^2)
    mu=w*r/(1.0+r*r)
    return r,mu


def f_and_derivative(x,r,mu):
    # Smooth stiff continuum with state amplitude decaying as r^-2.
    # f_R(x)=int sin(r x)/r^2 * dr/(1+r^2)
    amp=mu/(r*r)
    f=np.sum(amp*np.sin(r*x))
    fp=np.sum((mu/r)*np.cos(r*x))
    return float(f),float(fp)


def ninth_abs_majorant(r,mu):
    # |d^9/dx^9 sin(rx)/r^2| <= r^7
    return float(np.sum(mu*r**7))


def fd8_derivative(x,h,r,mu):
    vals=[]
    for j in FD8_OFFSETS:
        f,_=f_and_derivative(x+j*h,r,mu)
        vals.append(f)
    return float(np.dot(FD8_WEIGHTS,np.asarray(vals))/h)


def run_case(rmax,h,x0,nq):
    r,mu=log_grid(rmax,nq)
    _,fp=f_and_derivative(x0,r,mu)
    d8=fd8_derivative(x0,h,r,mu)
    defect=abs(d8-fp)
    m9=ninth_abs_majorant(r,mu)
    taylor=FD8_LEADING_K*(h**8)*m9
    ratio=taylor/max(defect,1e-300)
    return {
        "rmax":float(rmax),
        "h":float(h),
        "nq":int(nq),
        "exact_derivative":fp,
        "fd8_derivative":d8,
        "actual_defect":defect,
        "M9_absolute_majorant":m9,
        "FD8_Taylor_bound_proxy":taylor,
        "bound_to_actual_ratio":ratio,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--h",type=float,default=1e-2)
    ap.add_argument("--x0",type=float,default=0.37)
    ap.add_argument("--nq",type=int,default=20000)
    ap.add_argument("--rmax",type=float,nargs="*",default=[10,30,100,300,1000])
    ap.add_argument("--csv",type=Path,default=None)
    args=ap.parse_args()

    rows=[run_case(R,args.h,args.x0,args.nq) for R in args.rmax]

    print("RMAX actual_defect taylor_bound bound/actual")
    for q in rows:
        print(
            f'{q["rmax"]:8.1f} '
            f'{q["actual_defect"]:.6e} '
            f'{q["FD8_Taylor_bound_proxy"]:.6e} '
            f'{q["bound_to_actual_ratio"]:.6e}'
        )

    if args.csv is not None:
        args.csv.parent.mkdir(parents=True,exist_ok=True)
        with args.csv.open("w",newline="") as f:
            wr=csv.DictWriter(f,fieldnames=list(rows[0]))
            wr.writeheader()
            wr.writerows(rows)
        print("WROTE",args.csv)


if __name__=="__main__":
    main()
