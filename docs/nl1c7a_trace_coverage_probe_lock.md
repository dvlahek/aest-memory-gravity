# NL1C7A A4 native trace coverage probe — implementation lock

Status: **LOCKED BEFORE OFFICIAL EXTENDED CLASS TRACE RUN**

- C7A preregistration commit: `5399a2ca73165e8f97cea45934e50baf8ffb3629`
- trace extension blob: `b25b6087cb1e9fd6a275ffcf0843c880d009efce`
- coverage probe path: `nl1c7a/trace_coverage_probe.py`
- coverage probe blob SHA: `5be7163070a7fa2709e3ac6cb5835206c8feb5ec`
- coverage probe implementation commit: `6e532fdadca252f182765dcbeccca22fb86d5d35`

Frozen trace grid: 128 logarithmic requested modes over `[0.0015,1.2] h Mpc^-1`, exact eta=0/memory-off Exp model and `a_i=0.02`.

A4 requires relative k miss `<=1e-12`, common native source times across all requested modes at relative mismatch `<=1e-12`, at least three native times below and three above `a_i` within `0.015<=a<=0.03`, and finite required trace fields.

This checkpoint performs no interpolation and no radial/spherical reconstruction.
