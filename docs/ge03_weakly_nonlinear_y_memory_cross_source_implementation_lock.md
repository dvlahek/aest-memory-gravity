# GE03 weakly nonlinear Y-memory cross-source — implementation lock

## Status

Implementation locked before first GE03 execution.

GE03 is the N1 stage of the physics-first nonlinear programme.

It does not solve the full second-order state `Z21`, does not introduce finite eta and does not reopen B4-B8.

## Theory provenance

Dependencies:

- `NL0C_Y_SECTOR_WEAKLY_NONLINEAR_PASS`;
- `NL1A_PSEUDOSPECTRAL_OPERATOR_BRIDGE_PASS`;
- `NL1B2_DIRECTIONAL_SECOND_ORDER_ETA_TANGENT_PASS`;
- `V077_NATIVE_STATE_TANGENT_AFFINITY_PASS`.

The target operator is the exact NL1B2 directional derivative

`DY2[chi10;chi11]`.

For

`g=grad_phys chi10`

and

`h=grad_phys chi11`,

the normalized beta-dependent operator is

`DO_beta=(1/(1+beta0)) div_phys[ |g|h + (g.h/|g|)g ]`

with the bracket set continuously to zero where `|g|=0`.

The common physical prefactor

`2(2-KB)/a0`

is factored out of the numerical conditioning tests exactly as in NL1A.

## Frozen retained artifact

Workflow run:

`34315590099`.

Artifact ID:

`10090367181`.

Artifact digest:

`sha256:24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378`.

Required traces:

- `v076_v077_base_trace.dat`;
- plus/minus traces for
  `lambda={10,5,2.5,1.25}`.

## Preregistration

Commit:

`bceff2b86dd5f94cfe50ca722d4601400fc4ee49`.

File:

`ge03/predata_weakly_nonlinear_y_memory_cross_source.json`.

Frozen blob:

`9b5a21aa77f4e8bcacb0e41cc9f0d83285a62395`.

## Implementation

Commit:

`21664244deff23a7a05980aabcc95072aa42aaf9`.

File:

`ge03/weakly_nonlinear_y_memory_cross_source.py`.

Frozen blob:

`c80a76a190d749b0a2c57d35449ed01ad2205a03`.

## Frozen reconstruction

Signal-band modes:

`k_h={0.03,0.05,0.08,0.10,0.15,0.20} h/Mpc`.

Exact integer periodic-box modes:

`{3,5,8,10,15,20}`.

Frozen phases:

`{0.13,0.71,1.29,2.03,2.77,3.41}`.

Native evaluation window:

`0.2<=z<=1.5`.

The baseline direction is the retained memory-off `chi10`.

For every lambda,

`chi11_lambda=[chi(+lambda)-chi(-lambda)]/(2 lambda)`.

The primary `chi11` is the four-lambda mean after the affinity gate.

## Frozen numerical controls

Co-primary:

`beta0={1,0.5,0.1}`.

Spatial resolutions:

`Nx={256,512}`.

Derivatives:

FFT pseudospectral.

Nonlinear flux:

2/3 dealiasing.

Finite-difference directional steps:

- primary relative direction step `1e-4`;
- control relative direction step `3e-5`.

The actual perturbation is scaled as

`delta_chi = h ||chi10||/||chi11|| chi11`.

## Frozen gates

- exact retained artifact provenance;
- all requested k matches <= `1e-12`;
- common native grid mismatch <= `1e-12`;
- at least eight native evaluation times;
- four-lambda chi11 relative-L2 affinity <= `5e-3`;
- four-lambda chi11 cosine >= `0.9999`;
- analytic versus finite-difference DY2 relative L2 <= `1e-4`;
- primary versus control finite-difference DY2 relative L2 <= `1e-4`;
- Nx256 versus Nx512 low-mode DY2 relative L2 <= `5e-4`;
- beta0 scaling relative error <= `1e-12`;
- all outputs finite.

No sign/cosine/amplitude of the physical cross-source is a PASS gate.

Those quantities are descriptive physics outputs.

## Classification

Full control:

`GE03_WEAKLY_NONLINEAR_Y_MEMORY_CROSS_SOURCE_PASS`.

Otherwise:

`GE03_WEAKLY_NONLINEAR_Y_MEMORY_CROSS_SOURCE_FAIL`.

## Claim boundary

A PASS certifies the weakly nonlinear Y-memory cross-source entering the exact eta=0 second-order hierarchy.

It does not:

- solve `Z21`;
- introduce finite eta;
- simulate collapse;
- establish a halo or lensing prediction;
- constitute observational evidence.

## Anti-tuning

After this lock do not change:

- lambda set;
- signal-band modes;
- phases;
- native window;
- beta0 set;
- spatial resolutions;
- finite-difference steps;
- dealiasing rule;
- numerical gates.
