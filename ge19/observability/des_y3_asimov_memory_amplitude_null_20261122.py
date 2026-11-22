#!/usr/bin/env python3
"""GE19 DES Y3 Asimov IDENTIFIABILITY screen, no observed residuals read.

This is an exact null control for a shape-uniform *historical one-point* Weyl
ratio promoted only as a mathematical comparator, NOT a physical DES template.
A fully action-certified delayed galaxy-shear derivative is NOT available.
Reads ONLY GR theory, covariance, and tomographic indices from frozen OBS06;
does not access any observed DATA/VALUE/residual vectors and never fits DES.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

PINNED_OBS06_SHA256 = "564542d47fa95d5b5fb3c5b0c8bb4eae1ecbc93f450bf993ea0bbb98310546e3"
HISTORICAL_ONE_POINT_W1_DELAYED_OVER_W0_PER_ETA = -1.712922233834667e-9
COV_KEYS=("cov","covariance","C","covmat","cov_192","gammat_covariance")
GR_KEYS=("theory","theory_vector","gammat_theory","gr_theory","theory_gammat","prediction","mu_gr","pred")
LENS_KEYS=("bin1","BIN1","lens_bin","lens","lens_bins","bin_lens")
SOURCE_KEYS=("bin2","BIN2","source_bin","source","source_bins","bin_source")
PAIR_KEYS=("pairs","bin_pairs","tomographic_pairs")

def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def find_reference(root: Path):
    dirs=[root/"observations/des_y3",root/"results",root/"observations"]
    hits=[]
    for d in dirs:
        if d.is_dir():
            hits.extend(d.rglob("obs06_fixed_gr_192.npz"))
    return sorted({p.resolve() for p in hits})

def describe(z, file_path):
    # Parse .npy HEADERS without calling z[k] or reading observed data values.
    # Manifest must never load the observed VALUE/data/residual arrays.
    import zipfile
    from numpy.lib import format as fmt
    out={}
    with zipfile.ZipFile(file_path) as archive:
        for k in z.files:
            with archive.open(k+".npy") as fd:
                version=fmt.read_magic(fd)
                if version==(1,0):
                    shape,fortran,dtype=fmt.read_array_header_1_0(fd)
                elif version in ((2,0),(3,0)):
                    shape,fortran,dtype=fmt.read_array_header_2_0(fd)
                else:
                    raise ValueError("unsupported NPY header "+str(version))
                out[k]={"shape":list(shape),"dtype":str(dtype)}
    return out

def pick(z,keys,ndim=None,shape=None):
    found=[k for k in keys if k in z.files and
           (ndim is None or z[k].ndim==ndim) and
           (shape is None or z[k].shape==shape)]
    return found[0] if len(found)==1 else None,found

def whiten_projection(mu,cov,template,source_bins):
    # Each source-bin has one free overall shear amplitude. These are
    # conservative diagnostic nuisances, not the full DES likelihood.
    mu=np.asarray(mu,dtype=float)
    template=np.asarray(template,dtype=float)
    n=mu.size
    if n<4 or cov.shape!=(n,n):
        raise ValueError("bad selected dimensions")
    if not (np.all(np.isfinite(mu)) and np.all(np.isfinite(cov)) and
            np.all(np.isfinite(template))):
        raise ValueError("nonfinite numeric input")
    if not np.allclose(cov,cov.T,rtol=1e-10,atol=1e-18):
        raise ValueError("covariance not symmetric")
    import scipy.linalg as la
    L=la.cholesky(cov,lower=True,check_finite=True)
    v=la.solve_triangular(L,template,lower=True)
    cols=[mu*(source_bins==s) for s in sorted(set(source_bins.tolist()))]
    A=np.stack(cols,axis=1)
    Aw=la.solve_triangular(L,A,lower=True)
    U,sing,_=la.svd(Aw,full_matrices=False)
    thresh=100*np.finfo(float).eps*max(Aw.shape)*max(sing)
    rank=int(np.sum(sing>thresh))
    if rank!=A.shape[1]:
        raise ValueError("GR amplitudes unidentifiable on the selected pairs")
    residual=v-U[:,:rank]@(U[:,:rank].T@v)
    info_raw=float(v@v)
    info_prof=float(residual@residual)
    relative_projection_residual=float(np.linalg.norm(residual)/max(np.linalg.norm(v),1e-300))
    return {
      "rows":n,"source_bins":sorted(set(int(v) for v in source_bins)),
      "nuisance_amplitude_columns":A.shape[1],"nuisance_rank":rank,
      "F_unprofiled":info_raw,
      "F_profiled_numeric_roundoff":info_prof,
      "relative_whitened_projection_residual":relative_projection_residual,
      "SNR_eta1_unprofiled":float(np.sqrt(info_raw)),
      "SNR_eta1_profiled_numeric_roundoff":float(np.sqrt(info_prof)),
    }

def run(path):
    r={"classification":"GE19_DES_Y3_ASIMOV_PROXY_NOT_A_PHYSICAL_MEMORY_FORECAST",
       "data_used":"GR model reference, full covariance and tomographic metadata ONLY; never observed values or residuals",
       "probe":"MagLim lens bin 4 x source bin 4; source bin 3 fixed control",
       "source_template":"UNPHYSICAL constant-fraction null control, scaled by historical ONE (k,z) Weyl ratio only",
       "fraction_per_eta":HISTORICAL_ONE_POINT_W1_DELAYED_OVER_W0_PER_ETA,
       "physical_delayed_gamma_t_template_present":False,
       "physical_forecast_GO":False,"DES_detection":False,
       "observable_template_identifiable":None}
    if path is None:
        r["classification"]="GE19_ASIMOV_ASSET_BLOCKED_REFERENCE_MISSING"
        r["next_required"]="Provide exact OBS06 reference NPZ: obs06_fixed_gr_192.npz, SHA256 pinned; do not use observed VALUE as theory."
        return r
    r["reference_path"]=str(path)
    r["reference_sha256"]=sha256(path)
    if r["reference_sha256"]!=PINNED_OBS06_SHA256:
        r["classification"]="GE19_ASIMOV_ASSET_BLOCKED_REFERENCE_SHA_MISMATCH"
        r["expected_sha256"]=PINNED_OBS06_SHA256
        return r
    with np.load(path,allow_pickle=False) as z:
        r["npz_manifest"]=describe(z,path)
        gkey,gfound=pick(z,GR_KEYS,ndim=1)
        if gkey is None:
            r["classification"]="GE19_ASIMOV_ASSET_BLOCKED_GR_KEY_AMBIGUOUS_OR_ABSENT"
            r["GR_candidates"]=gfound
            return r
        gr=np.asarray(z[gkey],float)
        n=gr.size
        ckey,cfound=pick(z,COV_KEYS,ndim=2,shape=(n,n))
        if ckey is None:
            r["classification"]="GE19_ASIMOV_ASSET_BLOCKED_COVARIANCE_KEY_AMBIGUOUS_OR_ABSENT"
            r["cov_candidates"]=cfound
            return r
        cov=np.asarray(z[ckey],float)
        lkey,lfound=pick(z,LENS_KEYS,ndim=1,shape=(n,))
        skey,sfound=pick(z,SOURCE_KEYS,ndim=1,shape=(n,))
        if lkey and skey:
            lens=np.asarray(z[lkey],int)
            source=np.asarray(z[skey],int)
        else:
            pkey,pfound=pick(z,PAIR_KEYS,ndim=2,shape=(n,2))
            if pkey is None:
                r["classification"]="GE19_ASIMOV_ASSET_BLOCKED_TOMOGRAPHY_MAPPING_NOT_CERTIFIED"
                r["lens_candidates"]=lfound
                r["source_candidates"]=sfound
                r["pair_candidates"]=pfound
                return r
            pair=np.asarray(z[pkey],int)
            lens,source=pair[:,0],pair[:,1]
        r["array_keys_used"]={"GR":gkey,"covariance":ckey,"lens_mapping":lkey,"source_mapping":skey}
        # Explicitly fail closed on 0-based labels; never silently relabel.
        r["tomographic_label_ranges"]={"lens":[int(lens.min()),int(lens.max())],
                                       "source":[int(source.min()),int(source.max())]}
        if np.any(lens<=0) or np.any(source<=0):
            r["classification"]="GE19_ASIMOV_ASSET_BLOCKED_ZERO_BASED_OR_INVALID_BIN_LABELS"
            return r
        # Full published MagLim convention: lens/source bins 1-based.
        selected=(lens==4)&np.isin(source,[3,4])
        counts={str(s):int(np.sum((lens==4)&(source==s))) for s in [3,4]}
        r["selected_rows_per_source"]=counts
        if any(v<3 for v in counts.values()):
            r["classification"]="GE19_ASIMOV_ASSET_BLOCKED_WRONG_BIN_CONVENTION_OR_CUTS"
            return r
        ids=np.flatnonzero(selected)
        submu=gr[ids]
        subcov=cov[np.ix_(ids,ids)]
        sources=source[ids]
        # This deliberately IMPOSES a constant fractional model, not a
        # claimed physical prediction: exactly collinear with amplitude nuisances.
        t=HISTORICAL_ONE_POINT_W1_DELAYED_OVER_W0_PER_ETA*submu
        stats=whiten_projection(submu,subcov,t,sources)
        if stats["relative_whitened_projection_residual"]>1e-10:
            raise RuntimeError("PROXY_COLLINEARITY_NEGATIVE_CONTROL_FAILED")
        r["asymptotic_fisher_null_identity"]="t=epsilon*mu; D=[mu*I_source3,mu*I_source4]; hence t in col(D), F_perp=0 exactly"
        r["numeric_profiled_F_is_roundoff_not_evidence"]=True
        r["diagnostic"]=stats
        r["observable_template_identifiable"]=False
        r["classification"]="GE19_DES_Y3_FROZEN_GR_COVARIANCE_PROXY_AMPLITUDE_DEGENERACY_PASS_ONLY"
    return r

def self_test():
    mu=np.array([1.8,1.1,0.8,0.4,2.0,1.4,1.0,0.5])
    src=np.array([3]*4+[4]*4)
    T=np.arange(8,dtype=float)
    M=np.eye(8)+0.05*np.outer(np.sin(T),np.sin(T))
    C=M@M.T
    stats=whiten_projection(mu,C,0.017*mu,src)
    assert stats["SNR_eta1_unprofiled"]>0
    assert stats["relative_whitened_projection_residual"]<1e-12
    # A genuine (not physically licensed) shape-changing test must remain.
    t=np.array([.2,-.1,.1,-.08,.15,-.12,.04,.08])
    v=whiten_projection(mu,C,t,src)
    assert v["SNR_eta1_profiled_numeric_roundoff"]>0.01
    print("GE19_ASIMOV_PROJECTION_SELFTEST_PASS 3",flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
    p.add_argument("--reference-npz",type=Path)
    p.add_argument("--out",type=Path)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        self_test()
        return
    if a.reference_npz is not None:
        path=a.reference_npz.expanduser().resolve()
        if not path.is_file():raise FileNotFoundError(path)
    else:
        matches=find_reference(a.repo_root.resolve())
        if len(matches)>1:
            raise RuntimeError("AMBIGUOUS_OBS06_REFERENCE "+repr([str(p) for p in matches]))
        path=matches[0] if matches else None
    self_test()
    result=run(path)
    print(result["classification"],flush=True)
    print("GE19_PHYSICAL_MEMORY_TEMPLATE_GO False",flush=True)
    print("GE19_DES_DETECTION False",flush=True)
    if a.out:
        out=a.out.expanduser().resolve()
        if out.exists():raise RuntimeError("REFUSE_OVERWRITE "+str(out))
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
        print("GE19_ASIMOV_REPORT "+str(out),flush=True)
    else:print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":main()
