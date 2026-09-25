#!/usr/bin/env python3
"""GE19 H4F3d10: actual first-order nonbath Euler and KNOWN boundary only.

Use original H3F H1 and certified Repair32B Z11; keep FD4 and FD8 distinct.
Unknown E00*F21, L21*EL00 and b21*Eb00 are NOT silently zeroed.
Run only from a dedicated isolated local runner (historical imports write files).
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
import numpy as np
from ge19 import h4f3b_actual_corrected_six_piece_source as s
from ge19 import repair37_cancellation_safe_fd8_h4_z21_reclosure as old

ROOT=Path(__file__).resolve().parents[1]
PRE="7aafe872f32057ab46ed99650b3df1803050077e"
PIN={
"ge19/h4f3d10_predata_actual_nonbath_first_order_known_boundary.json":PRE,
"ge19/h4f3d8_independent_nonbath_euler_and_boundary.py":"861cd5a81c17380a727777a4e1ff08cd7e857522",
"ge19/h4f3b_actual_corrected_six_piece_source.py":"0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c",
"ge19/h4f3d6_actual_normalized_bath_parent_ward.py":"0419145499f5f44e06ba0c96f779c2a604e84ce7",
"ge19/h4f3d7r1_physical_output_finite_check_repair.py":"e4cb9d6638b427368647a29b86ccf5445b43d7a2",
"ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py":"45d203a092f9ac71cc612b15df5f0c0c630f5898",
"ge06/analytic_aest_directional_source_generator.py":"a7afe0035054a9dca55d74a6497c081422114b4c",
"ge07/pressureless_matter_directional_source_generator.py":"cde8da77a80799cef00fc7c09c3633310fc9e3d4"}
SHA={
"source_json":"1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1",
"source_npz":"787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b",
"d6_json":"4607edde17c6820c85f32c0bbd774d5a58148eb01bfd0c81ce592e8c1b907791",
"d6_npz":"17b50c6ee584b2a8886f7114a90ea9396a127172dd9e02976b0e6275fe2fedc0",
"d7_json":"031229d570d29ae9c4ea0ab8e25222d94e9cda4520c991cd203e9d7b97e01dc9",
"d7_npz":"4f011c96c2c11165df6332eafc459c5d2c5e7bc5164a436bde3d1563696f0e13",
"trace":"608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8"}
FN=("N","L","R","b","u","phi","T","rho")
ORIG={"N":"N20","L":"S20","R":"S20","u":"u20","phi":"phi20","T":"T20","rho":"delta_varrho20"}
NX=128
RTOL=1e-12
TINY=1e-300

def digest(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):h.update(chunk)
    return h.hexdigest()

def locks():
    pre=json.loads((ROOT/"ge19/h4f3d10_predata_actual_nonbath_first_order_known_boundary.json").read_text())
    if pre["archive_only_fft_comparison_relative_tolerance"]!=RTOL:raise RuntimeError("prereg archive rtol")
    observed={}
    for path,sha in PIN.items():
        head=subprocess.check_output(["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True).strip()
        work=subprocess.check_output(["git","hash-object",str(ROOT/path)],cwd=ROOT,text=True).strip()
        observed[path]={"expected":sha,"head":head,"worktree":work,"exact":sha==head==work}
    if not all(v["exact"] for v in observed.values()):raise RuntimeError("immutable code/predata blob mismatch")
    s.code_lock()
    return observed

def physical_paths(rd,trace):
    filenames={
    "source_json":"ge19_h4f3b_actual_corrected_six_piece_source.json",
    "source_npz":"ge19_h4f3b_actual_corrected_six_piece_source.npz",
    "d6_json":"ge19_h4f3d6_actual_normalized_bath_parent_ward.json",
    "d6_npz":"ge19_h4f3d6_actual_normalized_bath_parent_ward.npz",
    "d7_json":"ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode.json",
    "d7_npz":"ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode.npz"}
    paths={k:rd/v for k,v in filenames.items()}
    paths["trace"]=trace
    for key,path in paths.items():
        if not path.is_file() or digest(path)!=SHA[key]:raise RuntimeError("physical input SHA: "+str(path))
    if trace.stat().st_size!=26643162:raise RuntimeError("R1 original length changed")
    expected={"source_json":"GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN",
              "d6_json":"GE19_H4F3D6_ACTUAL_BATH_PARENT_WARD_SUBSET_PASS_FULL_OPEN",
              "d7_json":"GE19_H4F3D7_FD4_INTERVAL_ODE_DISCREPANCY_DECOMPOSED"}
    for key,classification in expected.items():
        if json.loads(paths[key].read_text())["classification"]!=classification:
            raise RuntimeError("frozen actual science classification changed: "+key)
    d7=json.loads(paths["d7_json"].read_text())
    if not d7["all_diagnostic_gates_pass"] or len(d7["cases"])!=6:
        raise RuntimeError("original physical D7r1 diagnostic gate not PASS")
    return paths
