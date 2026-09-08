#!/usr/bin/env python3
"""Execution-only perturbation-vector index mapping diagnostic for v0.62.

This patch does not alter equations, solver tolerances, approximation switches,
initial conditions, physical parameters, or acceptance gates.  When the
environment variable AEST_PT_INDEX_MAP_FILE is set, it logs the actual scalar
perturbation-vector layout created by perturbations_vector_init().
"""
from pathlib import Path
import argparse


def replace_once(path, old, new, label):
    p = Path(path)
    s = p.read_text()
    n = s.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected one anchor, found {n} in {p}")
    p.write_text(s.replace(old, new, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()
    root = Path(args.class_root).resolve()
    src = root / "source" / "perturbations.c"

    text = src.read_text()
    marker = "AEST v0.62 perturbation index map"
    if marker in text:
        print("perturbation index-map patch already present")
        return

    # stdio is already used by perturbations.c; stdlib/getenv is available
    # through CLASS headers on the pinned tree.  Add only the diagnostic block.
    old = """  ppv->pt_size = index_pt;\n\n  /** - allocate vectors for storing the values of all these\n"""
    new = r'''  ppv->pt_size = index_pt;

  /* AEST v0.62 perturbation index map: execution-only instrumentation. */
  {
    const char *aest_map_path = getenv("AEST_PT_INDEX_MAP_FILE");
    if ((aest_map_path != NULL) && (aest_map_path[0] != '\0') && _scalars_) {
      FILE *aest_map_fp = fopen(aest_map_path,"a");
      if (aest_map_fp != NULL) {
        int aest_i;
        fprintf(aest_map_fp,
                "BEGIN tau=%.17g k=%.17g pt_size=%d tca=%d rsa=%d ufa=%d ncdmfa=%d\n",
                tau,k,ppv->pt_size,
                ppw->approx[ppw->index_ap_tca],
                ppw->approx[ppw->index_ap_rsa],
                ppw->approx[ppw->index_ap_ufa],
                ppw->approx[ppw->index_ap_ncdmfa]);

        for (aest_i=0; aest_i<ppv->pt_size; ++aest_i) {
          const char *aest_name = NULL;
          int aest_l = -1;

          if ((ppw->approx[ppw->index_ap_rsa] == (int)rsa_off)) {
            if (aest_i == ppv->index_pt_delta_g) aest_name = "photon_delta_g_l0";
            else if (aest_i == ppv->index_pt_theta_g) aest_name = "photon_theta_g_l1";
            else if ((ppw->approx[ppw->index_ap_tca] == (int)tca_off) &&
                     (aest_i >= ppv->index_pt_shear_g) &&
                     (aest_i <= ppv->index_pt_delta_g + ppv->l_max_g)) {
              aest_l = aest_i - ppv->index_pt_delta_g;
              aest_name = "photon_temperature_multipole";
            }
            else if ((ppw->approx[ppw->index_ap_tca] == (int)tca_off) &&
                     (aest_i >= ppv->index_pt_pol0_g) &&
                     (aest_i <= ppv->index_pt_pol0_g + ppv->l_max_pol_g)) {
              aest_l = aest_i - ppv->index_pt_pol0_g;
              aest_name = "photon_polarization_multipole";
            }
          }

          if (aest_i == ppv->index_pt_delta_b) aest_name = "baryon_delta";
          else if (aest_i == ppv->index_pt_theta_b) aest_name = "baryon_theta";

          if (pba->has_cdm == _TRUE_) {
            if (aest_i == ppv->index_pt_delta_cdm) aest_name = "cdm_or_aest_delta";
            if ((ppt->gauge == newtonian) && (aest_i == ppv->index_pt_theta_cdm))
              aest_name = "cdm_or_aest_theta";
          }

          if (pba->aest_enabled == _TRUE_ && ppt->gauge == newtonian) {
            if (aest_i == ppv->index_pt_alpha_aest) aest_name = "aest_alpha";
            if (aest_i == ppv->index_pt_E_aest) aest_name = "aest_E";
          }

          if (pba->has_ur == _TRUE_ &&
              ppw->approx[ppw->index_ap_rsa] == (int)rsa_off) {
            if (aest_i == ppv->index_pt_delta_ur) aest_name = "ur_delta_l0";
            else if (aest_i == ppv->index_pt_theta_ur) aest_name = "ur_theta_l1";
            else if (aest_i == ppv->index_pt_shear_ur) aest_name = "ur_shear_l2";
            else if (ppw->approx[ppw->index_ap_ufa] == (int)ufa_off &&
                     aest_i >= ppv->index_pt_l3_ur &&
                     aest_i <= ppv->index_pt_delta_ur + ppv->l_max_ur) {
              aest_l = aest_i - ppv->index_pt_delta_ur;
              aest_name = "ur_multipole";
            }
          }

          if (ppt->gauge == newtonian && aest_i == ppv->index_pt_phi)
            aest_name = "metric_phi";

          if (aest_name != NULL) {
            if (aest_l >= 0)
              fprintf(aest_map_fp,"idx=%d name=%s l=%d\n",aest_i,aest_name,aest_l);
            else
              fprintf(aest_map_fp,"idx=%d name=%s\n",aest_i,aest_name);
          }
        }
        fprintf(aest_map_fp,"END\n");
        fclose(aest_map_fp);
      }
    }
  }

  /** - allocate vectors for storing the values of all these
'''
    replace_once(src, old, new, "perturbation vector pt_size anchor")

    print(f"patched {src}")
    print("Set AEST_PT_INDEX_MAP_FILE=/path/to/map.log to enable mapping.")
    print("Scientific settings changed: false")


if __name__ == "__main__":
    main()
