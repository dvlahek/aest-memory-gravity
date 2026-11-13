#!/usr/bin/env python3
"""Repair exactly the GE19 v1 callback header-order compile bug in an isolated CLASS.

This is a single-source, fail-closed correction after the first researcher WSL
prepare succeeded in patching but failed building three aest_memory accessors.
It moves the already-existing aest_memory.h include ahead of the GE19 callback.
No physics equations, oscillator coefficients, v019j sources, or original backup
are modified. The manifest's source checksum is updated ONLY for this exact fix.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

OLD_WRITTEN_SHA256 = "856ba9feeda5a6c7de9d13441755303ade38b685138091b2bca533630112b0b3"
ORIGINAL_V019J_SHA256 = "2b4d7be96b6ebf4149bef129e357a32571f69cfffb3be0b1792d578e82ad6e17"
CLASS_HEAD = "e85808324f51fc694d12e3ed7439552a3c3f9540"
CLASS_BLOB = "c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0"
SOURCE_MARKER = "/* GE19 FULL CLASS DIRECT TANGENT EXPERIMENT v1 */"
HEADER = '#include "aest_memory.h"\n'
PIVOT = '#include "parallel.h"\n'


def sha(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def git(root: Path, argument: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", argument], text=True
    ).strip()


def validate(root: Path):
    src = root / "source" / "perturbations.c"
    manifest_path = root / "ge19_tangent_patch_manifest.json"
    base_backup = root / "source" / "perturbations.c.ge19_original_backup"
    if not (src.is_file() and manifest_path.is_file() and base_backup.is_file()):
        raise RuntimeError("GE19_HEADER_REPAIR_PREREQUISITE_MISSING")
    if git(root, "HEAD") != CLASS_HEAD or git(root, "HEAD:source/perturbations.c") != CLASS_BLOB:
        raise RuntimeError("GE19_HEADER_REPAIR_PARENT_CLASS_CHANGED")
    data = json.loads(manifest_path.read_text())
    if (data.get("parent_source_sha256") != ORIGINAL_V019J_SHA256
        or data.get("original_CLASS_HEAD") != CLASS_HEAD
        or data.get("original_CLASS_git_blob") != CLASS_BLOB):
        raise RuntimeError("GE19_HEADER_REPAIR_MANIFEST_PARENT_CHANGED")
    if sha(base_backup.read_bytes()) != ORIGINAL_V019J_SHA256:
        raise RuntimeError("GE19_HEADER_REPAIR_ORIGINAL_BACKUP_CHANGED")
    raw = src.read_bytes()
    current_sha = sha(raw)
    if current_sha != data.get("modified_source_sha256"):
        raise RuntimeError("GE19_HEADER_REPAIR_SOURCE_MANIFEST_MISMATCH "+current_sha)
    text = raw.decode("utf-8")
    if (text.count(SOURCE_MARKER) != 1 or text.count(PIVOT) != 1
        or text.count(HEADER) != 1
        or text.count("aest_memory_active_count(") < 1
        or text.count("aest_memory_node_order(") < 1
        or text.count("aest_memory_weight_order(") < 1):
        raise RuntimeError("GE19_HEADER_REPAIR_SOURCE_STRUCTURE_MISMATCH")
    return src, manifest_path, data, raw, current_sha, text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--class-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.class_root.expanduser().resolve()
    src, manifest_path, data, original, current, text = validate(root)
    pivot_index = text.index(PIVOT)
    header_index = text.index(HEADER)
    callback_index = text.index(SOURCE_MARKER)
    if pivot_index < header_index < callback_index:
        print("GE19_TANGENT_AEST_HEADER_ORDER_PASS", current, flush=True)
        print("GE19_HEADER_REPAIR_NO_CHANGE", flush=True)
        return
    if current != OLD_WRITTEN_SHA256 or not (pivot_index < callback_index < header_index):
        raise RuntimeError("GE19_HEADER_REPAIR_UNEXPECTED_PATCHED_SOURCE "+current)
    # Only move an existing guarded C/C++ header (whose declarations have
    # correct extern-C linkage) before the callback definition.
    repaired = text.replace(HEADER, "", 1).replace(PIVOT, PIVOT+HEADER, 1)
    if (repaired.count(HEADER) != 1 or
        repaired.index(HEADER) > repaired.index(SOURCE_MARKER)):
        raise RuntimeError("GE19_HEADER_REPAIR_RESULT_STRUCTURE_INVALID")
    new_raw = repaired.encode("utf-8")
    new_sha = sha(new_raw)
    snap = src.with_name(src.name + ".ge19_before_header_fix_20261113")
    if snap.exists():
        raise RuntimeError("GE19_HEADER_REPAIR_SNAPSHOT_ALREADY_EXISTS")
    snap.write_bytes(original)
    staging = src.with_name(src.name + ".ge19_header_fix_staging")
    if staging.exists():
        raise RuntimeError("GE19_HEADER_REPAIR_STAGING_EXISTS")
    staging.write_bytes(new_raw)
    if sha(staging.read_bytes()) != new_sha:
        raise RuntimeError("GE19_HEADER_REPAIR_STAGE_HASH_MISMATCH")
    os.replace(staging, src)
    data["modified_source_sha256"] = new_sha
    data["header_declaration_order_repaired"] = True
    data["header_repair_before_sha256"] = current
    data["header_repair_backup"] = str(snap)
    data["full_class_compiled"] = False
    data["source_convergence_qualified"] = False
    data["production_physics_go"] = False
    temp_manifest = manifest_path.with_name(manifest_path.name + ".ge19_header_staging")
    if temp_manifest.exists():
        raise RuntimeError("GE19_HEADER_REPAIR_MANIFEST_STAGE_EXISTS")
    temp_manifest.write_text(json.dumps(data, indent=2, sort_keys=True)+"\n")
    os.replace(temp_manifest, manifest_path)
    if sha(src.read_bytes()) != new_sha:
        raise RuntimeError("GE19_HEADER_REPAIR_POSTWRITE_HASH_MISMATCH")
    print("GE19_TANGENT_AEST_HEADER_ORDER_REPAIR_PASS", current, new_sha, flush=True)
    print("GE19_FULL_CLASS_C_BUILD_NOT_YET_VERIFIED", flush=True)


if __name__ == "__main__":
    main()
