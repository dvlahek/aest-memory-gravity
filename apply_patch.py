#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, json

TARGET_VERSION="v3.3.4"
TARGET_SHA="e85808324f51fc694d12e3ed7439552a3c3f9540"
OLD_SOURCE="SOURCE = input.o background.o thermodynamics.o perturbations.opp primordial.opp fourier.o transfer.opp harmonic.opp lensing.opp distortions.o"
NEW_SOURCE="SOURCE = input.o background.o thermodynamics.o aest_memory.o perturbations.opp primordial.opp fourier.o transfer.opp harmonic.opp lensing.opp distortions.o"

ap=argparse.ArgumentParser()
ap.add_argument("class_root")
ap.add_argument("--force",action="store_true")
args=ap.parse_args()

here=Path(__file__).resolve().parent
root=Path(args.class_root).resolve()
common=root/"include"/"common.h"
make=root/"Makefile"

if not common.exists() or not make.exists():
    raise SystemExit("Not a CLASS source root: "+str(root))

common_text=common.read_text(errors="replace")
if ('#define _VERSION_ "'+TARGET_VERSION+'"') not in common_text and not args.force:
    raise SystemExit("CLASS version mismatch; expected "+TARGET_VERSION)

mtext=make.read_text()
if "aest_memory.o" not in mtext:
    if OLD_SOURCE not in mtext:
        raise SystemExit("Pinned Makefile SOURCE line not found. Refusing fuzzy patch.")
    make.write_text(mtext.replace(OLD_SOURCE,NEW_SOURCE,1))

shutil.copy2(here/"patch"/"include"/"aest_memory.h",root/"include"/"aest_memory.h")
shutil.copy2(here/"patch"/"source"/"aest_memory.c",root/"source"/"aest_memory.c")

report={
  "target_version":TARGET_VERSION,
  "target_sha":TARGET_SHA,
  "class_root":str(root),
  "makefile_patched":True,
  "header_installed":True,
  "source_installed":True,
  "physics_path_modified":False
}
(here/"results").mkdir(exist_ok=True)
(here/"results"/"apply_patch_report.json").write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
