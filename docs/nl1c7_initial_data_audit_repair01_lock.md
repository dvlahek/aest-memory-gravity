# NL1C7 initial-data closure audit — Repair01 implementation lock

Status: **LOCKED BEFORE RE-RUN**

Repair01 preregistration commit: `47af6894bfbe2a863165570bf23dea006f0ddc8d`.

Historical technical-failure workflow: `35091142502`.

Frozen repaired implementation:

- path: `nl1c7/initial_data_closure_audit.py`
- blob SHA: `0040ed81ac2e4adb197612a5b37e9bd4de6dea6a`
- implementation commit: `044a9d162674ed9eb44063ca30ac8f4f29e39aaa`

Only the symbolic rank algorithm changed. The repaired code uses the exact G11 determinant identity and the frozen positive global kinetic margin to certify generic rank 4, plus an independent homogeneous-background determinant check. All physical equations, variable counts, classifications, and science gates are unchanged.
