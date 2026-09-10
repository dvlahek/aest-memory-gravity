# C3-only forensic audit — CLASS versus offline eta=0 tangent bridge

## Status and scope

This diagnostic is preregistered after the completed D2C6C-R3 run `34467829168` on implementation commit `d984b160cb2c9c7846a1a9e6d252a583829b1436` and before any C3-forensic output is generated.

The historical D2C6C-R3 result remains unchanged:

`CLASSIFICATION=NL1C6D2C6C_ETA0_NONLINEAR_MEMORY_TANGENT_FAIL`

with C1, C2 and C4--C8 passing and only C3 failing. The R3 modewise full-prehistory repair left the C3 relative-L2 mismatch essentially unchanged at approximately 8.8% in alpha/chi and 8.7% in E. Therefore this stage does not rerun the 27-member nonlinear family. It is a linear forensic diagnostic only.

This audit cannot license finite positive physical eta and cannot alter, reinterpret, or relax any D2C6C gate.

## Frozen inputs

The audit uses exactly the same corrected CLASS target and eta=0 tangent reference convention as D2C6C-R3:

- CLASS v3.3.4 SHA `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- physical `eta=0`;
- tau-H0 = 1;
- bath order 39;
- central signed-lambda CLASS variational reference with lambda = +/-10, where signed lambda is not physical eta;
- the accepted source-grid forcing trace used by D2C6C;
- the same six frozen k modes and nine checkpoints z = 6,5,4,3,2,1.5,1,0.5,0.2;
- the same offline stable-canonical eta0 tangent equations and D2C6C-R3 modewise full prehistory;
- offline linear-control discretization Nx=128, Nstep=4096.

No nonlinear completion member, likelihood, parameter fit, finite eta, or observational selection is introduced.

## Diagnostics frozen before output

For each field X in {alpha,E,chi}, each of the six frozen modes, and each of the nine frozen checkpoints, recover the offline modal coefficient from the real-space tangent field by least-squares projection onto the exact six-mode synthesis matrix used by D2C6C. Compare it with the corresponding corrected CLASS tangent coefficient.

The audit reports:

1. `CHECKPOINT` aggregate relative-L2 error across the six modes for alpha, E and chi at every checkpoint.
2. `MODE` diagnostics for every mode and field: the z=6 relative point error, the full-nine-checkpoint relative-L2 error, the best multiplicative scale

   `s = <offline,CLASS>/<CLASS,CLASS>`

   and the residual after removing that scale

   `r_scaled = ||offline-s CLASS||/||CLASS||`.
3. Per-field scale median, scale spread (max-min across six modes), maximum scaled residual, z=6 aggregate error, and z=0.2 aggregate error.
4. A reconstruction audit verifying that projection of a synthetically generated six-mode field recovers its modal coefficients to relative L2 <= 1e-12. Failure of this audit makes the forensic result `INCOMPLETE` rather than physical evidence.

Pointwise ratios are reported only when the CLASS denominator exceeds `1e-12` times the maximum absolute CLASS coefficient for that same mode/field trajectory; otherwise the ratio is reported as non-finite/omitted and is not used for interpretation.

## Predeclared interpretation flags

These are diagnostic flags, not D2C6C gates.

- `EARLY_OFFSET=True` for a field if its aggregate six-mode relative-L2 error is already > 0.03 at z=6.
- `POST_Z6_GROWTH=True` for a field if its z=6 aggregate error is <= 0.01 and its z=0.2 aggregate error is > 0.03.
- `MULTIPLICATIVE_COMPATIBLE=True` for a field if the maximum six-mode scaled residual is <= 5e-3 and the six-mode scale spread is <= 1e-2.
- `COMMON_SCALE_COMPATIBLE=True` if all three fields are multiplicative-compatible and the medians of their six-mode scales span <= 1e-2.

The audit must report all flags even if none are true. No threshold may be changed after output is seen.

## Interpretation limits

A common multiplicative pattern would identify a normalization/convention mismatch to be derived and audited separately before any repair. An early offset without multiplicative compatibility would instead point to initial-condition or unobserved early-time bridge structure. A small z=6 error followed by growth would point to a post-z=6 evolution/source mismatch.

None of these outcomes retroactively converts D2C6C-R3 into a PASS. Any subsequent repair requires a separate pre-data declaration that specifies the derived cause and changes only the demonstrated faulty bridge.