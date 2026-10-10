#!/usr/bin/env python3
"""Pure static tests: do not require a local AeST repository or original H1."""
import ast
import hashlib
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'ge19/h4f3d32_independent_sector_first_interval.py'
PRE=ROOT/'ge19/h4f3d32_independent_sector_first_interval_prereg.json'
LOCK=ROOT/'ge19/h4f3d32_independent_sector_first_interval_lock.json'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def test():
    prereg=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
    assert prereg['classification']=='GE19_D32_PREEXEC_INDEPENDENT_SIGNED_SECTOR_FIRST_INTERVAL'
    assert prereg['original_shift_gate']==prereg['original_boundary_backward_gate']==1e-6
    assert prereg['cases']==[[14,0.1],[1,1.0],[40,0.1]]
    assert prereg['substeps']==[1,8] and prereg['off_support_modes']==[1,14]
    assert prereg['m40_source_relative_limit']==1e-11
    assert prereg['m40_endpoint_state_relative_limit']==1e-8
    assert prereg['no_observational_tuning'] and prereg['production_source_unchanged']
    assert prereg['original_D22A_shift_failure_immutable'] and prereg['original_D31R1_shift_failure_immutable']
    assert lock['classification']=='GE19_D32_SOURCE_PREREG_STATIC_RUNNER_SHA256_LOCK'
    for f,want in lock['sha256_local_files'].items():
        assert len(want)==64 and sha(ROOT/f)==want,('D32 own SHA lock FAIL',f)
    for f,want in prereg['frozen_local_code_sha256'].items():
        assert len(want)==64 and len(f)>0
    for f,want in prereg['frozen_results_sha256'].items():
        assert len(want)==64 and len(f)>0
    tree=ast.parse(SOURCE.read_text())
    fun=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='independent_candidate')
    ns={'np':np}
    exec(compile(ast.Module(body=[fun],type_ignores=[]),str(SOURCE),'exec'),ns)
    independent=ns['independent_candidate']
    shape=(6,128,41);conshape=(2,128,41)
    ga=np.zeros(shape,dtype=complex);gc=np.zeros(conshape,dtype=complex)
    ma=np.zeros(shape,dtype=complex);mc=np.zeros(conshape,dtype=complex)
    lam=np.zeros(shape,dtype=complex);y=np.zeros(shape,dtype=complex)
    ga[3,0,40]=4+2j;gc[0,0,40]=1-1j
    ma[0,0,14]=0.13+0.03j;mc[0,0,14]=1e-28-2e-28j
    lam[0,0,14]=0.23+0.10j
    y[3,0,14]=2e-9+4e-9j;y[3,0,1]=1e-9-2e-9j
    B,base=independent(ga,gc,ma,mc,lam,y)
    assert B['rhs'].shape==shape and B['rhs_constraint'].shape==conshape
    assert np.array_equal(B['rhs'][3,:,14],y[3,:,14])
    assert np.array_equal(B['rhs'][3,:,1],y[3,:,1])
    assert np.array_equal(B['rhs']-base,y)
    assert B['rhs'][0,0,14]==ma[0,0,14]+lam[0,0,14]
    assert B['rhs_constraint'][0,0,14]==mc[0,0,14]
    assert B['rhs'][3,0,40]==ga[3,0,40]
    # Negatives: omitting Y or reversing GE07/shift cannot satisfy the source.
    wrong_no_y=base
    wrong_ge07_con=gc-mc
    assert wrong_no_y[3,0,14]!=B['rhs'][3,0,14]
    assert wrong_ge07_con[0,0,14]!=B['rhs_constraint'][0,0,14]
    try:
        independent(ga,gc,ma[:,:,:40],mc,lam,y)
    except RuntimeError:pass
    else:raise AssertionError('D32 wrong shape not rejected')
    bad=ma.copy();bad[0,0,14]=np.nan
    try:
        independent(ga,gc,bad,mc,lam,y)
    except RuntimeError:pass
    else:raise AssertionError('D32 nonfinite sector not rejected')
    # The preregistered source B is additive, independent of subtractive A.
    assert 'orig' not in independent.__code__.co_varnames
    print('GE19_D32_MANUFACTURED_INDEPENDENT_SIGNED_SECTORS_Y_RETENTION_AND_NEGATIVE_CONTROLS_PASS',flush=True)
    print('GE19_D32_SHA_PREREG_NO_GATE_CHANGE_STATIC_PASS',flush=True)

if __name__=='__main__':test()
