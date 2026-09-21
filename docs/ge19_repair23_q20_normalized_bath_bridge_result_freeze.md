# GE19 Repair23 q20 normalized-bath bridge audit result freeze

## Status

Frozen final locked Repair23 bridge execution.

Classification:

\`GE19_REPAIR23_Q20_NORMALIZED_BATH_BRIDGE_AUDIT_PASS\`.

Repair23 certifies the normalized-bath dictionary and second-directional bath equation needed for q20.

It does not itself construct q20.

## Parent

Repair22 remains frozen:

\`GE19_REPAIR22_ON_SHELL_PARENT_Z20_CERTIFICATION_PASS\`

with

\`Z20_certified=true\`.

Parent freeze commit:

\`9174f2e622f42851474ed124b429bf07b2db3ac7\`.

## Successful execution

Workflow:

\`.github/workflows/ge19-repair23-run.yml\`.

Final successful run:

\`35645649788\`.

Job:

\`106485343261\`.

Conclusion:

\`success\`.

Artifact:

- ID: \`10659908576\`;
- name: \`ge19-repair23-q20-normalized-bath\`;
- uploaded artifact ZIP SHA-256:
  \`1320ce0ac0cf75fb987c562c278f68521721f5887035502d3885f6b21cd9c096\`.

## Frozen output hashes

Result JSON:

- bytes: \`2678\`;
- SHA-256:
  \`20ce1c8d7faca45fe61b68bd0c451a616c00b0bd3e22504e83467877b8a3e6c6\`.

FULL log:

- bytes: \`2678\`;
- SHA-256:
  \`20ce1c8d7faca45fe61b68bd0c451a616c00b0bd3e22504e83467877b8a3e6c6\`.

## Execution-wrapper history

The first execution run

\`35645459393\`

printed a PASS science result but the workflow step exited nonzero because \`tee\` attempted to open the FULL log before the \`results/\` directory existed.

That was an execution-wrapper failure only.

No preregistration, science implementation, equation, gate or result value was changed.

Wrapper-only fix commit:

\`02b205d82ef9c89cfcbccd1a5ec2e5429a0cc2f8\`.

The fix only adds

\`mkdir -p results\`

before \`tee\`.

The final successful run above is the frozen Repair23 result.

## Exact symbolic identities

Frozen normalized variable:

\[
z_j=\frac{\omega_j q_j}{\sqrt{w_j}},
\qquad
q_j=\frac{\sqrt{w_j}}{\omega_j}z_j.
\]

The covariant longitudinal NL0B bath equation reduces exactly on FLRW to

\[
\ddot z_j+3H\dot z_j+\omega_j^2(z_j-X)=0.
\]

With

\[
\xi=t/\tau,\qquad r_j=\omega_j\tau,\qquad h=H\tau,
\]

it becomes exactly

\[
z_{j,\xi\xi}+3h z_{j,\xi}+r_j^2(z_j-X)=0.
\]

Both symbolic residuals are exactly zero.

## GE05 linear residual audit

GE05 c1 bath residual, normalized into the z variable, versus the standard linear z equation:

relative L2:

\`4.776595495173347e-16\`.

Frozen threshold:

\`1e-10\`.

PASS.

## GE05 second-directional audit

Analytic GE05 c2 bath residual versus primary centered finite difference:

\`9.244401818347801e-09\`.

Primary versus control finite-difference c2 residual:

\`8.412483336965135e-09\`.

Frozen threshold:

\`1e-5\`.

PASS.

The deterministic analytic bath c2 L2 norm is

\`3.8008574663582553\`.

## Weight normalization audit

Holding z fixed while changing the positive node weight:

- normalized c1 weight relative L2:
  \`0.0\`;
- normalized c2 weight relative L2:
  \`0.0\`.

Thus the \`sqrt(w)\` normalization cancels exactly from the normalized z equation as required.

## Exact interval integrator audit

Frozen NL1C4 \`step_linear\` versus independent high-accuracy DOP853:

- q/z relative L2:
  \`6.796235773486602e-15\`;
- velocity relative L2:
  \`1.6810014932296363e-14\`.

Frozen threshold:

\`1e-8\`.

PASS by more than five orders of magnitude.

## Frozen second-order bath hierarchy

First order:

\[
G_1[Z_{10},z_{10}]=0.
\]

Second order:

\[
G_1[Z_{20},z_{20}]
+
G_2[(Z_{10},z_{10}),(Z_{10},z_{10})]
=0.
\]

Perturbative convention:

\[
Z=\bar Z+\epsilon Z_{10}+\frac{\epsilon^2}{2}Z_{20}+\cdots.
\]

Physical normalized-bath dictionary:

\[
q_{20,j}=\frac{\sqrt{w_j}}{\omega_j}z_{20,j}.
\]

## Frozen GE19 scalar dictionary

- N -> N10/N20;
- L,R -> S10/S20;
- b -> 0 in the frozen plane-symmetric scalar reduction;
- rapidity -> u10/u20;
- scalar -> phi10/phi20;
- first-order drive:
  \`X10=Q_action u10 + partial_x(phi10)/a\`.

No nonlinear Fourier \`k chi\` prescription is introduced.

## Frozen q20 boundary convention

For future q20 construction:

- z10 at z=1.5 is inherited from the full-history positive-Drude retarded bath and then evolved on the reduced on-shell H1 parent;
- z20(z=1.5)=0;
- dz20/dxi(z=1.5)=0.

The z20 condition defines a **window-local particular second-order bath state**.

It does not certify or assume a primordial/homogeneous second-order bath mode.

## Gates

All 10 frozen Repair23 gates PASS.

## Next licensed step

Repair24 may now construct q20 on the certified Repair22 Z20 state.

It must retain:

- the Repair23 normalized z dictionary;
- the positive Drude measure;
- tau H0=10;
- the frozen full-history z10 initial state;
- the reduced on-shell H1 parent inside the GE19 window;
- zero window-local z20 homogeneous boundary;
- quadrature convergence;
- Nt128/Nt64 time control;
- explicit low-mode spatial control.

No H4/Z21 solve until Repair24 q20 is frozen.
