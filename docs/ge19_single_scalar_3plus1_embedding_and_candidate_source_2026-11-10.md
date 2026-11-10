# GE19 — one integrated covariant-to-linear-scalar CLASS bridge (no new LW stage)

**Date:** 2026-11-10.  
**Status:** \`LINEAR_SCALAR_CANDIDATE_KINEMATIC_EMBEDDING_SUPPORTED / PHYSICAL_CLASS_PRODUCTION_BLOCK / DES_OBSERVATION_BLOCK\`.  
**Method:** Direct theoretical reconstruction from the original NL0 and GE05/GE06 actions, together with archived LW24–LW33 Euler/constraint identities. This is **new conceptual synthesis**, **not** another source-locked symbolic certification, not an independently checked full covariant derivation, no numerical CLASS run, and no detection. The historical original v019j patch stays completely frozen.

## 1. Why a plane-symmetric reduction can cover *all linear scalar Fourier amplitudes* on FLRW

For a rotationally invariant background, scalar, transverse vector and tensor representations **decouple at first order**. For an arbitrary one-mode scalar Fourier wavevector \(\boldsymbol k\ne0\), rotate the spatial frame so \(\boldsymbol k=k\hat{\boldsymbol x}\). Before gauge-fixing, write

\[
ds^2=-(1+2\Psi)dt^2
+2a\,\partial_i B_g\,dt\,dx^i
+a^2\left[(1-2\Phi)\delta_{ij}
+2\partial_i\partial_j E_g\right]dx^idx^j.
\]

For a wave along \(x\), the independent scalar metric data embed in the original GE06 plane-symmetric coframe as

\[
N=1+\Psi,\quad
L=a(1-\Phi-k^2E_g),\quad
R=a(1-\Phi),\quad
b=\frac{ik}{a}B_g +O(\epsilon^2),
\]
where \(g_{0x}=L^2b\). In Newtonian gauge \(B_g=E_g=0\) only **after varying** with respect to \(N,L,R,b\). The aether scalar perturbation \(A_x=ik\alpha\) is encoded by \(\sinh u=A_x/L\), hence \(u=ik\alpha/a+O(\epsilon^2)\). The covariant scalar perturbation is \(\phi=\bar\phi+\varphi\). A scalar auxiliary-vector mode has \(U_i\parallel k_i\), so only its \(x\)-component remains, with \(U_x=aU_{\hat x}\) at FLRW first order. This field inventory contains all four scalar metric variables, a scalar-aether longitudinal mode, a scalar perturbation, and the longitudinal scalar of every auxiliary vector. A transverse vector or tensor is **not** a linearly mixing missing scalar mode on FLRW.

**Important proof limit:** representation completeness does *not*, by itself, verify that a specific reduced action is the faithful restriction of the full covariant action, or that each legacy CLASS equation is the correct change of variables. These are separate obligations below.

## 2. Why the GE06 analytic gravitational/aether density has the correct covariant structure

Start from the actual frozen covariant AeST form in \`docs/nl0_equation_audit.md\`:

\[
\mathcal L_{\rm AeST}=R-\frac{K_B}{2}F_{\mu\nu}F^{\mu\nu}
+2C J^\mu\nabla_\mu\phi-C\mathcal Y
-\mathcal F(\mathcal Y,\mathcal Q)
-\lambda(A^2+1),\qquad C=2-K_B,
\]
and \(\mathcal F=-2K(\mathcal Q)+C\mathcal J(\mathcal Y)\) in the frozen branch.

In the orthonormal 1+1 coframe \(\theta^0=Ndt,\theta^1=L(dx+b\,dt)\), write a unit aether \(A^\flat=-\cosh u\,\theta^0+\sinh u\,\theta^1\) and a unit spatial normal \(n^\flat=-\sinh u\,\theta^0+\cosh u\,\theta^1\). Then \(\mathcal Q=A^\mu\partial_\mu\phi\) and \(X=n^\mu\partial_\mu\phi\) are exactly the GE06 \`Qinv\` and \`Xinv\` expressions. The spatial acceleration/electric scalar \(E=n_\mu A^\nu\nabla_\nu A^\mu\) is GE06's \`E\`. In the longitudinal sector \(F^2=-2E^2\), \(J^\mu\nabla_\mu\phi=EX\) and \(\mathcal Y=X^2\), hence the *analytic* AeST density indeed has the original structure

\[
\mathcal L_{\rm analytic}/(NLR^2)=K_BE^2+2CEX-CX^2+2K(\mathcal Q).
\]

The GR part is the original reduced ADM/EH expression, up to the explicit spatial integration-by-parts boundary choice; LW30 and LW31 varied the independent lapse/shift and L/R equations before gauge fixing.

The frozen \(\mathcal J(\mathcal Y)\sim C_\beta\mathcal Y^{3/2}\) obeys \(\mathcal Y=O(\epsilon^2)\), so **its quadratic scalar action vanishes** on relaxed FLRW, although its second-order *field equations* are nonzero. This provides a reason why the NL0C/nonanalytic Y problem does **not** by itself invalidate the *linear* scalar candidate. It must NOT be extrapolated to nonlinear H4/Z21 results.

## 3. Explicit covariant projected bath derivative → GE05 longitudinal action

The frozen NL0B positive auxiliary action has, per mode,
\[
\mathcal L_{\rm mem}
=\frac{\sqrt{-g}}4\left[(\mathscr D_AU_\mu)(\mathscr D_AU^\mu)
-(\omega U_\mu-\sqrt{\eta w}\,X_\mu)
(\omega U^\mu-\sqrt{\eta w}\,X^\mu)\right],
\]
subject to \(A\cdot U=0\). In the 1+1 scalar/longitudinal coframe write **exactly** \(U_\mu=U\,n_\mu\) and \(X_\mu=X\,n_\mu\). Then

\[
\mathscr D_A(U n_\mu)
=h_\mu{}^\nu A^\rho\nabla_\rho(U n_\nu)
=(A^\rho\partial_\rho U)n_\mu+
U\,h_\mu{}^\nu A^\rho\nabla_\rho n_\nu.
\]

Because \(A\cdot n=0\), \(n\cdot n=1\), and within the 1+1 coframe the derivative of the unit spatial normal has only a component **parallel to \(A\)**, the projector kills the final term. In this longitudinal sector,

\[
\boxed{\mathscr D_A(U n_\mu)=(AU)n_\mu},
\qquad
AU=\frac{\cosh u}{N}(\partial_tU-b\partial_xU)
+\frac{\sinh u}{L}\partial_xU.
\]

This is precisely the **original GE05** \`Aq\`; likewise its \`Xphi\` is the covariant projected scalar gradient. Thus the complete *longitudinal* bath scalar action reduces to

\[
\boxed{
\mathcal L_{\rm mem}^{\rm long}=
\frac{NLR^2}{4}[(AU)^2-(\omega U-\sqrt{\eta w}X)^2]
}
\]
without an omitted longitudinal connection term. For a general scalar mode on FLRW the corresponding physical triad is parallel to \(\boldsymbol k\); transverse components decouple at quadratic order. Unit and auxiliary multipliers are algebraically eliminated on the regular branch, as in LW32.

**Claim limit:** this geometric step supports the *quadratic scalar action* correspondence, not the complete nonlinear multidirectional GE05 construction, vector/tensor dynamics, or finite-eta numerical solution.

## 4. Original CLASS effective-fluid variables and the conditional normalized source

The archived action-derived linear effective-fluid dictionary (proper time) is

\[
\delta Q=\dot\varphi-Q\Psi,\quad E_A=\dot\alpha+\Psi,\quad\chi=\varphi+Q\alpha,
\]
\[
\rho_A=\frac{QK_Q-K}{3},\quad p_A=\frac K3,\quad
D_A=\frac13\left[QK_{QQ}\delta Q-\frac{k^2}{a^2}(K_BE_A+C\chi)\right],\quad
\theta_A=\frac{k^2\varphi}{aQ}.
\]

LW30 gives the restricted GR+AeST Hamiltonian and momentum constraints and LW31 the scalar traceless shear; LW32 handles regular unit/auxiliary multiplier elimination; LW33 gives the complete reduced off-shell scalar-charge equation in this same dictionary. LW25's original variation of the *combined* longitudinal AeST+NL0B action yields

\[
\boxed{
K_B(\dot E_A+HE_A)=K_Q\chi
-C[\dot\chi-QE_A+(H+Q)\chi]
-\frac{\eta Q}{4}B_{\chi,\rm raw}.
}
\]
The original v019/v019j equations for \(\theta_A\) and \(\alpha_A\) imply the frozen \(\dot\chi\) kinematics. The LW33 scalar-charge identity then leaves

\[
\mathscr S_{\phi,\rm rem}=\frac{a\eta k^2B_{\chi,\rm raw}}2(1-4\gamma).
\]

Thus in the **linear scalar quadratic sector with the original fixed CLASS state dictionary**, \(\gamma=1/4\) is the **action-normalized candidate**. The historical v019j code uses \(\gamma=1/2\) and an extra unaccounted scalar-current source residual within that dictionary. Do not silently halve old \(\eta\) inference: the full coupled evolution and physical interpretation depend on the implemented source and response.

The existence of a faithful 3D scalar field embedding is meaningful new support for the action-based source normalization. It still does not constitute an independent, complete line-by-line validation of every production CLASS approximation switch, species response, initial condition and retarded transfer.

## 5. Decision: separated linear scalar *candidate* is scientifically motivated; production/observations remain BLOCK

**Narrow candidate permission:** A **separate, explicitly marked exploratory source branch** may prepare a copy of the original v019j-patched CLASS code with only the E-row bath coefficient changed to \`0.25\`, leaving \`v019j\` and original official CLASS checkout untouched. This is a controlled *hypothesis implementation* supported by the scalar-action source theorem and the rotational embedding argument, **NOT** a certified physical model, nor permission to publish old LW01/06 or new DES data results as physical observations.

**Production \`PHYSICS_GO\` is still withheld**, because the complete independent full action-to-C-evolution source/gauge/constraint propagation verification and ordinary-species feedback across all used CLASS approximation branches has not been executed. The first necessary local gate after preparing the candidate is a single regression of \(\eta=0\) recovery, coefficient in the C source, correct retarded auxiliary initialization and Einstein-constraint propagation on the actual CLASS branch. Fail closed; no source tuning.

**DES gate:** Physical \(\partial_\eta P_{D_mW}\) and the nuisance-marginal DES Y3 MagLim4×Source4 (Source3 control) GGL test are still **BLOCKED**. Existing LW08 differential tangent is unresolved and the LW22 efficiencies are geometry-only. A numerical source signal, absent a physical propagator and meaningful bias/IA nuisance discriminant, is *not* detection of gravitational memory.

This one document replaces further LW34/LW35 symbolic micro-audits. Historical PASS and FAIL reports remain untouched; no new cosmological run was started in this synthesis.

## Reviewed sources

- \`docs/nl0_equation_audit.md\` (original covariant AeST action)
- \`docs/nl0b_predata_covariant_memory_completion.md\` (covariant positive NL0B auxiliary)
- \`docs/nl0c_y_sector_weakly_nonlinear_result.md\` (nonanalytic Y order)
- \`ge06/analytic_aest_directional_source_generator.py\` (original 3+1 plane-symmetric reduction)
- \`ge05/memory_directional_source_generator.py\` (original longitudinal auxiliary reduction)
- \`v019/apply_patch_v019.py\`, \`v019j/apply_memory_patch.py\` (original frozen CLASS state/forcing)
- \`docs/ge19_lw25_reduced_aether_shift_class_memory_source_consistency_2026-11-10.md\`
- \`docs/ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md\`
- Skordis & Złośnik, *Phys. Rev. Lett.* **127**, 161302 (2021), doi:10.1103/PhysRevLett.127.161302.
- Bataki, Skordis & Zlosnik, *Phys. Rev. D* **110**, 044015 (2024), doi:10.1103/PhysRevD.110.044015 (full AeST Hamiltonian analysis; not a validation of this NL0B patch).
