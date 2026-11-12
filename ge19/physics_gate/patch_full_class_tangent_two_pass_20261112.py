#!/usr/bin/env python3
"""GE19 experimental full-CLASS two-pass direct eta tangent (single k, adiabatic IC).
Applies ONLY to a pristine v019j or isolated-quarter AeST CLASS perturbations.c.
Fail-closed: exact source SHA, exact insertion anchors, backup+manifest; no git action.
Not a certified physical Einstein–AeST–NL0B equivalence or DES detection.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path

PRISTINE_SHA256 = {
    "276646d913348824bddf9e24138e4213ecc3fb8b605d21525bf9280474dbca80": "v019j_historical_half",
    "75bf9fe85f2aae85031edc109e131c6b5d1745dca8497300237e16e57c99f883": "isolated_quarter_candidate",
}
SOURCE_MARKER = "/* GE19 FULL CLASS DIRECT TANGENT EXPERIMENT v1 */"

HELPER = r"""
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
/* GE19 FULL CLASS DIRECT TANGENT EXPERIMENT v1 */
/* FAIL CLOSED: ONLY ONE ADIABATIC K, OMP_NUM_THREADS=1, independent CLASS runs.
   record: dense accepted solution samples at output callback, true primordial bath.
   force: zero initial state, full native homogeneous CLASS operator + E-source.
   This feature is experimental, not certified cosmological detection. */
static int ge19_mode(void) {
  const char *m=getenv("GE19_TANGENT_MODE");
  if (!m || !m[0]) return 0;
  if (strcmp(getenv("OMP_NUM_THREADS") ? getenv("OMP_NUM_THREADS") : "", "1") != 0) {
    fprintf(stderr,"GE19_TANGENT_REFUSE_THREADS: set OMP_NUM_THREADS=1\n");
    exit(81);
  }
  if (strcmp(m,"record")==0) return 1;
  if (strcmp(m,"force")==0) return 2;
  fprintf(stderr,"GE19_TANGENT_UNKNOWN_MODE\n"); exit(81);
}
static double ge19_target_k(void) {
  const char *s=getenv("GE19_TANGENT_K_MPC");
  char *end=NULL;
  double k;
  if (!s || !s[0]) {fprintf(stderr,"GE19_TANGENT_K_REQUIRED\n");exit(81);}
  k=strtod(s,&end);
  if (!end || *end || !isfinite(k) || k<=0.) {
    fprintf(stderr,"GE19_TANGENT_INVALID_K\n");exit(81);
  }
  return k;
}
static int ge19_selected(double k) {
  double target;
  if (!ge19_mode()) return 0;
  target=ge19_target_k();
  return fabs(k-target)<=1.e-11*target;
}
static FILE *ge19_writer(const char *var) {
  static FILE *rec=NULL,*out=NULL;
  FILE **f=(strcmp(var,"GE19_TANGENT_TRACE")==0)?&rec:&out;
  const char *name;
  if (*f) return *f;
  name=getenv(var);
  if (!name || !name[0]) {fprintf(stderr,"GE19_TANGENT_OUTPUT_MISSING %s\n",var);exit(82);}
  *f=fopen(name,"w");
  if (!*f) {perror(name);exit(82);}
  fprintf(*f,"tau,a,k_mpc,W,Bchi\n");
  fflush(*f);
  return *f;
}
static double *ge19_times=NULL, *ge19_B=NULL;
static size_t ge19_count=0;
static void ge19_load_trace(void) {
  FILE *f;
  char line[1024];
  const char *path=getenv("GE19_TANGENT_TRACE");
  double t,a,k,W,B;
  size_t cap=0;
  if (ge19_times) return;
  if (!path || !path[0] || !(f=fopen(path,"r"))) {
    fprintf(stderr,"GE19_TANGENT_TRACE_NOT_FOUND\n");exit(82);
  }
  while (fgets(line,sizeof(line),f)) {
    if (line[0]=='t') continue;
    if (sscanf(line,"%lf,%lf,%lf,%lf,%lf",&t,&a,&k,&W,&B)!=5 ||
        !isfinite(t) || !isfinite(a) || !isfinite(k) ||
        !isfinite(W) || !isfinite(B) || a<=0. ||
        fabs(k-ge19_target_k())>1.e-11*ge19_target_k() ||
        (ge19_count && t<=ge19_times[ge19_count-1])) {
      fprintf(stderr,"GE19_TANGENT_INVALID_SOURCE_TRACE line=%zu\n",ge19_count+1);
      exit(82);
    }
    if (ge19_count==cap) {
      double *tt,*bb;
      cap=cap ? 2*cap : 4096;
      tt=(double*)realloc(ge19_times,cap*sizeof(double));
      if (!tt) {fprintf(stderr,"GE19_TANGENT_OOM\n");exit(82);}
      ge19_times=tt;
      bb=(double*)realloc(ge19_B,cap*sizeof(double));
      if (!bb) {fprintf(stderr,"GE19_TANGENT_OOM\n");exit(82);}
      ge19_B=bb;
    }
    ge19_times[ge19_count]=t;
    ge19_B[ge19_count]=B;
    ge19_count++;
  }
  fclose(f);
  if (ge19_count<3) {fprintf(stderr,"GE19_TANGENT_TRACE_TOO_SHORT\n");exit(82);}
  fprintf(stderr,"GE19_TANGENT_TRACE_LOADED %zu\n",ge19_count);
}
static double ge19_force_at(double tau, double k) {
  size_t lo,hi,mid;
  if (ge19_mode()!=2 || !ge19_selected(k)) return 0.;
  ge19_load_trace();
  if (tau<ge19_times[0]-1.e-7 || tau>ge19_times[ge19_count-1]+1.e-7) {
    fprintf(stderr,"GE19_TANGENT_SOURCE_OUTSIDE_TRACE tau=%.17g range=[%.17g,%.17g]\n",
            tau,ge19_times[0],ge19_times[ge19_count-1]);
    exit(83);
  }
  if (tau<=ge19_times[0]) return ge19_B[0];
  if (tau>=ge19_times[ge19_count-1]) return ge19_B[ge19_count-1];
  lo=0; hi=ge19_count-1;
  while (hi-lo>1) {
    mid=(lo+hi)/2;
    if (ge19_times[mid]<=tau) lo=mid;
    else hi=mid;
  }
  return ge19_B[lo]+(ge19_B[hi]-ge19_B[lo])*
         (tau-ge19_times[lo])/(ge19_times[hi]-ge19_times[lo]);
}
static double *ge19_dense_sampling(double begin,double end,int *n) {
  double dt,span;
  const char *dts=getenv("GE19_TANGENT_DT_MPC");
  double *arr;
  int i;
  if (!dts || !dts[0]) dt=0.1;
  else dt=atof(dts);
  /* Strict source-sampling ceiling: max 0.1 Mpc on original order-16 bath.
     Further halve this value for independent interpolation convergence. */
  if (dt<=0. || dt>0.1 || !isfinite(dt) || !(end>begin)) {
    fprintf(stderr,"GE19_TANGENT_INVALID_DENSE_STEP\n");exit(84);
  }
  span=end-begin;
  *n=(int)ceil(span/dt)+1;
  if (*n>400000 || *n<3) {
    fprintf(stderr,"GE19_TANGENT_SAMPLE_CAP %d\n",*n);exit(84);
  }
  arr=(double*)malloc((size_t)(*n)*sizeof(double));
  if (!arr) {fprintf(stderr,"GE19_TANGENT_SAMPLE_OOM\n");exit(84);}
  for (i=0;i<*n;i++) arr[i]=begin+span*i/(*n-1);
  arr[0]=begin;arr[*n-1]=end;
  fprintf(stderr,"GE19_TANGENT_DENSE_TIMES %d step_max=%.8g\n",*n,span/(*n-1));
  return arr;
}
/* Source callback is invoked by native CLASS evolver at interpolated accepted
   trajectory samples, NEVER at speculative stiff integrator RHS probes. */
static int ge19_record_callback(double tau,double *y,double *dy,int index_tau,
                                void *parameters_and_workspace,
                                ErrorMsg error_message) {
  struct perturbations_parameters_and_workspace *pppaw=
    (struct perturbations_parameters_and_workspace *)parameters_and_workspace;
  struct perturbations_workspace *ppw=pppaw->ppw;
  struct background *pba=pppaw->pba;
  struct thermodynamics *pth=pppaw->pth;
  struct perturbations *ppt=pppaw->ppt;
  struct perturbations_vector *pv=ppw->pv;
  double a,Q,chi,B=0.,Weyl,k=pppaw->k,z;
  int j,n;
  (void)dy;(void)index_tau;
  if (!ge19_selected(k) || ge19_mode()!=1) {
    fprintf(stderr,"GE19_TANGENT_INVALID_CALLBACK\n");exit(85);
  }
  if (!pba->aest_enabled || !pba->aest_memory_enabled ||
      ppt->gauge != newtonian || pppaw->index_md!=ppt->index_md_scalars) {
    fprintf(stderr,"GE19_TANGENT_REQUIRES_AEST_NEWTONIAN_SCALARS\n");exit(85);
  }
  class_call(background_at_tau(pba,tau,normal_info,inter_closeby,
                &(ppw->last_index_back),ppw->pvecback),
             pba->error_message,error_message);
  a=ppw->pvecback[pba->index_bg_a];z=1./a-1.;
  class_call(thermodynamics_at_z(pba,pth,z,inter_closeby,
              &(ppw->last_index_thermo),ppw->pvecback,ppw->pvecthermo),
             pth->error_message,error_message);
  class_call(perturbations_einstein(pppaw->ppr,pba,pth,ppt,
                         pppaw->index_md,k,tau,y,ppw),
             ppt->error_message,error_message);
  Q=ppw->pvecback[pba->index_bg_Q_aest];
  chi=Q*(a*y[pv->index_pt_theta_cdm]/(k*k)+y[pv->index_pt_alpha_aest]);
  n=aest_memory_active_count(pba->aest_memory_order);
  for(j=0;j<n;j++) {
    double omega=aest_memory_node_order(pba->aest_memory_order,j)*
                 pba->H0/pba->aest_tau_H0;
    double w=aest_memory_weight_order(pba->aest_memory_order,j);
    B+=w*chi-sqrt(w)*(a*omega/k)*y[pv->index_pt_mem_q_aest+j];
  }
  Weyl=(y[pv->index_pt_phi]+ppw->pvecmetric[ppw->index_mt_psi])/2.;
  fprintf(ge19_writer("GE19_TANGENT_TRACE"),"%.17g,%.17g,%.17g,%.17g,%.17g\n",
          tau,a,k,Weyl,B);
  return _SUCCESS_;
}
static void ge19_write_tangent_readout(double tau,double a,double k,double Weyl) {
  if (ge19_mode()==2 && ge19_selected(k)) {
    fprintf(ge19_writer("GE19_TANGENT_OUT"),"%.17g,%.17g,%.17g,%.17g,0\n",
            tau,a,k,Weyl);
  }
}
"""

def one(s: str, old: str, new: str, label: str) -> str:
    n=s.count(old)
    if n!=1:
        raise RuntimeError(f"GE19_PATCH_ANCHOR_{label}_COUNT_{n}")
    return s.replace(old,new)

def modify(original: str) -> str:
    s=original
    s=one(s,'#include "parallel.h"\n',
          '#include "parallel.h"\n'+HELPER+'\n',"HEADER")
    # In the target branch only one AeST memory E term is present.
    if 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' in s:
        s=one(s,'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;',
              'E_rhs_aest -= 0.25*Q_aest*Bchi_aest;',"QUARTER")
    elif s.count('E_rhs_aest -= 0.25*Q_aest*Bchi_aest;') != 1:
        raise RuntimeError("GE19_SOURCE_NOT_QUARTER_OR_HISTORICAL")
    s=one(s,
      'dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;',
      '/* GE19 forced exact eta tangent: only the direct E source at eta0. */\n'
      '        if (ge19_mode()==2 && ge19_selected(k)) {\n'
      '          E_rhs_aest -= 0.25*Q_aest*ge19_force_at(tau,k);\n'
      '        }\n'
      '        dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;',
      "TANGENT_E")
    s=one(s,
       '               ppt->error_message,\n'
       '               ppt->error_message);\n\n'
       '    /** - --> compute quantities depending on approximation schemes */',
       '               ppt->error_message,\n'
       '               ppt->error_message);\n'
       '    /* GE19 direct W1 from full CLASS Einstein shear at source times. */\n'
       '    ge19_write_tangent_readout(tau,a,k,\n'
       '      (y[ppw->pv->index_pt_phi]+pvecmetric[ppw->index_mt_psi])/2.);\n\n'
       '    /** - --> compute quantities depending on approximation schemes */',
       "READOUT")
    s=one(s,
       '               ppt->error_message,\n'
       '               ppt->error_message);\n\n'
       '  }\n\n'
       '  /** - case of switching approximation while a wavenumber is being integrated */',
       '               ppt->error_message,\n'
       '               ppt->error_message);\n'
       '    /* GE19: the derivative of eta-independent initial data is zero. */\n'
       '    if (ge19_mode()==2 && ge19_selected(k)) {\n'
       '      int i;\n'
       '      for(i=0;i<ppw->pv->pt_size;i++) ppw->pv->y[i]=0.;\n'
       '    }\n\n'
       '  }\n\n'
       '  /** - case of switching approximation while a wavenumber is being integrated */',
       "INITIAL_TANGENT")
    s=one(s,
       '  int tau_actual_size;\n',
       '  int tau_actual_size;\n'
       '  int ge19_record_selected=0;\n'
       '  int ge19_n=0;\n'
       '  double *ge19_tau=NULL;\n',
       "SOLVE_LOCALS")
    s=one(s,
       '  /** - loop over intervals over which approximation scheme is uniform. For each interval: */',
       '  /* GE19: the recorder samples from true primordial tau_ini, not only\n'
       '     native tau_sampling[0] (which can start too late for memory). */\n'
       '  ge19_record_selected=(ge19_mode()==1 && ge19_selected(k));\n'
       '  if (ge19_record_selected) {\n'
       '    ge19_tau=ge19_dense_sampling(interval_limit[0],\n'
       '                  interval_limit[interval_number],&ge19_n);\n'
       '  }\n'
       '  /** - loop over intervals over which approximation scheme is uniform. For each interval: */',
       "RECORD_TIMES")
    s=one(s,
       '                               ppt->tau_sampling,\n'
       '                               tau_actual_size,\n'
       '                               perturbations_sources,\n'
       '                               perhaps_print_variables,\n',
       '                               ge19_record_selected?ge19_tau:ppt->tau_sampling,\n'
       '                               ge19_record_selected?ge19_n:tau_actual_size,\n'
       '                               ge19_record_selected?ge19_record_callback:perturbations_sources,\n'
       '                               ge19_record_selected?NULL:perhaps_print_variables,\n',
       "EVOLVER")
    s=one(s,
       '  free(interval_limit);\n\n'
       '  return _SUCCESS_;\n}\n\n/**\n * Fill array of strings with the name of the',
       '  free(interval_limit);\n'
       '  if (ge19_tau) free(ge19_tau);\n\n'
       '  return _SUCCESS_;\n}\n\n/**\n * Fill array of strings with the name of the',
       "FREE_DENSE")
    return s

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--class-root",type=Path,required=True)
    p.add_argument("--check-only",action="store_true")
    a=p.parse_args()
    root=a.class_root.expanduser().resolve()
    src=root/"source"/"perturbations.c"
    if not src.is_file():raise SystemExit("GE19_CLASS_ROOT_MISSING: "+str(src))
    orig=src.read_text()
    if SOURCE_MARKER in orig:raise SystemExit("GE19_ALREADY_PATCHED_REFUSE")
    h=hashlib.sha256(orig.encode()).hexdigest()
    if h not in PRISTINE_SHA256:
        raise SystemExit("GE19_UNRECOGNIZED_CLASS_SOURCE_SHA256="+h+
           "; expected historical or separate quarter candidate; no source modified")
    patched=modify(orig)
    if a.check_only:
        print("GE19_FULL_CLASS_TANGENT_PATCH_ANCHORS_PASS",
              PRISTINE_SHA256[h],h)
        print("GE19_IMPLEMENTATION_NOT_COMPILED_OR_RUN")
        return
    backup=src.with_suffix(".c.ge19_original_backup")
    if backup.exists():raise SystemExit("GE19_BACKUP_EXISTS_REFUSE")
    backup.write_text(orig)
    src.write_text(patched)
    report={
       "classification":"GE19_EXPERIMENTAL_FULL_CLASS_TWO_PASS_SOURCE_PATCHED_NOT_PHYSICS_GO",
       "parent_source_sha256":h,
       "parent_source_type":PRISTINE_SHA256[h],
       "modified_source_sha256":hashlib.sha256(patched.encode()).hexdigest(),
       "original_backup":str(backup),
       "changed_file":str(src),
       "baseline_mode":"record; full original early CLASS history; dense output samples",
       "tangent_mode":"force; exact eta=0 native full state; zero tangent IC",
       "source_sampling":"linear interpolation; must run dt-halving and source accuracy audit",
       "full_class_compiled":False,"source_convergence_qualified":False,
       "production_physics_go":False,"DES_detection":False
    }
    (root/"ge19_tangent_patch_manifest.json").write_text(
       json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("GE19_FULL_CLASS_TANGENT_PATCH_APPLIED_NOT_VALIDATED",report["modified_source_sha256"])

if __name__=="__main__":
    main()
