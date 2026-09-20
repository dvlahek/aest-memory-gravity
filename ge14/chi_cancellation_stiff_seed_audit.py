#!/usr/bin/env python3
"""GE14 diagnostic audit of the frozen GE11 chi-cancellation stiff seed.

No CLASS execution. Uses the first accepted endpoint of each frozen R1/R2 mode.
"""
from __future__ import annotations

import argparse, hashlib, json, math
from pathlib import Path

import numpy as np

KB=0.0665
H0_CLASS=67.3324639084866/299792.458
C_EPS=np.finfo(float).eps
ARTIFACT_ID=10600652596
ARTIFACT_DIGEST="sha256:b35a3a0c8bbd22483bd04c006b20ceb97d3c7f263e178382026cba2983628ecc"
R1_SHA="c50aae91fee94f00e1cbb5bd3c4d9352f15d892e91b230fad690f06c43e25fbd"
R2_SHA="5a9480f69744db59ab8ca7fbdef56398c5fe38493730976d92b25873f46379b1"
TINY=1e-300


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_rows(path):
    lines=Path(path).read_text().splitlines()
    hdr=lines[0].split()
    out=[]
    for ln in lines[1:]:
        vals=ln.split()
        if len(vals)!=len(hdr):
            continue
        row={k:float(v) for k,v in zip(hdr,vals)}
        if all(np.isfinite(list(row.values()))):
            out.append(row)
    if not out:
        raise RuntimeError(f"empty trace {path}")
    return out


def unique_find(root,name):
    hits=sorted(p for p in Path(root).rglob(name) if p.is_file())
    if len(hits)!=1:
        raise RuntimeError(f"expected exactly one {name}, found {len(hits)}")
    return hits[0]


def first_by_k(rows):
    out={}
    for r in rows:
        k=r["k"]
        if k not in out or r["tau"]<out[k]["tau"]:
            out[k]=r
    return [out[k] for k in sorted(out)]


def aor_scalar(a,b):
    ae=abs(a-b)
    re=ae/max(abs(a),abs(b),TINY)
    return min(ae,re)


def diagnostics(row):
    k=row["k"]; a=row["a"]; Q=row["Q"]
    H=row["H_over_H0"]*H0_CLASS
    calH=a*H
    rho=row["rho_dark"]; p=row["p_dark"]; cad2=row["cad2_dark"]
    w=p/rho
    theta=row["theta_dark"]; alpha=row["alpha_aest"]; E=row["E_aest"]
    delta=row["delta_dark"]

    v=a*theta/(k*k)
    s=v+alpha
    chi=Q*s
    KQ=3.0*(rho+p)/Q
    Pi=cad2*delta + cad2*k*k/(3.0*a*a*rho)*(KB*E+(2.0-KB)*chi)

    T_stiff=(a/KB)*KQ*chi
    T_pressure=-(a/KB)*(2.0-KB)*Q*Pi/(1.0+w)
    T_HQchi=-(a/KB)*(2.0-KB)*(H+Q)*chi
    T_alpha=(a/KB)*(2.0-KB)*3.0*cad2*H*Q*alpha
    T_damp=-calH*E
    Eprime_reconstructed=T_stiff+T_pressure+T_HQchi+T_alpha+T_damp

    S=delta/(1.0+w)-3.0*H*alpha
    T_grad=-(a/KB)*(2.0-KB)*Q*cad2*S

    eps_units=abs(s)/(C_EPS*max(abs(v),abs(alpha),TINY))
    stiff_rel_err=abs(T_stiff-row["E_aest_prime"])/max(abs(row["E_aest_prime"]),TINY)
    full_aor=aor_scalar(Eprime_reconstructed,row["E_aest_prime"])
    grad_over_stiff=abs(T_grad)/max(abs(T_stiff),TINY)

    return {
        "k_Mpc":k,
        "a":a,
        "tau":row["tau"],
        "k_over_aH":k/max(calH,TINY),
        "v_a_theta_over_k2":v,
        "alpha_aest":alpha,
        "cancellation_residual_s":s,
        "chi":chi,
        "machine_epsilon_units":eps_units,
        "KQ":KQ,
        "Pi":Pi,
        "comoving_density_bracket":S,
        "E_aest":E,
        "E_aest_prime_trace":row["E_aest_prime"],
        "Eprime_terms":{
            "stiff_KQ_chi":T_stiff,
            "pressure":T_pressure,
            "H_plus_Q_chi":T_HQchi,
            "cad2_H_alpha":T_alpha,
            "damping":T_damp,
            "finite_gradient_direct":T_grad,
        },
        "Eprime_reconstructed":Eprime_reconstructed,
        "stiff_vs_trace_relative_error":stiff_rel_err,
        "full_Eprime_reconstruction_abs_or_rel_error":full_aor,
        "finite_gradient_over_stiff_abs_ratio":grad_over_stiff,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact-root",required=True)
    ap.add_argument("--artifact-meta-json",required=True)
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()

    meta=json.loads(Path(args.artifact_meta_json).read_text())
    artifact_ok=bool(
        int(meta.get("id",-1))==ARTIFACT_ID
        and meta.get("digest")==ARTIFACT_DIGEST
        and meta.get("expired") is False
    )

    r1=unique_find(args.artifact_root,"ge11r1_R1_dense_accepted_step_trace.dat")
    r2=unique_find(args.artifact_root,"ge11r1_R2_dense_accepted_step_trace.dat")
    hashes_ok=bool(sha256(r1)==R1_SHA and sha256(r2)==R2_SHA)

    rows1=first_by_k(read_rows(r1))
    rows2=first_by_k(read_rows(r2))
    modes_ok=bool(len(rows1)==6 and len(rows2)==6 and all(abs(a["k"]-b["k"])<1e-15 for a,b in zip(rows1,rows2)))

    d1=[diagnostics(r) for r in rows1]
    d2=[diagnostics(r) for r in rows2]
    allrows=d1+d2

    eps_max=max(r["machine_epsilon_units"] for r in allrows)
    stiff_err=max(r["stiff_vs_trace_relative_error"] for r in allrows)
    full_err=max(r["full_Eprime_reconstruction_abs_or_rel_error"] for r in allrows)
    finite=bool(all(np.isfinite(v) for r in allrows for v in [
        r["machine_epsilon_units"],r["stiff_vs_trace_relative_error"],
        r["full_Eprime_reconstruction_abs_or_rel_error"],
        r["finite_gradient_over_stiff_abs_ratio"],
        r["Eprime_reconstructed"]
    ]))

    gates={
        "artifact_digest_exact":artifact_ok,
        "dense_trace_hashes_exact":hashes_ok,
        "all_six_modes_present":modes_ok,
        "cancellation_residual_machine_epsilon_units_le_8":bool(eps_max<=8.0),
        "stiff_term_reproduces_full_Eprime_relative_error_le_1e6":bool(stiff_err<=1e-6),
        "full_exact_Eprime_reconstruction_abs_or_rel_le_1e12":bool(full_err<=1e-12),
        "all_quantities_finite":finite,
    }
    passed=bool(all(gates.values()))

    result={
        "classification":(
            "GE14_CHI_CANCELLATION_STIFF_SEED_LOCALIZED"
            if passed else
            "GE14_CHI_CANCELLATION_STIFF_SEED_DIAGNOSTIC_FAIL"
        ),
        "predata_classification":"GE14_PREDATA_CHI_CANCELLATION_STIFF_SEED_AUDIT",
        "scope":"Frozen GE11 first-endpoint cancellation/stiff-source audit only; no CLASS execution.",
        "machine_epsilon":float(C_EPS),
        "R1":d1,
        "R2":d2,
        "summary":{
            "machine_epsilon_units_max":float(eps_max),
            "stiff_vs_trace_relative_error_max":float(stiff_err),
            "full_Eprime_reconstruction_abs_or_rel_error_max":float(full_err),
            "finite_gradient_over_stiff_abs_ratio_min":float(min(r["finite_gradient_over_stiff_abs_ratio"] for r in allrows)),
            "finite_gradient_over_stiff_abs_ratio_max":float(max(r["finite_gradient_over_stiff_abs_ratio"] for r in allrows)),
        },
        "cancellation_free_reparameterization":{
            "state":"s = a theta/k^2 + alpha = chi/Q",
            "alpha_reconstruction":"alpha = s - a theta/k^2",
            "chi":"chi=Q s",
            "s_prime":"s' = a[E + Pi/(1+w)] + 3 cad2 (aH) (a theta/k^2)",
            "E_prime":"E' = a/KB[KQ chi-(2-KB)(Q Pi/(1+w)+(H+Q)chi-3 cad2 H Q alpha)]-(aH)E",
            "background_identity_used":"Q'/Q=-3 cad2 (aH), following KQ=I0/a^3 and cad2=KQ/(Q KQQ)",
            "leading_IC":"s_i=0, E_i=0; finite-gradient source is generated directly by s' without subtracting alpha and a theta/k^2",
        },
        "gates":gates,
        "claim_boundary":"PASS localizes the initial numerical seed to cancellation plus the stiff KQ chi coupling. It does not relabel GE11 or by itself prove the entire late amplitude difference is numerical.",
    }

    Path(args.json_out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.json_out).write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps(result,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    main()
