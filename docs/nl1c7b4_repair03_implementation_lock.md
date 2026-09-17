# NL1C7B4 Repair03 implementation lock

Status: **LOCKED BEFORE OFFICIAL REPAIR03 RUN**

- Repair03 pre-data commit: `6d0ac30a1e2b16ed5b3c896c1a6411402ee5517e`.
- Repair03 implementation commit: `3b6f19752792b4e04ea8c5ef4e6edef712d2f139`.
- Repair03 implementation blob: `3c60d384de2a55b7b9f02ef48ec3eca1ce43be2f`.
- Reporting-adapter commit: `561241a18cb7eea8ef7b842da665dd60789cf4b0`.
- Reporting-adapter blob: `f30a88a1cb04fda1c9126e8700287d72654f193f`.

The adapter sets the already frozen C7A value `h=0.6733246390848661` only under the name `H_SMALL_H` used to report `x=r/(R_sigma/h)`. It does not enter any reconstructed field, action term, radial derivative, constraint residual, normalization, amplitude-scaling diagnostic, or classification gate.

Frozen parent Repair02:

- run `35216284867`;
- head `2791ba272e8a587bfe2ead747b54596631527627`;
- artifact `10495377062`;
- artifact digest `sha256:f74795d3c57ba6f307655b1ec15513b57babc7eadbe0c81c4f62bf1949643d49`;
- result freeze commit `9c1f5c6a17467467bcf82e134f21793a3f63d0d4`.

No code, threshold, source, state mapping, amplitude ladder, branch, scale, radial grid, or localization rule may be changed after this lock for the official Repair03 run.
