#!/usr/bin/env python3
"""GE19 G2A: source-frozen SIGNED complex H4 stage-forcing extraction, NO ODE.

Read the *actual original Cr12abR2 exact_source_functions* (hash-locked),
its final M2 stages, original Cr12u Q6/Q7/Lambda/DY2 stages, and original
Repair37 source-by-beta. Export signed complex H4 RHS for all 40 original
modes, three beta choices, 254 saved stage points and initial x0.

This is the signed SOURCE SIDE of the mixed Ward, not the signed shift
EULER RESIDUAL Eb: its phase cannot be obtained from the saved Z21 six
fields and unsigned |Eb|. No full Noether certification or new integration.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results/d47_offclock_first_interval"
INPUTS={
 "r37":(
  ROOT/"results/ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.npz",
  "572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f"
 ),
 "cr12u":(
  OUT/"ge19_d55cr12u_all_z11_dependent_exact_stage_h4_reclosure.npz",
  "9d85d9309c616092ab609b91dd72ea4d5d5fd5c97c851ded930a1339d340ef24"
 ),
 "cr12abr2":(
  OUT/"ge19_d55cr12abr2_fine48_m2_coherent_final_cstar_h4.npz",
  "a12f4c1476edb1cd1c00625fffb9c2377ef63eeac1db90cbf4349f10cf278f49"
 ),
 "original_cr12abr2_code":(
  OUT/"d55cr12abr2_package/d55cr12abr2_fine48_m2_coherent_final_cstar_h4_repair_package/d55cr12abr2_fine48_m2_coherent_final_cstar_h4.py",
  "6f569ba44c14f1727a020e389430decf4663385bf1389550567853e1c9ec60a9"
 )
}

def sha256(p):
    h=hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda:fh.read(1<<20),b""):
            h.update(chunk)
    return h.hexdigest()

def require(ok,code):
    if not bool(ok):
        raise RuntimeError("GE19_G2A_"+code)

def as_pair(z):
    z=complex(z)
    return [float(z.real),float(z.imag)]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",type=Path,required=True)
    ap.add_argument("--npz-out",type=Path,required=True)
    args=ap.parse_args()
    require(not args.json_out.exists() and not args.npz_out.exists(),
            "OUTPUT_EXISTS_STOP_NO_OVERWRITE")
    locks={}
    for name,(p,want) in INPUTS.items():
        require(p.is_file(),"MISSING_PARENT_"+name)
        got=sha256(p)
        require(got==want,"PARENT_SHA256_CHANGED_"+name)
        locks[name]={"path":str(p.relative_to(ROOT)),"sha256":got}
    spec=importlib.util.spec_from_file_location(
       "ge19_g2a_original_locked_cr12abr2",INPUTS["original_cr12abr2_code"][0])
    require(spec is not None and spec.loader is not None,"SOURCE_MODULE_NOT_FOUND")
    cr=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cr)
    require(cr.TAG=="C_star" and abs(cr.SHIFT_TARGET-1e-6)<1e-30,
            "ORIGINAL_H4_SCOPE_CHANGED")
    with np.load(INPUTS["r37"][0],allow_pickle=False) as r37, \
         np.load(INPUTS["cr12u"][0],allow_pickle=False) as cr12u, \
         np.load(INPUTS["cr12abr2"][0],allow_pickle=False) as cr12:
        x=np.asarray(r37["x_primary"],float)
        stage_x=np.asarray(cr12["stage_x"],float)
        require(x.shape==(128,) and stage_x.shape==(254,),
                "ORIGINAL_CLOCK_SHAPE_CHANGED")
        require(np.array_equal(stage_x[1::2],x[1:]),
                "ORIGINAL_RADAU_RIGHT_STAGE_MISMATCH")
        require(np.array_equal(stage_x,np.asarray(cr12u["stage_x"],float)),
                "CR12U_STAGE_COORDINATE_MISMATCH")
        modes=np.asarray(cr.r7.M_SOLVE,dtype=int)
        betas=np.asarray(cr.r7.BETAS,float)
        require(modes.shape==(40,) and betas.shape==(3,),
                "ORIGINAL_MODES_OR_BETA_CHANGED")
        full_x=np.r_[x[:1],stage_x]
        old_sources=cr.r38.frozen_source_by_beta(r37,cr.TAG)
        m2new=(np.asarray(cr12["sub48_M2_main_stage"],complex),
               np.asarray(cr12["sub48_M2_constraint_stage"],complex))
        # Axes: beta, mode, original Euler row, time.  Index 0 = x0;
        # indices 1..254 are EXACT original Cr12abR2 Radau source nodes.
        signed_main=np.empty((3,40,6,255),complex)
        signed_constraint=np.empty((3,40,2,255),complex)
        old_main=np.empty_like(signed_main)
        old_constraint=np.empty_like(signed_constraint)
        for jm,mode in enumerate(modes):
            signed_rhs,signed_con=cr.exact_source_functions(
                x,stage_x,cr12u,m2new,r37,int(mode))
            base_rhs,base_con=cr.r7._source_interp(
                x,old_sources,int(mode))
            for jt,xc in enumerate(full_x):
                # Each evaluator is the original frozen code, not an
                # interpolator newly fitted to the Cr12 stage values.
                a=np.asarray(signed_rhs(float(xc)),complex)
                b=np.asarray(signed_con(float(xc)),complex)
                ao=np.asarray(base_rhs(float(xc)),complex)
                bo=np.asarray(base_con(float(xc)),complex)
                require(a.shape==(6,3) and b.shape==(2,3) and
                        ao.shape==(6,3) and bo.shape==(2,3),
                        "SOURCE_ROW_OR_BETA_SHAPE_MISMATCH")
                signed_main[:,jm,:,jt]=a.T
                signed_constraint[:,jm,:,jt]=b.T
                old_main[:,jm,:,jt]=ao.T
                old_constraint[:,jm,:,jt]=bo.T
        arrays=(signed_main,signed_constraint,old_main,old_constraint)
        require(all(np.isfinite(a).all() for a in arrays),
                "NONFINITE_SIGNED_STAGE_SOURCE")
        require(np.array_equal(signed_main[:,:,:,0],old_main[:,:,:,0]) and
                np.array_equal(signed_constraint[:,:,:,0],
                               old_constraint[:,:,:,0]),
                "INITIAL_SOURCE_NOT_INHERITED")
        # Explicit source component decomposition independent of the
        # original function at ONE physical hotspot, to detect
        # accidentally altered row ordering or a missing action piece.
        ix=int(np.where(modes==40)[0][0])
        it=48  # output index 48 corresponds to stage 47 = original x24
        stage_idx=it-1
        require(stage_idx==47 and full_x[it]==x[24],
                "HOTSPOT_STAGE_INDEX_CHANGED")
        part_r=old_main[:,ix,:,it].T.copy()
        part_c=old_constraint[:,ix,:,it].T.copy()
        keys=(cr.Q6,cr.Q7,cr.QL,cr.DY,cr.M2)
        newm={
          cr.Q6:np.asarray(cr12u["sub48_QGE06_main_stage"],complex)[:,stage_idx,40],
          cr.Q7:np.asarray(cr12u["sub48_QGE07_main_stage"],complex)[:,stage_idx,40],
          cr.QL:np.asarray(cr12u["sub48_QLambda_main_stage"],complex)[:,stage_idx,40],
          cr.DY:np.asarray(cr12u["sub48_DY2_main_stage"],complex)[:,:,stage_idx,40].T,
          cr.M2:m2new[0][:,stage_idx,40]
        }
        newc={
          cr.Q6:np.asarray(cr12u["sub48_QGE06_constraint_stage"],complex)[:,stage_idx,40],
          cr.Q7:np.asarray(cr12u["sub48_QGE07_constraint_stage"],complex)[:,stage_idx,40],
          cr.QL:np.asarray(cr12u["sub48_QLambda_constraint_stage"],complex)[:,stage_idx,40],
          cr.DY:np.asarray(cr12u["sub48_DY2_constraint_stage"],complex)[:,:,stage_idx,40].T,
          cr.M2:m2new[1][:,stage_idx,40]
        }
        for key in keys:
            pp=cr.r42.frozen_piece_by_beta(r37,cr.TAG,key)
            oldr,oldc=cr.r7._source_interp(x,pp,40)
            part_r-=np.asarray(oldr(float(x[24])),complex)
            part_c-=np.asarray(oldc(float(x[24])),complex)
            v=newm[key];u=newc[key]
            part_r+=v[:,None] if v.ndim==1 else v
            part_c+=u[:,None] if u.ndim==1 else u
        reconstructed_max=max(float(np.max(np.abs(
                   part_r-signed_main[:,ix,:,it].T))),
                     float(np.max(np.abs(
                   part_c-signed_constraint[:,ix,:,it].T))))
        # Floating sum regrouping can change last ULP; this is a
        # numerical implementation cross-check, not a physical bound.
        refmax=max(1.,float(np.max(np.abs(part_r))),
                       float(np.max(np.abs(part_c))))
        require(reconstructed_max<1e-12*refmax,
                "INDEPENDENT_SIGNED_PIECE_RECONSTRUCTION_MISMATCH")
        mask=np.asarray(cr12["frozen_Cstar_active_mask"],bool)
        shift=np.asarray(cr12["final_shift_metric"],float)
        require(mask.shape==(3,40,128) and shift.shape==mask.shape,
                "FROZEN_ACTIVE_SHIFT_MASK_CHANGED")
        report={
          "classification":"GE19_G2A_ORIGINAL_SIGNED_H4_STAGE_FORCING_RECOVERED_FULL_PARENT_WARD_OPEN",
          "parent_locks":locks,
          "scope":{"tag":"C_star","Nt":128,"modes":modes.tolist(),
                   "beta_values":betas.tolist(),"source_times":255,
                   "first_time_is_original_x0":True,
                   "later_times_are_254_frozen_Radau_stages":True},
          "signed_source_hotspot_m40_beta_index1_node24":{
               "x":float(x[24]),
               "original_R37_shift_source":as_pair(old_constraint[1,ix,0,it]),
               "final_Cr12abr2_shift_source":as_pair(signed_constraint[1,ix,0,it]),
               "final_Cr12abr2_anisotropy_source":as_pair(
                                          signed_constraint[1,ix,1,it]),
               "final_Cr12abr2_isotropic_source":as_pair(
                                          signed_main[1,ix,1,it]),
               "frozen_final_active_shift_normalized":
                                          float(shift[1,ix,24]),
               "signed_residual_Eb_not_saved":True},
          "source_stage_beta_spread":{
            "main_max_abs":float(max(
                np.max(np.abs(signed_main[0]-signed_main[b])) for b in (1,2))),
            "shift_source_max_abs":float(max(
                np.max(np.abs(signed_constraint[0,:,0,:]-
                              signed_constraint[b,:,0,:])) for b in (1,2)))},
          "independent_component_source_crosscheck_max_abs":reconstructed_max,
          "first_node_old_source_preserved":True,
          "no_h4_ODE_run":True,
          "source_finite_stage_values_do_not_define_unique_continuum":True,
          "physical_parent_Rparent_Bparent_enclosed":False,
          "signed_complex_shift_Eb_recovered":False,
          "signed_longitudinal_EL_recovered":False,
          "full_original_H4_Ward_certified":False,
          "Z21_certified":False,
          "lensing_licensed":False,
          "original_cr12abr2_implementation_and_science_FAIL_preserved":True,
          "next_physics":"Compare recovered signed stage sources to independently evaluated action parent/Noether currents on a single common physical clock. Reconstruct actual complex Eb/EL from original canonical stages only with explicit replay/provenance; never infer phase from abs residual and never equate stage agreement to continuous Ward."
        }
    args.json_out.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(args.npz_out,
        x_primary=x,source_x=x,stage_x=stage_x,full_x=full_x,
        modes=modes,betas=betas,
        original_R37_main_signed=old_main,
        original_R37_constraint_signed=old_constraint,
        original_Cr12abr2_main_signed=signed_main,
        original_Cr12abr2_constraint_signed=signed_constraint)
    args.json_out.write_text(json.dumps(report,sort_keys=True,
                              indent=2,allow_nan=False)+"\n")
    print(report["classification"])
    print("SIGNED_SOURCE_HOTSPOT",
          json.dumps(report["signed_source_hotspot_m40_beta_index1_node24"]))
    print("ORIGINAL_OUTPUTS",args.json_out,args.npz_out)

if __name__=="__main__":
    main()
