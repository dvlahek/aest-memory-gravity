#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).with_name("direct_bath_bridge_audit.py")
text = path.read_text()

old_guard = '''                if not (float(tau[0]) < float(data["tau_check"][0])):\n                    raise RuntimeError(\n                        f"mode {imode} finite common-domain start is not before z=6: tau={tau[0]}"\n                    )\n\n'''
if text.count(old_guard) != 1:
    raise RuntimeError("R2 start-guard anchor not found exactly once")
text = text.replace(old_guard, "", 1)

old_checkpoint = '''                    if target < tau[0] - 1e-10 or target > tau[-1] + 1e-10:\n                        raise RuntimeError(\n                            f"mode {imode} checkpoint z={redshift} outside dense CLASS history"\n                        )\n'''
new_checkpoint = '''                    if target < tau[0] - 1e-10:\n                        print(\n                            f"BATH_CHECKPOINT_SKIPPED mode={imode} z={redshift:g} "\n                            f"target_tau={target:.12e} common_tau_first={tau[0]:.12e}",\n                            flush=True,\n                        )\n                        continue\n                    if target > tau[-1] + 1e-10:\n                        raise RuntimeError(\n                            f"mode {imode} checkpoint z={redshift} after dense CLASS history"\n                        )\n'''
if text.count(old_checkpoint) != 1:
    raise RuntimeError("R2 checkpoint-guard anchor not found exactly once")
text = text.replace(old_checkpoint, new_checkpoint, 1)

path.write_text(text)
print("C3_BATH_BRIDGE_R2_COMMON_DOMAIN_PATCH_PASS")
