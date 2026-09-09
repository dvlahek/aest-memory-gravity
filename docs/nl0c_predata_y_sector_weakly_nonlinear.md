# NL0C predata — weakly nonlinear AeST Y-sector audit

Classification before audit: **NL0C_PREDATA_Y_SECTOR_WEAKLY_NONLINEAR**

This is an analytic theory-only gate. It uses no observational data and no nonlinear numerical outcome. The closed v0.77/v0.78 linear chain and the NL0B memory completion remain unchanged.

## 1. Frozen continuation of the free function

For the strong nonlinear path use the minimal separable continuation

\[
\mathcal F(\mathcal Y,\mathcal Q)
=-2\mathcal K(\mathcal Q)+(2-K_B)\mathcal J(\mathcal Y).
\]

The \(\mathcal K(\mathcal Q)\) branch is exactly the already frozen Cosh/Exp cosmological branch. No change is made to \(Q_0,K_2,Z_0\) or to the background calibration.

The \(\mathcal Y\) branch is the published AeST MOND branch. In inverse-screening notation \(\beta_0=1/\lambda_s>0\),

\[
\mathcal J(\mathcal Y)
=\frac{2}{3(1+\beta_0)a_0}\,\mathcal Y^{3/2}
+o(\mathcal Y^{3/2})
\qquad (\sqrt{\mathcal Y}\ll a_0).
\]

For later numerical work the MOND acceleration is frozen to

\[
a_0=1.2\times10^{-10}\;{\rm m\,s^{-2}},
\]

and the screening control is not to be selected after seeing outcomes. The preregistered co-primary values are the three values explicitly used in the 2024 AeST quasistatic study:

\[
\beta_0\in\{1,0.5,0.1\}.
\]

No result may be promoted by choosing one of these values after the fact; all three must be reported.

## 2. Perturbative ordering to be audited

Around homogeneous FLRW,

\[
X_\mu=h_\mu{}^\nu\nabla_\nu\phi=O(\epsilon),
\qquad
\mathcal Y=X_\mu X^\mu=O(\epsilon^2).
\]

The audit must establish the order at which the published MOND branch enters the equations of motion and whether a full interpolation function is needed for the first weakly nonlinear calculation.

## 3. Locked questions

### C1. Linear preservation

Show that

\[
\mathcal J(0)=0,
\qquad
\mathcal J_{\mathcal Y}(0)=0,
\]

so the new \(\mathcal Y\) branch does not change the already certified background or linear perturbation system.

### C2. Leading nonlinear order

Determine the perturbative order of

\[
\sqrt{-g}\,(2-K_B)\mathcal J(\mathcal Y)
\]

and of its field equations around FLRW.

### C3. Sufficiency of the small-gradient asymptote

Determine whether differences among full interpolation functions with the same deep-MOND asymptote can enter the equations at the same order as the first nonlinear correction. If they enter only at higher order, NL1 must use only the asymptotic coefficient and must not introduce an arbitrary interpolation shape.

### C4. Q–Y cross freedom

Because the continuation is frozen as separable, verify that

\[
\mathcal F_{\mathcal Y\mathcal Q}=0
\]

and therefore no unconstrained mixed \(\delta Q\,\mathcal Y\) vertex is introduced in NL1.

### C5. Form of the leading MOND force

Derive the leading real-space nonlinear operator. The expected structure is proportional to

\[
\nabla_\mu\left(\sqrt{\mathcal Y}\,X^\mu\right),
\]

which in the weak-field spatial limit becomes

\[
\nabla\cdot\left(|\nabla\chi|\nabla\chi\right).
\]

The exact coefficient must follow from the frozen action.

### C6. Standard F2 versus nonanalytic homogeneous response

Determine whether the \(\mathcal Y^{3/2}\) term admits an ordinary bilinear Fourier-space second-order kernel \(F_2(\mathbf k_1,\mathbf k_2)\) about the zero-gradient FLRW state. If not, NL1 must be formulated in real space (or as a directional/homogeneous second-order response) rather than forcing the MOND term into an invalid polynomial SPT kernel.

### C7. Screening values

All analytic formulae must retain \(\beta_0\) explicitly. Subsequent numerical tests must evaluate all three preregistered values \(1,0.5,0.1\) with the same grids and gates.

## 4. Classification rule

If C1–C7 are resolved consistently without adding new free functions or outcome-informed choices:

**NL0C_Y_SECTOR_WEAKLY_NONLINEAR_PASS**

Otherwise:

**NL0C_Y_SECTOR_WEAKLY_NONLINEAR_FAIL_OR_INCOMPLETE**

A PASS closes the theory-definition stage needed for the first weakly nonlinear calculation. It does not certify nonlinear structure formation and does not determine the later high-gradient/virial interpolation required for NL2/NL3.

## 5. Historical results

Nothing in NL0C can alter:

- `V077_NATIVE_STATE_TANGENT_AFFINITY_PASS`;
- `V078_TIME_INTERPOLATION_OPERATOR_CLOSURE_PASS`;
- `NL0B_COVARIANT_MEMORY_COMPLETION_PASS`;
- any historical FAIL classification.
