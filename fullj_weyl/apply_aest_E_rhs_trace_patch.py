#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

MARKER = "FULLJ_AEST_ERHS_TRACE_V2"

ANCHOR = '''        dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;\n        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'''

INJECT = r'''        /* FULLJ_AEST_ERHS_TRACE_V2: read-only source diagnostic. */
        {
          static FILE *aest_erhs_trace_fp = NULL;
          static char aest_erhs_trace_path[4096] = "";
          const char *trace_path = getenv("AEST_ERHS_TRACE_FILE");
          const char *trace_k_text = getenv("AEST_ERHS_TRACE_K");
          if ((trace_path != NULL) && (trace_path[0] != '\0') &&
              (trace_k_text != NULL) && (trace_k_text[0] != '\0')) {
            double trace_k = strtod(trace_k_text,NULL);
            if ((k == trace_k) && (a <= 3.e-4)) {
              if (strcmp(aest_erhs_trace_path,trace_path) != 0) {
                if (aest_erhs_trace_fp != NULL) fclose(aest_erhs_trace_fp);
                strncpy(aest_erhs_trace_path,trace_path,sizeof(aest_erhs_trace_path)-1);
                aest_erhs_trace_path[sizeof(aest_erhs_trace_path)-1] = '\0';
                aest_erhs_trace_fp = fopen(trace_path,"w");
                if (aest_erhs_trace_fp != NULL) {
                  fprintf(aest_erhs_trace_fp,
                    "# k tau a alpha E delta theta Q KQ H cad2 w rho chi Pi pi_delta pi_E pi_chi T1 T2 T3 T4 E_rhs D1 D2 dyE\n");
                }
              }
              if (aest_erhs_trace_fp != NULL) {
                double pi_delta = cad2_aest*y[pv->index_pt_delta_cdm];
                double pi_E = cad2_aest*k2/(3.*a*a*rho_aest)*pba->aest_KB*E_aest;
                double pi_chi = cad2_aest*k2/(3.*a*a*rho_aest)*(2.-pba->aest_KB)*chi_aest;
                double T1 = KQ_aest*chi_aest;
                double T2 = -(2.-pba->aest_KB)*Q_aest*Pi_aest/(1.+w_aest);
                double T3 = -(2.-pba->aest_KB)*(H_aest+Q_aest)*chi_aest;
                double T4 = +(2.-pba->aest_KB)*3.*cad2_aest*H_aest*Q_aest*alpha_aest;
                double D1 = a*E_rhs_aest/pba->aest_KB;
                double D2 = -a_prime_over_a*E_aest;
                double dyE = D1+D2;
                fprintf(aest_erhs_trace_fp,
                  "%.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g\n",
                  k,tau,a,alpha_aest,E_aest,y[pv->index_pt_delta_cdm],theta_div_aest,
                  Q_aest,KQ_aest,H_aest,cad2_aest,w_aest,rho_aest,chi_aest,Pi_aest,
                  pi_delta,pi_E,pi_chi,T1,T2,T3,T4,E_rhs_aest,D1,D2,dyE);
                fflush(aest_erhs_trace_fp);
              }
            }
          }
        }

        dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;
        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'''


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()
    p = Path(args.class_root).resolve() / "source" / "perturbations.c"
    if not p.is_file():
        raise SystemExit(f"missing perturbations.c: {p}")
    text = p.read_text()
    if MARKER in text:
        print("FULLJ_AEST_ERHS_TRACE_PATCH already=2")
        return 0
    if text.count(ANCHOR) != 1:
        raise SystemExit(f"expected one E-RHS assignment anchor, found {text.count(ANCHOR)}")
    text = text.replace(ANCHOR, INJECT, 1)
    p.write_text(text)
    final = p.read_text()
    required = [MARKER, 'AEST_ERHS_TRACE_FILE', 'AEST_ERHS_TRACE_K', 'double T1 = KQ_aest*chi_aest;', 'double dyE = D1+D2;']
    if not all(x in final for x in required):
        raise SystemExit("E-RHS trace patch verification failed")
    if '\\\\n' in final[final.index(MARKER):final.index(MARKER)+5000]:
        raise SystemExit("E-RHS trace patch still contains literal-backslash newline formatting")
    print("FULLJ_AEST_ERHS_TRACE_PATCH_PASS version=2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
