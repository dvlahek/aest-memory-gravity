# NL1C7B3 implementation lock — standard background sector identification

Status: **FROZEN BEFORE B3 WORKFLOW EXECUTION**

Predata commit:

`e36570cce4e8f5057af5d0abe01b4f66e90fcf92`

Implementation commit:

`eae3ca58239a07c306d00db2c157f770fd8fe9e9`

Frozen implementation:

- path: `nl1c7b/standard_background_sector_identification.py`
- blob: `565c3cbf598c2978ee2b263ffdce354e085c43c7`

Frozen parent:

- NL1C7B2 Repair01 run `35193003807`
- artifact `10484278813`
- artifact SHA256 `76f24778c432b018724c90cdbb3c6a586dd37698fa9ae4eb644cf8acd0b99059`
- science classification `NL1C7B2_REPAIR01_HOMOGENEOUS_BACKGROUND_SECTOR_INCOMPLETE`

Frozen B3 rules:

- pinned CLASS `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- exact `v063/theory_response_map.py::class_params()` physical model;
- eta=0 and memory disabled;
- evaluate `Class.get_background()` at `a_i=0.02`;
- primary standard sum only: photons + ultra-relativistic species + the single ncdm species + Lambda when source-declared;
- baryons and the CLASS cdm slot excluded from this sum because B1 and AeST already represent them;
- no fitted remainder and no additional radial source;
- parent reproduction limit `1e-8`;
- homogeneous closure limit `1e-7`;
- PCHIP-vs-linear control limit `2e-2`.

No radial initial constraint, nonlinear trajectory, or finite-eta calculation is licensed by this lock.
