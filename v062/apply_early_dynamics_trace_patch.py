#!/usr/bin/env python3
"""Execution-only early-time perturbation dynamics trace for v0.62.

This patch instruments perturbations_derivs() without changing equations,
initial conditions, tolerances, approximation switches, physical parameters,
or scientific gates.  When AEST_EARLY_DYNAMICS_TRACE_FILE is set, it writes a
throttled early-time trace of the UR sector, metric potentials, and AeST state.

The trace is diagnostic only and MUST NOT be used for the preregistered v0.62
classification.
"""
from pathlib import Path
import argparse

MARKER = "AEST v0.62 early dynamics trace"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()

    root = Path(args.class_root).resolve()
    src = root / "source" / "perturbations.c"
    if not src.exists():
        raise SystemExit(f"missing {src}")

    text = src.read_text()
    if MARKER in text:
        print("early dynamics trace patch already present")
        return

    fn = text.find("int perturbations_derivs(double tau,")
    if fn < 0:
        raise RuntimeError("perturbations_derivs() anchor not found")

    # Restrict the insertion search to perturbations_derivs().  The pinned CLASS
    # implementation has a single final return _SUCCESS_; in this function.
    next_doc = text.find("\n/**", fn + 1)
    if next_doc < 0:
        next_doc = len(text)
    ret = text.rfind("  return _SUCCESS_;", fn, next_doc)
    if ret < 0:
        raise RuntimeError("final perturbations_derivs() return anchor not found")

    block = r'''  /* AEST v0.62 early dynamics trace: execution-only instrumentation. */
  {
    const char *tr_path = getenv("AEST_EARLY_DYNAMICS_TRACE_FILE");
    if ((tr_path != NULL) && (tr_path[0] != '\0')) {
      struct perturbations_parameters_and_workspace *tr_pppaw =
        (struct perturbations_parameters_and_workspace *)parameters_and_workspace;
      struct background *tr_pba = tr_pppaw->pba;
      struct perturbations *tr_ppt = tr_pppaw->ppt;
      struct perturbations_workspace *tr_ppw = tr_pppaw->ppw;
      struct perturbations_vector *tr_pv = tr_ppw->pv;
      double tr_k = tr_pppaw->k;
      double tr_tau_min = 0.03;
      double tr_tau_max = 7.0;
      double tr_growth = 1.03;
      const char *tr_env;
      static double tr_last_k = -1.;
      static double tr_last_tau = -1.;
      static long long tr_eval_total = 0;
      static long long tr_eval_mode = 0;
      static int tr_header_written = 0;

      tr_eval_total++;
      tr_env = getenv("AEST_EARLY_DYNAMICS_TAU_MIN");
      if ((tr_env != NULL) && (tr_env[0] != '\0')) tr_tau_min = atof(tr_env);
      tr_env = getenv("AEST_EARLY_DYNAMICS_TAU_MAX");
      if ((tr_env != NULL) && (tr_env[0] != '\0')) tr_tau_max = atof(tr_env);
      tr_env = getenv("AEST_EARLY_DYNAMICS_GROWTH");
      if ((tr_env != NULL) && (tr_env[0] != '\0')) tr_growth = atof(tr_env);
      if (tr_growth <= 1.) tr_growth = 1.03;

      if ((tr_last_k < 0.) ||
          (fabs(tr_k-tr_last_k) > 1.e-12*MAX(1.,fabs(tr_k)))) {
        tr_last_k = tr_k;
        tr_last_tau = -1.;
        tr_eval_mode = 0;
      }
      tr_eval_mode++;

      if ((tau >= tr_tau_min) && (tau <= tr_tau_max) &&
          ((tr_last_tau < 0.) ||
           (tau >= tr_last_tau*tr_growth) ||
           (tau-tr_last_tau >= 1.e-3))) {
        FILE *tr_fp = fopen(tr_path,"a");
        if (tr_fp != NULL) {
          int tr_rsa = tr_ppw->approx[tr_ppw->index_ap_rsa];
          int tr_ufa = (tr_pba->has_ur == _TRUE_) ?
            tr_ppw->approx[tr_ppw->index_ap_ufa] : -1;
          int tr_have_ur =
            (tr_pba->has_ur == _TRUE_) && (tr_rsa == (int)rsa_off);
          int tr_have_aest =
            (tr_pba->aest_enabled == _TRUE_) && (tr_ppt->gauge == newtonian);
          double tr_nan = NAN;
          double tr_phi = tr_nan;
          double tr_psi = tr_nan;
          double tr_phi_prime = tr_nan;
          double tr_du = tr_nan, tr_tu = tr_nan, tr_su = tr_nan;
          double tr_du_rhs = tr_nan, tr_tu_rhs = tr_nan, tr_su_rhs = tr_nan;
          double tr_alpha = tr_nan, tr_E = tr_nan;
          double tr_alpha_rhs = tr_nan, tr_E_rhs = tr_nan;
          double tr_cont_theta = tr_nan, tr_cont_metric = tr_nan, tr_cont_other = tr_nan;

          if (tr_ppt->gauge == newtonian) {
            tr_phi = y[tr_pv->index_pt_phi];
            tr_psi = tr_ppw->pvecmetric[tr_ppw->index_mt_psi];
            tr_phi_prime = tr_ppw->pvecmetric[tr_ppw->index_mt_phi_prime];
          }

          if (tr_have_ur) {
            tr_du = y[tr_pv->index_pt_delta_ur];
            tr_tu = y[tr_pv->index_pt_theta_ur];
            tr_su = y[tr_pv->index_pt_shear_ur];
            tr_du_rhs = dy[tr_pv->index_pt_delta_ur];
            tr_tu_rhs = dy[tr_pv->index_pt_theta_ur];
            tr_su_rhs = dy[tr_pv->index_pt_shear_ur];
            if (tr_ppt->gauge == newtonian) {
              /* For standard ceff2_ur=1/3, these are the two continuity
                 contributions and the residual is zero up to roundoff. */
              tr_cont_theta = -4./3.*tr_tu;
              tr_cont_metric = 4.*tr_phi_prime;
              tr_cont_other = tr_du_rhs-tr_cont_theta-tr_cont_metric;
            }
          }

          if (tr_have_aest) {
            tr_alpha = y[tr_pv->index_pt_alpha_aest];
            tr_E = y[tr_pv->index_pt_E_aest];
            tr_alpha_rhs = dy[tr_pv->index_pt_alpha_aest];
            tr_E_rhs = dy[tr_pv->index_pt_E_aest];
          }

          if (tr_header_written == 0) {
            fprintf(tr_fp,
                    "# classification_use=NONE_NON_SCIENTIFIC_EARLY_DYNAMICS_TRACE\n"
                    "# columns: eval_total eval_mode k tau pt_size rsa ufa "
                    "ur_delta ur_theta ur_shear dur dtheta_ur dshear_ur "
                    "phi psi phi_prime ur_cont_theta ur_cont_metric ur_cont_other "
                    "aest_alpha aest_E daest_alpha daest_E\n");
            tr_header_written = 1;
          }

          fprintf(tr_fp,
                  "%lld %lld %.17g %.17g %d %d %d "
                  "%.17g %.17g %.17g %.17g %.17g %.17g "
                  "%.17g %.17g %.17g %.17g %.17g %.17g "
                  "%.17g %.17g %.17g %.17g\n",
                  tr_eval_total,tr_eval_mode,tr_k,tau,tr_pv->pt_size,tr_rsa,tr_ufa,
                  tr_du,tr_tu,tr_su,tr_du_rhs,tr_tu_rhs,tr_su_rhs,
                  tr_phi,tr_psi,tr_phi_prime,
                  tr_cont_theta,tr_cont_metric,tr_cont_other,
                  tr_alpha,tr_E,tr_alpha_rhs,tr_E_rhs);
          fclose(tr_fp);
          tr_last_tau = tau;
        }
      }
    }
  }

'''

    text = text[:ret] + block + text[ret:]
    src.write_text(text)

    print(f"patched {src}")
    print("Enable with AEST_EARLY_DYNAMICS_TRACE_FILE=/path/to/trace.dat")
    print("Scientific settings changed: false")


if __name__ == "__main__":
    main()
