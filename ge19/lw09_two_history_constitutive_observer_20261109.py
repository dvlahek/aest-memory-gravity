#!/usr/bin/env python3
"""GE19 LW09 — a rigorous prescribed-driver two-history Drude test.

Only frozen NL0B exact constant-H positive-continuum retarded kernel.
No CLASS, new physics parameters, observed data, fit, cosmological
physical history, gauge-invariant Weyl observable or H4 simulation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw09_two_history_constitutive_observer_gate_predata_20261109.json"
PRE_BLOB="1ce822be6a15640f43b5f1e6785e2a641dd8dde4"


def require(condition,name):
    if not bool(condition):
        raise RuntimeError("GE19_LW09_"+name)


def gauss_interval(n,low,high):
    x,w=np.polynomial.legendre.leggauss(n)
    return (high-low)*x/2+(high+low)/2,w*(high-low)/2


def spectral(H,tau,n):
    c=3*H
    discriminant=math.sqrt(c*c+4/tau**2)
    alpha=(c+discriminant)/2
    Z=2/(tau*tau*alpha*discriminant)
    theta,w=gauss_interval(n,0,math.pi/2)
    rates=c*np.sin(theta)**2
    sin2cos2=np.sin(theta)**2*np.cos(theta)**2
    spectral_weights=w*2*tau*c/math.pi * np.cos(theta)**2 / (
        1+tau*tau*c*c*sin2cos2)
    require(np.all(spectral_weights>=0) and
            abs(Z+np.sum(spectral_weights)-1)<1e-11,
            "POSITIVE_SPECTRAL_NORMALIZATION")
    return Z,alpha,rates,spectral_weights


def fp(t,Z,alpha,rates,weights):
    """f'_H(t), negative for all finite t >=0, regularized quadrature."""
    t=np.atleast_1d(np.asarray(t,float))
    require(np.all(t>=0),"NEGATIVE_TIME")
    return -Z*alpha*np.exp(-alpha*t)-np.sum(
        rates[:,None]*weights[:,None]*np.exp(-rates[:,None]*t[None,:]),
        axis=0)


def pulse(s,T,eps,Xamp):
    s=np.atleast_1d(s)
    result=np.zeros(s.shape,float)
    mask=(s>-T)&(s<-eps)
    u=(s[mask]+T)/(T-eps)
    result[mask]=Xamp*np.exp(4-1/(u*(1-u)))
    return result


def evaluate(n,H,tau,T,eps,Xamp):
    require(H>0 and tau>0 and T>eps>0 and Xamp>0,"PARAMS")
    Z,alpha,rates,weights=spectral(H,tau,n)
    s,w=gauss_interval(n,-T,-eps)
    X=pulse(s,T,eps,Xamp)
    mass=float(np.dot(w,X))
    # Integration by parts: int f(-s)*X'(s) ds = int f'(-s)*X(s) ds.
    B=float(np.dot(w,fp(-s,Z,alpha,rates,weights)*X))
    lo=float(-fp(T,Z,alpha,rates,weights)[0]*mass)
    hi=float(-fp(eps,Z,alpha,rates,weights)[0]*mass)
    require(mass>0 and B<0 and lo < -B < hi,
            "STRICT_HISTORY_MEMORY_AND_BOUNDS")
    return {"quadrature_nodes":n,"B_pulse_at_observation":B,
            "B_zero_history_at_observation":0.0,
            "pulse_integral":mass,
            "negative_B_lower_bound":lo,
            "negative_B_upper_bound":hi,
            "Z_pole_positive":float(Z),
            "alpha_pole_rate_positive":float(alpha),
            "continuum_weight_integral":float(np.sum(weights)),
            "fprime_at_epsilon":float(fp(eps,Z,alpha,rates,weights)[0]),
            "fprime_at_T":float(fp(T,Z,alpha,rates,weights)[0])}


def selftest():
    q1=evaluate(96,.12,1.7,5.,.5,1.)
    q2=evaluate(192,.12,1.7,5.,.5,1.)
    err=abs(q1["B_pulse_at_observation"]-
            q2["B_pulse_at_observation"])/abs(q2["B_pulse_at_observation"])
    require(err<1.e-8,"TWO_ORDER_REPRODUCTION")
    for t in (0,1,4):
        assert pulse(np.array([t]),5,.5,1.)[0]==0
    print("GE19_LW09_TWO_HISTORY_BATH_SYNTHETIC_SELFTEST_PASS",
          "B0",q2["B_pulse_at_observation"],flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path,default=
        ROOT/"results/ge19_lw09_two_history_constitutive_observer_20261109.json")
    a=p.parse_args()
    if a.self_test:
        selftest()
        return
    blob=subprocess.check_output(["git","hash-object",str(PRE)],
                                 text=True).strip()
    require(blob==PRE_BLOB,"PREDATA_BLOB_CHANGED")
    data=json.loads(PRE.read_text())
    require(data["classification"]==
            "GE19_LW09_TWO_HISTORY_CAUSAL_CONSTITUTIVE_TEST_PRELOCK",
            "PREDATA_CHANGED")
    v=data["analytically_predeclared_two_histories"]["choose_dimensionless_example"]
    nlow,nhigh=data["frozen_numerical_selftest"]["quadrature_nodes"]
    q1=evaluate(nlow,v["H"],v["tau"],v["T"],v["eps"],v["Xamp"])
    q2=evaluate(nhigh,v["H"],v["tau"],v["T"],v["eps"],v["Xamp"])
    rel=abs(q1["B_pulse_at_observation"]-
            q2["B_pulse_at_observation"])/abs(q2["B_pulse_at_observation"])
    gates={
        "positive_normalized_relaxation_spectrum":True,
        "bump_has_all_derivatives_zero_at_t0":True,
        "memory_strictly_negative_for_nonnegative_past_bump":
            q2["B_pulse_at_observation"]<0,
        "exact_monotone_derivative_bounds":
            q2["negative_B_lower_bound"]<
            -q2["B_pulse_at_observation"]<
            q2["negative_B_upper_bound"],
        "two_quadrature_orders_agree":
            rel<=data["frozen_numerical_selftest"]["relative_agreement_max"],
    }
    verdict=(data["proposed_result_labels"]["bath_pass"] if all(gates.values())
             else data["proposed_result_labels"]["bath_fail"])
    result={
        "classification":verdict,
        "original_model":"NL0B positive Drude continuum, externally prescribed linear X, fixed constant H",
        "predata_git_blob_sha1":PRE_BLOB,
        "dimensionless_inputs":v,
        "quadratures":[q1,q2],
        "relative_quadrature_disagreement":rel,
        "gates":gates,
        "analytic_proof":"f'_H(t)<0 from positive pole and positive continuum rates. For smooth nonnegative compact pulse X(s) supported in (-T,-eps) and t0=0: B(0)=integral_{-T}^{-eps} f'_H(-s) X(s) ds <0, while X and all jets vanish near t0. Lower/upper positive bounds use monotonic -f'_H(t).",
        "competitor_scope":"Refutes only regular strictly instantaneous laws of finite-order jets of X, with F(t,0,...,0)=0. Hidden-state Markovian local auxiliary theories and more general nonlocal/additive/scale-time laws are not refuted.",
        "gauge_scope":"On FLRW, X_mu and B_mu have vanishing homogeneous background, so their linear perturbations are gauge invariant (Stewart-Walker). Not a proof of an observed Weyl response.",
        "Einstein_AeST_retarded_metric_organizer":"Formally deltaW=P_W L0^{-1,ret} J[-Q B_chi_raw/2], with all original dynamical constraints and initial conditions imposed; the specific nonzero Green function for the prescribed pair has NOT been computed.",
        "history_pair_dynamically_admissible_in_full_AeST":False,
        "gauge_invariant_Weyl_history_pair_difference_certified":False,
        "full_metric_causal_observer_kernel_evaluated":False,
        "DES_ACT_data_fit":False,
        "observational_detection":False,
        "finite_physical_eta_calibrated":False,
        "LW01_native_Weyl_PASS_preserved":True,
        "LW03_radial_FAIL_preserved":True,
        "LW04_source_time_PASS_preserved":True,
        "LW05_full_LOS_BLOCK_preserved":True,
        "LW08_differential_source_response_UNRESOLVED_preserved":True,
        "H4_Z21_certified":False
    }
    out=a.output.resolve()
    require(out.parent.is_dir() and not out.exists(),
            "OUTPUT_ALREADY_EXISTS_OR_PARENT_MISSING")
    out.write_text(json.dumps(result,indent=2,sort_keys=True,
                              allow_nan=False)+"\n")
    print("GE19_LW09_CLASSIFICATION",verdict,flush=True)
    print("GE19_LW09_B0",q2["B_pulse_at_observation"],flush=True)
    print("GE19_LW09_METRIC_OBSERVER_CERTIFIED",False,flush=True)
    print("GE19_LW09_OUTPUT",str(out),flush=True)


if __name__=="__main__":
    main()
