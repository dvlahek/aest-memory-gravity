# NL1C7B3 Repair01 implementation lock

Status: **LOCKED BEFORE OFFICIAL RUN**

- predata commit: `58a5dc4d22fe83d8b2eadae35a313050e6c7df43`
- historical B3 result freeze: `4fb8679f84585c4008008d7043ac0b5f4ca33eeb`
- implementation commit: `4e50a12c062f96dcc79eeb0f496fe922b551eee7`
- implementation path: `nl1c7b/standard_background_sector_identification_repair01.py`
- implementation blob: `b3cdba7e314d2b5285b51770fb20e17cf68b181c`

Only the numerical background-point representation is changed relative to historical B3. The frozen physical species sum, eta=0 model, pinned CLASS commit, C6 normalization, and `1e-7` homogeneous closure limit are unchanged.

`rho_tot` is treated only as an aggregate diagnostic, never as an independent species.
