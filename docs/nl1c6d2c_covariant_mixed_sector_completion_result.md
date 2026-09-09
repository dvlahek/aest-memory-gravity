# NL1C6D2C covariant mixed-sector completion result

Final classification:

```text
NL1C6D2C_COVARIANT_MIXED_SECTOR_COMPLETION_FAIL
```

This result is a theory/action-level FAIL under the preregistered conjunctive D2C gates. It is **not** a numerical solver failure and it is **not** a physical exclusion of AeST. The failure is an exact factor-of-two normalization inconsistency between the frozen Exp FLRW background implementation and the frozen D1A/R3 `K2` weak-field normalization.

No nonlinear branch trajectory was run. No member of the 27-member completion family was selected or retuned.

## 1. Provenance

Entering locked state:

- branch: `v053-model-freeze-planck`
- identity-audit implementation HEAD: `9bf761ce372bd77d7550bf01722716c2e13d7d6a`
- identity-audit result record: `215e6d89202d30df73f209e50b1f04df92926d9b`
- D2C family predata: `77d47673ca7d42d8615a7dc2b4bec709d4ebdefd`
- D2C identity-audit details predata: `01908269027c0a6e7db7ba2ea5de41120cfed45d`

The earlier

```text
NL1C6D2C_COMPLETION_IDENTITY_AUDIT_PASS
```

remains valid in its stated restricted scope: homogeneous-slice identity, coefficient-level linear invisibility of the mixed control, tracking-slice identity, deep-MOND subleading behavior, and high-gradient control bound. It explicitly did not classify full D2C.

## 2. Frozen D1A/R3 normalization

The D1A/R3 weak-field sector uses the published late-time quadratic normalization

\[
K(Q)=K_2(Q-Q_0)^2+\cdots,
\]

or equivalently, since

\[
F(0,Q)=-2K(Q),
\]

\[
F(0,Q)=-2K_2(Q-Q_0)^2+\cdots.
\]

Therefore

\[
K_{QQ}(Q_0)=2K_2,
\qquad
F_{QQ}(0,Q_0)=-4K_2.
\]

This is the normalization behind the already certified D1A canonical relation

\[
P_\chi=4K_2 U,
\qquad
U=\dot\chi-Q_0E,
\]

and the frozen static mass

\[
\mu^2_{\rm D1/R3}=\frac{2K_2Q_0^2}{2-K_B}.
\]

For the frozen parameters,

```text
K2 = 9500
Q0 = 1e-4 Mpc^-1
K_B = 0.0665
mu^2_D1_R3 = 9.826739074217741e-05 Mpc^-2
```

## 3. Frozen Exp FLRW implementation

The frozen CLASS bridge implements the Exp background as

\[
K_{\rm Exp}(Q)=2K_2Z_0^2\left(e^{Z^2}-1\right),
\qquad
Z=\frac{Q-Q_0}{Z_0},
\]

with the same numerical input `K2=9500`.

The D2C predata retained this expression exactly in order not to alter the frozen cosmological model after results.

Expanding around `Q=Q0`,

\[
e^{Z^2}-1=Z^2+O(Z^4),
\]

hence

\[
K_{\rm Exp}(Q)
=2K_2(Q-Q_0)^2+O((Q-Q_0)^4/Z_0^2).
\]

Thus

\[
K_{{\rm Exp},QQ}(Q_0)=4K_2,
\qquad
F_{{\rm Exp},QQ}(0,Q_0)=-8K_2.
\]

The corresponding Minkowski/zero-expansion kinetic coefficient would be

\[
P_\chi^{\rm Exp}=8K_2U,
\]

not the frozen D1A value `4 K2 U`.

Likewise the mass scale implied by this curvature is

\[
\mu^2_{\rm Exp}=\frac{4K_2Q_0^2}{2-K_B}
=1.9653478148435482\times10^{-4}\ {\rm Mpc}^{-2},
\]

which is exactly twice the frozen D1/R3 value.

Therefore the normalized coefficient discrepancy is

```text
abs(2*K2 - K2)/K2 = 1.0
```

and the mass-squared discrepancy is

```text
abs(mu2_Exp - mu2_D1_R3)/mu2_D1_R3 = 1.0
```

against the preregistered D2C inherited zero-expansion/static gates of `1e-12`.

This is an exact algebraic contradiction, not a finite-difference or integration error.

## 4. Published-theory cross-check

The normalization issue is visible in the literature itself.

Skordis & Zlosnik (2021) first define the generic cosmological expansion as

\[
K=-2\Lambda+K_2(Q-Q_0)^2+\cdots,
\]

and their late-time Minkowski action uses

\[
\frac{\partial^2F}{\partial Q^2}\to-4K_2,
\]

which agrees with D1A/R3.

The same paper later displays the example Exp function with the prefactor

\[
2K_2Z_0^2(e^{Z^2}-1),
\]

which has twice that quadratic curvature.

Skordis & Zlosnik (2022), in the dedicated Minkowski stability analysis, again define

\[
K=K_2(Q-Q_0)^2+\cdots
\]

and

\[
F=(2-K_B)\lambda_sY-2K_2(Q-Q_0)^2+\cdots,
\]

confirming the D1A normalization.

Mistele, McGaugh & Hossenfelder (2023) write instead

\[
K_{\rm exp}=K_2Z_0^2(e^{Z^2}-1),
\qquad
K_{\rm cosh}=2K_2Z_0^2(\cosh Z-1),
\]

and state that both reduce to the same quadratic `K(Q)` for small `Z`. This later convention is algebraically consistent with `K=K2(Q-Q0)^2`.

The present result does not attempt to adjudicate the publication-history origin of the factor. It records only the exact consequence for the repository's frozen implementation.

## 5. Why the identity audit still passed

The earlier identity audit checked, by design, the exact slices and asymptotics of the newly introduced mixed deformation. In particular its A3 tracking identity verified that the `sigma`-dependent mixed correction vanishes at `Q=Q0`, so that the value of the `Y`-sector slice remains the frozen full-`J` slice.

That test did **not** independently reconstruct the `Q` curvature which generates the D1A kinetic coefficient and R3 mass term. The action-level D2C-A derivation is the first gate that simultaneously exposes the `Q` curvature and the full nonlinear `Y` sector.

Therefore

```text
NL1C6D2C_COMPLETION_IDENTITY_AUDIT_PASS
```

remains a valid restricted result, but it cannot imply full D2C PASS.

## 6. Conjunctive D2C decision

The D2C preregistration requires the action-derived completion to recover the frozen D1A zero-expansion system and exact fixed-a R3 full-`J` system at relative discrepancy `<=1e-12`.

For every one of the 27 co-primary `sigma × interpolation × beta0` members, the common Exp `Q` sector instead has an exact relative `K2`/`mu^2` discrepancy of `1.0`.

Hence at least one required inherited exact regression fails; in fact all 27 fail for the same completion-independent reason.

Under the frozen classification rule,

```text
NL1C6D2C_COVARIANT_MIXED_SECTOR_COMPLETION_FAIL
```

is therefore mandatory.

No further D2C-A algebra or D2C-B numerical regression can restore a conjunctive PASS without changing a frozen physical function/normalization, so they are intentionally not run.

## 7. Historical interpretation

This FAIL does not change earlier classifications:

- `NL1C6R3_FULL_J_BARYONIC_RECLOSURE_FAIL` remains a numerical/static reclosure FAIL, not a physical exclusion;
- D1 remains PASS in the model/normalization it explicitly audited;
- D2A remains PASS for the frozen CLASS baryon density/momentum history;
- D2B remains INCOMPLETE;
- the D2C identity audit remains PASS in its restricted scope.

What fails is the attempt to regard the currently frozen Exp CLASS cosmology and the currently frozen D1A/R3 weak-field sector, with the same numerical `K2=9500`, as two limits of one covariant `F(Y,Q)` completion.

## 8. Continuation rule

D2 nonlinear physical branch evolution remains blocked and NL1C7 remains blocked.

Continuing requires a **new preregistered model/provenance revision** that explicitly chooses one normalization and then regenerates all downstream quantities that depend on the changed sector. Two logically possible revisions are:

1. retain the D1A/R3 published quadratic normalization and replace the Exp background by
   `K_exp = K2 Z0^2 (exp(Z^2)-1)`, followed by a fresh CLASS/source/cosmology freeze; or
2. retain the current CLASS Exp function literally and reinterpret its local quadratic coefficient as `K2_local=2*K2`, followed by rebuilding D1A/R3/static mass and every downstream nonlinear result with that local coefficient.

Neither revision may be silently substituted into the historical v053 chain.
