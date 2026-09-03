#!/usr/bin/env python3
from pathlib import Path
import argparse
OLD_SOURCE='SOURCE = input.o background.o thermodynamics.o perturbations.opp primordial.opp fourier.o transfer.opp harmonic.opp lensing.opp distortions.o'
NEW_SOURCE='SOURCE = input.o background.o thermodynamics.o aest_memory.o perturbations.opp primordial.opp fourier.o transfer.opp harmonic.opp lensing.opp distortions.o'
ap=argparse.ArgumentParser()
ap.add_argument("class_root")
args=ap.parse_args()
root=Path(args.class_root)
make=root/"Makefile"
text=make.read_text()
if NEW_SOURCE in text:
    make.write_text(text.replace(NEW_SOURCE,OLD_SOURCE,1))
for p in [root/"include"/"aest_memory.h",root/"source"/"aest_memory.c"]:
    if p.exists(): p.unlink()
print("v0.18 patch removed")
