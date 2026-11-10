#!/usr/bin/env python3
"""GE19 LW23: action / implemented-source eta-branch audit, NO CLASS run.

A source-locked, exact-symbolic audit of the *implemented* E_A tangent
source and its offline Drude representation. It does NOT certify the
complete 3+1 action-to-CLASS or survey forward operator.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / "ge19/lw23_implemented_eta_source_vs_action_branch_predata_20261110.json"
PRE_BLOB = "3dbeba3ea52776d9cda6e85b5dcabda937659a81"
ANCHORS = {
    "v019/apply_patch_v019.py": [
        "Pi_aest = cad2_aest*y[ppw",
        "ppw->delta_p += rho_dark*Pi_aest;",
    ],
    "v019j/apply_memory_patch.py": [
        "Bchi_aest *= pba->aest_eta;",
        "E_rhs_aest -= 0.5*Q_aest*Bchi_aest;",
        "dy[pv->index_pt_mem_p_aest+jm] =",
    ],
    "v019w/apply_variational_forcing_patch.py": [
        "aest_tangent_trace_force(k,tau,-0.5*a*Q_aest*Braw_aest/pba->aest_KB);",
        "dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);",
    ],
    "v022/build_offline_forcing.py": [
        "out[i+1] = x[i+1]-float(np.dot(weights,q))",
        "0.5*w",
        "z_j=(omega_j/k)u_j",
    ],
    "v039/build_tau_forcing.py": [
        "fc=-0.5*aa*aa*Q*yc/a.KB",
        "fp=-0.5*aa*aa*Q*yp/a.KB",
    ],
    "v063/theory_response_map.py": [
        "'aest_memory_enabled': 'no'",
        "'aest_eta': 0.0",
        "'gauge': 'newtonian'",
    ],
    "ge19/linear_weyl_native_tangent_20261109.py": [
        "AEST_TANGENT_FORCE_FILE", "AEST_TANGENT_LAMBDA",
    ],
    "ge19/lw16_scalar_to_velocity_bath_euler_projection_20261110.py": [
        "projected_aether_source_matches_frozen_CLASS",
        "negative_control_scalar_partner_missing",
    ],
    "ge19/lw18_reduced_time_diffeo_noether_20261110.py": [
        "Ephi_fourier=-eta*a*k**2*Bchi/2",
        "Eu_fourier=-s.I*eta*a**2*k*Q*Bchi/2",
    ],
    "ge19/lw19_reduced_full_action_temporal_invariance_20261110.py": [
        "full_reduced_action_exact_boundary",
        "negative_omit_rapidity_boost_detected",
    ],
}


def require(condition, label):
    if not bool(condition):
        raise RuntimeError("GE19_LW23_" + label)


def blob(path):
    return subprocess.check_output(
        ["git", "hash-object", str(path)], cwd=ROOT, text=True
    ).strip()


def sha256(path):
    d = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            d.update(chunk)
    return d.hexdigest()


def exact_symbolics():
    import sympy as s

    a, Q, KB, y, chi, z1, z2, w1 = s.symbols(
        "a Q K_B y chi z_1 z_2 w_1", nonzero=True, real=True
    )
    eta, om, q, w, X, k = s.symbols(
        "eta omega q w X k", positive=True, real=True
    )
    u0, u1, q0, q1, c = s.symbols("u0 u1 q0 q1 c", real=True)
    D, W, De, We, PR = s.symbols("D W D_eta W_eta PR", real=True)

    Braw = w1 * (chi - a*z1) + (1-w1) * (chi-a*z2)
    offline = a * (chi/a - w1*z1 - (1-w1)*z2)
    Fclass = -a*Q*Braw/(2*KB)
    Foffline = -a*a*Q*(Braw/a)/(2*KB)

    # The *entire* normalized auxiliary action carries eta:
    # at exactly eta=0 its Euler equation is 0=0; a retarded
    # branch q0 must be selected from eta>0 before differentiating.
    Lpotential = -eta*s.Rational(1, 4)*(om*q - s.sqrt(w)*X)**2
    Eq = s.diff(Lpotential, q)

    # Triangular variational source lemma for the IMPLEMENTED equations,
    # with q0 fixed by a selected causal eta>0 auxiliary branch.
    u = u0 + eta*u1
    qb = q0 + eta*q1
    F0 = u*u + c*u
    S = -a*Q*(u-qb)/(2*KB)
    tangent = s.diff(F0+eta*S, eta).subs(eta, 0)
    intended = (2*u0+c)*u1-a*Q*(u0-q0)/(2*KB)

    # Exact reduced time-Ward identity of the physical bath source pair.
    B = s.symbols("B", real=True)
    Ephi = -eta*a*k*k*B/2
    Eu = -s.I*eta*a*a*k*Q*B/2

    Pc = PR*(D+eta*De)*(W+eta*We)
    checks = {
        "offline_continuum_Braw_equals_a_times_y_for_unit_weights":
            s.simplify(Braw-offline) == 0,
        "original_Eprime_matches_offline_a_squared_Q_over_2KB":
            s.simplify(Fclass-Foffline) == 0,
        "negative_wrong_a_factor_detected":
            s.simplify(Fclass+Q*Braw/(2*KB)) != 0,
        "negative_wrong_half_factor_detected":
            s.simplify(Fclass+a*Q*Braw/KB) != 0,
        "eta_zero_auxiliary_Euler_is_degenerate":
            s.simplify(Eq.subs(eta, 0)) == 0 and
            s.simplify(s.diff(Eq, eta)) != 0,
        "triangular_implemented_eta_tangent":
            s.simplify(tangent-intended) == 0,
        "auxiliary_q1_not_direct_source_at_eta_zero":
            s.simplify(s.diff(tangent, q1)) == 0,
        "reduced_physical_bath_scalar_aether_time_Ward":
            s.simplify(Q*Ephi+s.I*k*Eu/a) == 0,
        "negative_missing_scalar_companion_detected":
            s.simplify(s.I*k*Eu/a) != 0,
        "signed_cross_product_derivative":
            s.simplify(s.diff(Pc, eta).subs(eta, 0)-PR*(De*W+D*We)) == 0,
    }
    failed = [name for name, ok in checks.items() if not bool(ok)]
    require(not failed, "SYMBOLIC_FAIL_" + "_".join(failed))
    return {name: bool(ok) for name, ok in checks.items()}


def source_audit():
    require(PRE.is_file() and blob(PRE) == PRE_BLOB, "PRELOCK_CHANGED")
    frozen = json.loads(PRE.read_text(encoding="utf-8"))
    require(
        frozen["classification"] ==
        "GE19_LW23_IMPLEMENTED_SOURCE_FACTOR_AND_ETA_BRANCH_PRELOCK",
        "PRECLASS_CHANGED"
    )
    require(set(frozen["source_blobs"]) == set(ANCHORS), "PRE_SOURCE_SET_CHANGED")
    actual = {}
    for path, sha in sorted(frozen["source_blobs"].items()):
        p = ROOT / path
        require(p.is_file(), "MISSING_SOURCE_" + p.name)
        digest = blob(p)
        require(digest == sha, "SOURCE_BLOB_CHANGED_" + p.name)
        data = p.read_text(encoding="utf-8")
        for i, anchor in enumerate(ANCHORS[path], start=1):
            require(anchor in data, "SOURCE_ANCHOR_" + p.name + "_" + str(i))
        actual[path] = digest
    return actual, frozen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--out", type=Path, default=ROOT /
        "results/ge19_lw23_implemented_eta_source_action_branch_20261110_r1.json")
    a = ap.parse_args()
    gates = exact_symbolics()
    print("GE19_LW23_SYMBOLIC_SELFTEST_PASS", len(gates), flush=True)
    if a.self_test:
        return

    parents, frozen = source_audit()
    print("GE19_LW23_SOURCE_ANCHORS_PASS", len(parents), flush=True)
    output = a.out.resolve()
    require(output.parent.is_dir() and not output.exists(),
            "OUTPUT_EXISTS_OR_PARENT_MISSING")
    report = {
        "classification":
            "GE19_LW23_IMPLEMENTED_ETA_SOURCE_FACTOR_PASS_PHYSICAL_ACTION_TO_CLASS_BRIDGE_OPEN",
        "predata_blob": PRE_BLOB,
        "original_source_blobs": parents,
        "symbolic_gates": gates,
        "physical_source_evaluation": {
            "eta_zero_baseline": "aest_memory_enabled=no, aest_eta=0",
            "continuum_retarded_branch": "offline Drude history reconstructed from frozen eta0 chi/a; q0 branch must be specified as eta approaches zero from positive eta",
            "normalized_Braw": "a*(chi/a - sum_j w_j z_j) for normalized positive quadrature",
            "Eprime_eta_inhomogeneity":
                "-a*Q*Braw/(2*K_B)=-a^2*Q*y/(2*K_B)",
            "numeric_lambda":
                "amplification of prescribed external force; not physical finite eta",
            "conditional_variational_statement":
                "If q0 is the retarded normalized auxiliary solution and frozen patched E-row plus coupled constraints is the correct reduced physical Euler map, the implemented external forcing gives the u_eta inhomogeneity at eta=0. This is NOT a proof of that full physical map.",
        },
        "source_level_signed_cross_derivative":
            "P_R*(D_eta*W+D*W_eta); independently audited product rule, not observed gamma_t",
        "resolved": {
            "source_coefficient_sign_a_KB": True,
            "offline_vs_native_Braw_normalization_algebra": True,
            "auxiliary_eta_zero_degeneracy_identified": True,
            "physical_reduced_bath_Ward_partner": True,
        },
        "unresolved": {
            "full_3plus1_action_to_CLASS_E_theta_density_momentum_map": True,
            "complete_Einstein_metric_constraint_and_other_species_tangent": True,
            "continuum_vs_finite_bath_retarded_branch_error_bound": True,
            "physical_history_pair_Weyl_observer": True,
            "real_DES_gamma_t_forward_and_covariance": True,
            "nuisance_marginal_memory_identifiability": True,
        },
        "physical_eta_cross_response_certified": False,
        "full_GGL_physical_forward_ready": False,
        "observational_memory_detection": False,
        "LW22_geometry_pass_preserved": True,
        "LW08_antisymmetric_response_unresolved_preserved": True,
        "H4_Z21_uncertified_preserved": True,
    }
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")
    print("GE19_LW23_CLASSIFICATION", report["classification"], flush=True)
    print("GE19_LW23_PHYSICAL_FORWARD_READY", False, flush=True)
    print("GE19_LW23_OUTPUT", str(output), flush=True)


if __name__ == "__main__":
    main()
