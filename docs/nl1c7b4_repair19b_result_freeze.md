# NL1C7B4 Repair19b — local result freeze

## Status

Frozen local WSL result from the first locked Repair19b execution.

Terminal classification:

`NL1C7B4_REPAIR19B_IMPLEMENTATION_FAIL`

with

`SCIENCE_RC=2`.

Execution HEAD:

`a711bc54702cdba259672b5aa024af8fd48db9e5`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `33646`
  - SHA-256:
    `d177394b45e19ac2bca739d4ff256694c5df65e9331276e3c1b1466f4fbe5929`
- evaluator log:
  - bytes: `34092`
  - SHA-256:
    `686fc3a0a3f09ee3d98b4cf1528224d3aaf935018de6cddc163245e65e3b7721`
- local runner log:
  - bytes: `38093`
  - SHA-256:
    `b9a14ecb011467e0de46c622f89d5eb21e7875cfdd5142fa6d22b7537d31d83c`.

## Gate result

PASS:

- R19B_G1 exact frozen provenance
- R19B_G2 exact frozen subspace/basis reproduction
- R19B_G3 exact parent/Jacobian input reproduction
- R19B_G8 exact gauge satisfaction
- R19B_G9 LSMR-stagnation ratio test
- R19B_G10 claim boundary.

FAIL:

- R19B_G4 all direct solves full reduced-column rank
- R19B_G5 both-basis GELSD feasibility
- R19B_G6 chain-vs-orth physical correction agreement
- R19B_G7 GELSD-vs-GELSY physical correction agreement.

The frozen terminal class remains IMPLEMENTATION_FAIL and must not be relabelled.

## Basis reproduction

The Repair19a basis diagnostics reproduce exactly.

Chain basis condition numbers:

- Nr=256: `162.33598862000716`
- Nr=512: `325.3116790240505`.

Orthonormal Helmert basis:

- condition number `1.0` at both grids;
- gauge residual and orthonormality errors at approximately `1e-15`.

## Direct orthonormal-basis feasibility payload

The orthonormal basis is the predeclared coordinate-conditioning control from Repair19a/Repair19b.

For the primary GELSD solve, relative linear residuals are:

- scale 5, Nr=256:
  `4.196346283532464e-12`
- scale 5, Nr=512:
  `3.48273712439107e-08`
- scale 10, Nr=256:
  `1.0389389472679538e-10`
- scale 10, Nr=512:
  `1.1984362607786484e-07`
- scale 20, Nr=256:
  `5.5409575977125e-11`
- scale 20, Nr=512:
  `2.0056795697491796e-11`.

All six are below the unchanged Repair19a linear-feasibility threshold

`1e-6`.

For the independent GELSY solve, all six orthonormal-basis residuals are also below `1e-6`.

Thus the frozen payload contains direct linear feasibility in the orthonormal representation for every canonical scale/grid case.

## LSMR stagnation payload

For the orthonormal basis, the frozen Repair19a LSMR residual divided by the Repair19b GELSD residual is enormous in every case.

Examples:

- scale 5, Nr=256:
  `9.296730686198724e10`
- scale 10, Nr=256:
  `4.9253113162973175e9`
- scale 20, Nr=512:
  `2.7282445466862537e10`.

The minimum LSMR/GELSD ratio across all chain/orth cases is still

`45026.80417446184`.

Therefore the result strongly supports the numerical-stagnation interpretation of the Repair19a iterative LSMR solve.

## Exact gauge preservation

All direct orthonormal-basis corrections satisfy:

- Y4 residual at roundoff level;
- Qmean residual approximately `1e-20` or smaller.

Thus direct linear feasibility does not come from relaxing the certified Y4/Qmean conditions.

## Numerical-rank sensitivity

The original R19b implementation required every direct solve in both coordinate bases and both LAPACK drivers to report full reduced-column rank.

That gate is not basis invariant.

Examples:

### Scale 5, Nr=256

Chain/GELSD:

- rank `505/508`
- relative residual `4.734664009473492e-7`.

Orth/GELSD:

- rank `508/508`
- relative residual `4.196346283532464e-12`.

### Scale 10, Nr=256

Chain/GELSD:

- rank `504/508`
- relative residual `9.446088660375044e-6`.

Orth/GELSD:

- rank `508/508`
- relative residual `1.0389389472679538e-10`.

### Nr=512 orthonormal cases

At scale 5 and scale 10, GELSD reports `1019/1020`, while GELSY reports `1020/1020`.

At scale 20 both return full rank.

Thus the numerical rank decision changes with coordinate representation and LAPACK driver near the frozen relative singular-value cutoff.

## Physical-correction disagreement

Because different rank decisions retain/drop weak directions, the physical correction vectors are not stable under the original R19b `1e-8` vector-agreement gate.

This is most severe in the chain basis.

The orth basis is substantially more stable at Nr=256, but at Nr=512 scale 5 and 10 GELSD/GELSY still differ because one driver truncates one weak singular direction and the other retains it.

This correction-vector ambiguity does not remove the observed residual-space feasibility.

## Interpretation

Repair19b does not pass its preregistered implementation gates.

However its frozen payload establishes a narrower and important fact:

1. the orthonormal Y4=0/Qmean=0 reduced system is directly linearly feasible in all six canonical cases under both GELSD and GELSY at the unchanged `1e-6` residual threshold;
2. the frozen LSMR solutions were many orders of magnitude less converged;
3. chain-basis and cross-driver numerical-rank decisions are not invariant near the weak singular directions;
4. therefore full-rank and physical-vector-agreement gates are too strong for diagnosing residual-space feasibility of this near-singular reduced operator.

This does not yet certify nonlinear closure.

## Licensed continuation

A separately preregistered Repair19b1 may make the scientific question narrower and coordinate-stable:

- reproduce the frozen Repair19b payload exactly;
- treat the orthonormal basis as the predeclared conditioning-stable representation;
- require both GELSD and GELSY orthonormal residuals to satisfy the unchanged `1e-6` feasibility threshold in all six cases;
- require exact Y4/Qmean satisfaction;
- require the frozen LSMR/direct residual improvement to exceed the preregistered stagnation factor;
- report numerical-rank variation descriptively rather than requiring full rank;
- keep the chain basis as a conditioning control only.

Repair19b itself remains IMPLEMENTATION_FAIL.
