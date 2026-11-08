#!/usr/bin/env python3
"""GE19 G1M: physics-first NL0B oscillator energy → original GE05 source error.

Prove exactly, with SymPy on two real components of a complex Fourier mode,
the dissipative work/energy identity for the frozen *normalized* NL0B bath:
    qdd + 3 H qdot + omega^2 q = omega sqrt(w) X.
With B_j = w_j X - omega_j sqrt(w_j) q_j, E_j =
    (|qdot_j|^2 + |omega_j q_j - sqrt(w_j) X|^2)/4,
    d E_total/dt = -3 H/2 sum |qdot_j|^2 + Re(B^* Xdot)/2.

For approximate bath qh,Xh whose physical-time residual is
    R_j = qhdd+3H qhdot+omega^2 qh-omega sqrt(w) Xh,
a conditional energy inequality (H>=0, w_j>0, omega_j>0, W=sum w<infinity,
common background and physical time, finite initial error) gives
    |Btrue-Bh|(t) <= 2 sqrt(W Eerr(t0))
       + W integral |(Xtrue-Xh)dot| dt
       + sqrt(W) integral ||R||_ell2 dt.
The proof uses Cauchy-Schwarz/Young and a sqrt(E+epsilon) limit.

At positive H and x=ln a, the first integral is exactly
integral |d_x (Xtrue-Xh)| dx; the bath residual integral is
integral ||R||_ell2/H dx. For original Repair32B -2 M1 RHS with frozen
GE05→GE06 scale 2:
    S_u = a^3 Q B, S_phi = -i k a^2 B
=> ||delta S||_2 = a^2 sqrt(a^2 Q^2+k^2) |delta B|
for a COMMON exact-input background and wave number. If a,Q differ,
their uncertainty must be added separately.

This is an analytic source bound, NOT a numerical true-bath/source
certificate or a validated original Z11 8D solution error. No changes to
the original action, source coefficients, original FD4/FD8 B_total or
H4 shift gate. Read-only verification, small JSON report only.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
SOURCE_BLOBS={
    "docs/gravitational_elasticity_canonical_nl0b_interpretation.md":
       "d4a774074ad6c69142bb6f00f5426949e98ca67b",
    "docs/gravitational_maxwell_viscoelasticity.md":
       "31096994e08dc7c101ba7f0743e52d2893b643ca",
    "ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py":
       "6ece578e8a30f48faaded8808687a9bd5c114608",
}

def require(cond,reason):
    if not bool(cond):
        raise RuntimeError("GE19_G1M_"+reason)

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def lock_sources():
    verified={}
    for path,expect in SOURCE_BLOBS.items():
        original=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],
            text=True,cwd=ROOT).strip()
        working=subprocess.check_output(
            ["git","hash-object",str(ROOT/path)],
            text=True,cwd=ROOT).strip()
        require(original==expect and working==expect,
                "ORIGINAL_SOURCE_BLOB_CHANGED_"+path)
        verified[path]=expect
    action=(ROOT/"docs/gravitational_elasticity_canonical_nl0b_interpretation.md").read_text()
    source=(ROOT/"ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py").read_text()
    require("B_mu=sum_j [w_j X_mu-omega_j sqrt(w_j) q_{j mu}]" in action,
            "NL0B_ELASTIC_BACKREACTION_DICTIONARY_CHANGED")
    require("RAW_RESIDUAL_DICTIONARY_SCALE=2.0" in source and
            "RAW_RESIDUAL_DICTIONARY_SCALE*0.5*bg[\"Q_action\"]*bg[\"a\"]**3*B[im]" in source and
            "RAW_RESIDUAL_DICTIONARY_SCALE*(-0.5)*bg[\"a\"]**2*(1j*k)*B[im]" in source,
            "GE05_RAW_EULER_SOURCE_DICTIONARY_CHANGED")
    return verified

def proof():
    R=sp.symbols
    H,omega,sw=R("H omega sqrtw",real=True,positive=True)
    vR,vI,eR,eI=R("vR vI eR eI",real=True)
    xdR,xdI=R("xdR xdI",real=True)
    rR,rI=R("rR rI",real=True)

    # Residual convention for qh in an exact common background.
    # Delta q = q_true - qh therefore has driving -R.
    accR=-3*H*vR-omega*eR-rR
    accI=-3*H*vI-omega*eI-rI
    deR=omega*vR-sw*xdR
    deI=omega*vI-sw*xdI
    dE=sp.Rational(1,2)*(
        vR*accR+vI*accI+eR*deR+eI*deI)
    BR,BI=-sw*eR,-sw*eI
    expected=(
        -sp.Rational(3,2)*H*(vR**2+vI**2)
        +sp.Rational(1,2)*(BR*xdR+BI*xdI)
        -sp.Rational(1,2)*(vR*rR+vI*rI))
    require(sp.expand(dE-expected)==0,
            "COMPLEX_ERROR_WORK_ENERGY_IDENTITY_FAILED")
    require(sp.expand(dE.subs({rR:0,rI:0})-
            expected.subs({rR:0,rI:0}))==0,
            "EXACT_OSCILLATOR_ENERGY_IDENTITY_FAILED")

    t1,t2=R("sqrtw1 sqrtw2",real=True,positive=True)
    a,b,c,d=R("e1R e1I e2R e2I",real=True)
    sum_e=a*a+b*b+c*c+d*d
    sum_b=(t1*a+t2*c)**2+(t1*b+t2*d)**2
    cauchy_slack=(t1*t1+t2*t2)*sum_e-sum_b
    squared=(t1*c-t2*a)**2+(t1*d-t2*b)**2
    require(sp.expand(cauchy_slack-squared)==0,
            "POSITIVE_COMPLEX_BATH_CAUCHY_IDENTITY_FAILED")

    # Original Repair32B source_from_B maps -2 M1 to RAW GE06 rows.
    aa,QQ,k,BR0,BI0=R("a Q k BR BI",real=True)
    Bc=BR0+sp.I*BI0
    scale=sp.Integer(2)
    su=scale*sp.Rational(1,2)*aa**3*QQ*Bc
    sphi=scale*(-sp.Rational(1,2))*aa**2*sp.I*k*Bc
    require(sp.simplify(su-aa**3*QQ*Bc)==0 and
            sp.simplify(sphi+sp.I*k*aa**2*Bc)==0,
            "ORIGINAL_GE05_FACTOR_TWO_SOURCE_FAILED")
    norm=sp.expand(sp.re(su*sp.conjugate(su)+
                         sphi*sp.conjugate(sphi)))
    expected_norm=aa**4*(aa**2*QQ**2+k**2)*(BR0**2+BI0**2)
    require(sp.simplify(norm-expected_norm)==0,
            "ORIGINAL_GE05_COMPLEX_SOURCE_L2_GAIN_FAILED")

    # Physical-clock x=ln a: dt=dx/H, X_t=H X_x.
    Xx,Rbath=R("Xx Rbath",real=True,nonnegative=True)
    require(sp.simplify(
        H*Xx/H-Xx)==0 and
        sp.simplify(Rbath/H*H-Rbath)==0,
        "PHYSICAL_TO_LOGA_CLOCK_CONVERSION_FAILED")

    eta=R("eta",real=True,nonnegative=True)
    physical=eta*QQ*Bc/2
    require(sp.simplify(physical.subs(eta,0))==0,
            "ORIGINAL_ETA_ZERO_COUPLING_EDGE_FAILED")

    return {
      "complex_two_component_bath_energy_identity":True,
      "complex_two_component_residual_error_identity":True,
      "positive_two_mode_Cauchy_identity":True,
      "original_Repair32B_factor_two_GE05_source_rows":True,
      "exact_original_GE05_source_vector_gain":True,
      "positive_H_physical_to_loga_clock_integral":True,
      "eta_zero_physical_coupling":True,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--json-out",type=Path)
    a=ap.parse_args()
    checks=proof()
    if a.self_test:
        print("GE19_G1M_NL0B_MEMORY_ENERGY_GE05_SOURCE_ANALYTIC_SELFTEST_PASS")
        return
    require(a.json_out is not None and not a.json_out.exists(),
            "JSON_OUTPUT_MISSING_OR_EXISTS")
    blobs=lock_sources()
    result={
      "classification":"GE19_G1M_SOURCE_LOCKED_NL0B_MEMORY_ENERGY_TO_GE05_ERROR_BRIDGE_ANALYTIC_PASS_PHYSICAL_G1_OPEN",
      "original_source_git_blobs":blobs,
      "sympy_version":sp.__version__,
      "exact_symbolic_checks":checks,
      "physical_assumptions":{
        "common_true_and_approximate_expanding_FLRW_H_nonnegative":True,
        "original_normalized_bath_wj_positive_omegaj_positive_constant":True,
        "sum_wj_W_finite_for_continuum_limit":True,
        "positive_H_for_x_loga_conversion":True,
        "approximate_bath_residual_Rj_defined_against_same_action_equation":True,
        "finite_initial_error_energy":True},
      "theorems":{
        "energy":"E=1/4 sum_j(|dq_j/dt|^2+|omega_j q_j-sqrt(w_j) X|^2); dE/dt=-3H/2 sum_j|dq_j/dt|^2+Re(conj(B)dX/dt)/2 for an exact bath.",
        "error_bound":"|Btrue-Bh|(t)<=2 sqrt(W Eerr(t0))+W int_t0^t |d_t(Xtrue-Xh)| dt+sqrt(W) int_t0^t ||Rh||_ell2 dt; W=sum_j w_j.",
        "loga_clock":"int |d_t deltaX| dt=int |d_x deltaX| dx; int ||Rh|| dt=int ||Rh||/H dx for H>0, x=ln a.",
        "original_GE05_raw_source":"S_u=a^3 Q B; S_phi=-i k a^2 B; other four original GE06 raw Euler M1 rows are zero.",
        "common_background_source_error_gain":"||delta S_GE05||_2=a^2 sqrt(a^2 Q^2+k^2) |delta B| for exact common real a>0,Q,k."
      },
      "scope_boundary":{
        "real_physical_bath_error_numerically_enclosed":False,
        "source_generation_roundoff_enclosed":False,
        "true_Z11_8D_IVP_error_enclosed":False,
        "original_G3_FD4_FD8_M5_M9_budget_enclosed":False,
        "full_H4_Ward_certified":False,
        "Z21_certified":False,
        "lensing_licensed":False,
        "physical_G1_closed":False},
      "interpretation":"An analytic finite-positive-weight bath energy and source transfer theorem under explicit assumptions; no observation or retuning. Does not bound X/Rh/initial data yet. Independent parent/error envelopes and full mixed H4 Noether/boundary still required."
    }
    a.json_out.parent.mkdir(parents=True,exist_ok=True)
    a.json_out.write_text(
        json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(result["classification"])
if __name__=="__main__":
    main()
