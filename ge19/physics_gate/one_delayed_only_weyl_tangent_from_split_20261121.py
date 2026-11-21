#!/usr/bin/env python3
"""GE19 one frozen native CLASS delayed-only Weyl tangent from archived split.

Never redoes baseline or bath inversion, never modifies CLASS source, no
parameter sweep. One CLASS forced run, conditional on exact source provenance.
PROVISIONAL IMPLEMENTATION DIAGNOSTIC, NOT PHYSICAL MEMORY OR DES DETECTION.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math,os,subprocess
from pathlib import Path

import run_full_class_two_pass_tangent_20261112 as base

ROOT=Path(__file__).resolve().parents[2]
RESPONSE_RUNNER_BLOB="94af6d14826d0621410204554e9d246a89660806"
RECONSTRUCTION_RUNNER_BLOB="e45b4d3d1a7328540793796a8c0896eb013ac2ce"
SPLIT_REPORT_SHA256="aefa147ed929db0bfb53892ea6f2b1c276d57aa355b79a1701ea40f0d814f591"
BASELINE_SHA256="fbe1212cbc052343e283edae1c7496e631da6056ad983d575fd2d699e9bf2e19"
NULL_SHA256="7cf0d48dd7bce488c81cdad7e3270ec258f8a4b1e954d574f87c2a1811a877ac"
ORIGINAL_TOTAL_REPORT_SHA256="3bbaa3cb99292d90e15cfef5f643f1484b5d34a58475bc43f0221294383e936e"
FROZEN_CLASS_PATCH_SHA256="c41ad4cad9cc18d658f80841137094349657df6ac5d68fd3c0c75cfbbe092073"
FROZEN_INI_BLOB="f9a2bde8921a148e063f9657a8ede0a51c6a629d"

def require(condition,label):
 if not bool(condition):raise RuntimeError("GE19_DELAYED_TANGENT_"+label)

def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()

def csv_source_consistency(baseline,instant,delayed):
 """Check exact input coordinates/W and signed additivity across ALL rows."""
 maximum=0.
 count=0
 with baseline.open(newline='') as fa,instant.open(newline='') as fi,delayed.open(newline='') as fd:
  A=csv.DictReader(fa);I=csv.DictReader(fi);D=csv.DictReader(fd)
  require(A.fieldnames==I.fieldnames==D.fieldnames==
          ['tau','a','k_mpc','W','Bchi'],'TRACE_COLUMNS')
  for row in zip(A,I,D):
   vals=[]
   for rec in row:
    x=tuple(float(rec[k]) for k in A.fieldnames)
    require(all(map(math.isfinite,x)),'NONFINITE_SPLIT')
    vals.append(x)
   (aa,ii,dd)=vals
   require(all(aa[j]==ii[j]==dd[j] for j in range(4)),
           'SPLIT_COORDINATES_OR_BASELINE_WEYL_MISMATCH')
   require(aa[2]==base.K_MPC,'K_SOURCE_NOT_FROZEN')
   maximum=max(maximum,abs(aa[4]-(ii[4]+dd[4])))
   count+=1
  # zip truncation cannot silently discard trailing source records.
  require(next(A,None) is None and next(I,None) is None and next(D,None) is None,
          'TRACE_LENGTH_MISMATCH')
 require(count==141494,'TRACE_ROW_COUNT_CHANGED')
 require(maximum<5e-11*(1+7837.613561516323),'SPLIT_NOT_ADDITIVE')
 return count,maximum

def preflight(opts):
 repo=ROOT.resolve()
 for source,expected in (
   ("ge19/physics_gate/run_full_class_two_pass_tangent_20261112.py",RESPONSE_RUNNER_BLOB),
   ("ge19/physics_gate/reconstruct_native_Bchi_instant_delayed_fast_20261120.py",RECONSTRUCTION_RUNNER_BLOB),
 ):
  f=repo/source
  require(f.is_file(),'RUNNER_SOURCE_MISSING_'+source)
  blob=subprocess.check_output(["git","hash-object",str(f)],cwd=repo,text=True).strip()
  require(blob==expected,'RUNNER_SOURCE_CHANGED_'+source)
 ini=opts.original_ini.resolve()
 require(ini.is_file(),'FROZEN_INI_MISSING')
 blob=subprocess.check_output(["git","hash-object",str(ini)],text=True).strip()
 require(blob==FROZEN_INI_BLOB,'FROZEN_INI_CHANGED')
 manifest=base.patched_source_qualification(opts.class_root.resolve())
 require(manifest['modified_source_sha256']==FROZEN_CLASS_PATCH_SHA256,
         'CLASS_PATCH_NOT_ORIGINAL_ONE_FORCED')
 split=opts.split_dir.resolve()
 require(split.is_dir(),'SPLIT_DIR_MISSING')
 report_path=split/"GE19_BCHI_SOURCE_SPLIT_DIAGNOSTIC.json"
 require(report_path.is_file() and sha(report_path)==SPLIT_REPORT_SHA256,
         'SPLIT_DIAGNOSTIC_SHA_MISMATCH')
 rep=json.loads(report_path.read_text())
 require(rep['classification']=="GE19_HISTORIC_BCHI_INSTANT_DELAYED_NUMERICALLY_RECONSTRUCTED_NOT_PHYSICAL_WEYL",
         'SPLIT_CLASSIFICATION_CHANGED')
 require(rep.get('internal_RK4_refinement_verified') is True,
         'SPLIT_REFINEMENT_NOT_VERIFIED')
 require(rep.get('independent_numerical_convergence_verified') is False,
         'INVALID_SPLIT_INDEPENDENCE_ASSERTION')
 require(rep.get('W1_delayed_computed') is False,'SPLIT_ALREADY_HAS_WEYL_RESULT')
 require(rep['sample_count']==141494 and rep['original_baseline_sha256']==BASELINE_SHA256,
         'ORIGINAL_BATH_HISTORY_MISMATCH')
 inst=split/"instantaneous_Bchi.csv"
 delayed=split/"delayed_Bchi.csv"
 require(inst.is_file() and delayed.is_file(),'SPLIT_CSV_MISSING')
 require(sha(inst)==rep["output_csv_sha256"]["instantaneous"],
         'INSTANT_FILE_SHA_MISMATCH')
 require(sha(delayed)==rep["output_csv_sha256"]["delayed"],
         'DELAYED_FILE_SHA_MISMATCH')
 old=opts.existing_dir.resolve()
 baseline=old/"baseline_dt010.csv"
 null=old/"null_W1.csv"
 require(baseline.is_file() and sha(baseline)==BASELINE_SHA256,
         'ORIGINAL_BASELINE_CHANGED')
 require(null.is_file() and sha(null)==NULL_SHA256,
         'ORIGINAL_NULL_CHANGED')
 require((old/"base010.log").is_file() and (old/"null.log").is_file(),
         'ORIGINAL_CLASS_LOGS_MISSING')
 n,err=csv_source_consistency(baseline,inst,delayed)
 total=repo/"results/ge19_one_forced_tangent_20261113/GE19_ONE_FORCED_TANGENT_SCREEN.json"
 require(total.is_file() and sha(total)==ORIGINAL_TOTAL_REPORT_SHA256,
         'ORIGINAL_TOTAL_WEYL_REPORT_CHANGED')
 old_report=json.loads(total.read_text())
 require(old_report["classification"]=="GE19_ONE_FORCED_NATIVE_CLASS_TANGENT_PROVISIONAL_ONLY",
         'TOTAL_REPORT_WRONG_CLASSIFICATION')
 require(old_report["class_source_patch_current_sha256"]==FROZEN_CLASS_PATCH_SHA256,
         'CLASS_REPORT_PATCH_MISMATCH')
 require(old_report["original_history_sha256"]==BASELINE_SHA256,
         'CLASS_REPORT_BASELINE_MISMATCH')
 require(old_report["original_null_sha256"]==NULL_SHA256,
         'CLASS_REPORT_NULL_MISMATCH')
 require(old_report["fixed_k_Mpc_inverse"]==base.K_MPC and
         old_report["target_z"]==0.5,'OLD_REPORT_UNEXPECTED_MODE')
 out=opts.out_dir.resolve()
 require(not out.exists(),'OUTPUT_EXISTS')
 require(out!=old and old not in out.parents and
         out!=split and split not in out.parents,
         'OUTPUT_UNSAFE_PARENT')
 return {
  'manifest':manifest,'original':old_report,'source_n':n,
  'additivity_error':err,'baseline':baseline,'null':null,
  'delayed':delayed,'instant':inst,'report':report_path,'out':out,
 }

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--class-root',type=Path,required=True)
 p.add_argument('--existing-dir',type=Path,required=True)
 p.add_argument('--split-dir',type=Path,required=True)
 p.add_argument('--original-ini',type=Path,default=ROOT/'v019/ini/aest_exp.ini')
 p.add_argument('--out-dir',type=Path,required=True)
 p.add_argument('--run',action='store_true',help='explicit opt-in to ONE CLASS run')
 opts=p.parse_args()
 accepted=preflight(opts)
 orig=accepted['original']
 print("GE19_DELAYED_TANGENT_PREFLIGHT_PASS",
       accepted['source_n'],"additivity_abs",
       format(accepted['additivity_error'],'.17g'),flush=True)
 print("GE19_REFERENCE_TOTAL_W1",format(orig["forced_W1_at_z0p5"],'.17g'),flush=True)
 if not opts.run:
  print("GE19_DELAYED_TANGENT_DRY_RUN_ONLY",flush=True)
  print("GE19_FULL_PHYSICS_GO False",flush=True)
  return
 out=accepted['out']
 out.mkdir(parents=True)
 (out/'native').mkdir()
 cfg=base.make_ini(opts.original_ini.resolve(),out,"force_delayed",2e-7)
 env=os.environ.copy()
 env['OMP_NUM_THREADS']='1'
 env['GE19_TANGENT_MODE']='force'
 env['GE19_TANGENT_K_MPC']=format(base.K_MPC,'.12g')
 env['GE19_TANGENT_TRACE']=str(accepted['delayed'])
 env['GE19_TANGENT_OUT']=str(out/'delayed_only_W1.csv')
 env.pop('GE19_TANGENT_ZERO_SOURCE',None)
 print("GE19_ONE_DELAYED_CLASS_TANGENT_START",flush=True)
 base.run_class(opts.class_root.resolve(),cfg,out/'delayed_only_CLASS.log',env)
 print("GE19_ONE_DELAYED_CLASS_TANGENT_FINISHED",flush=True)
 records=base.read_trace(out/'delayed_only_W1.csv')
 Wd=base.interpolate_a(records)
 Wtot=orig["forced_W1_at_z0p5"]
 Wi=Wtot-Wd
 W0=orig["baseline_W0_at_z0p5"]
 report={
  "classification":"GE19_HISTORICAL_CLASS_DELAYED_ONLY_WEYL_TANGENT_PROVISIONAL",
  "single_new_CLASS_run_complete":True,
  "k_Mpc_inverse":base.K_MPC,"target_z":0.5,
  "original_total_W1_at_z_0p5":Wtot,
  "delayed_W1_at_z_0p5":Wd,
  "instantaneous_W1_inferred_by_subtraction_not_independently_run":Wi,
  "delayed_over_total_signed":Wd/Wtot if Wtot!=0 else None,
  "instantaneous_over_total_signed_inferred":Wi/Wtot if Wtot!=0 else None,
  "delayed_over_baseline_W0_per_unit_eta":Wd/W0 if W0!=0 else None,
  "source_additivity_max_abs":accepted['additivity_error'],
  "history_split_report_sha256":sha(accepted['report']),
  "delayed_source_sha256":sha(accepted['delayed']),
  "original_total_report_sha256":ORIGINAL_TOTAL_REPORT_SHA256,
  "class_patch_sha256":FROZEN_CLASS_PATCH_SHA256,
  "interpolation_policy":"Linear in a at a=2/3; historical sparse readout, no error bound",
  "independent_instantaneous_W1_run":False,
  "independent_numerical_convergence_certified":False,
  "true_first_saved_bath_initial_state_certified":False,
  "independent_original_q_chi_trace_validation":False,
  "full_action_to_CLASS_Ward_certified":False,
  "correct_physical_finite_k_primordial_mode_certified":False,
  "physical_delayed_Weyl_certified":False,
  "DES_detection":False,"FULL_PHYSICS_GO":False,
 }
 path=out/'GE19_DELAYED_ONLY_WEYL_SCREEN.json'
 path.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
 print("GE19_HISTORIC_DELAYED_WEYL_TANGENT_PROVISIONAL",
       format(Wd,'.17g'),"SIGNED_RATIO",format(report['delayed_over_total_signed'],'.17g'),
       flush=True)
 print("GE19_REPORT",path,flush=True)
 print("GE19_FULL_PHYSICS_GO False",flush=True)

if __name__=='__main__':main()
