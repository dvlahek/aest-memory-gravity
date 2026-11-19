# GE19 — Scalar Ward current does not algebraically select the primordial stress-null amplitude

19 November 2026. Narrow physics decision from **existing original reduced scalar-action current**, not a new CLASS or DES campaign.

**Classification: REDUCED_SCALAR_CURRENT_INITIAL_DATA_TEST_EXACT / NO_ALGEBRAIC_SELECTION_OF_STRESS_NULL_AMPLITUDE / PHYSICAL_FINITE_K_ADIABATIC_MODE_OPEN.**

## Original initial stress-null perturbation

At regular finite \`t_i\`, with fixed metric, ordinary species and \`varphi\`, the source-locked original action density/pressure/momentum dictionary has an instantaneous stress-null direction
\`\`\`math
\Delta\chi=\epsilon,\quad
\Delta E_A=-\frac{C}{K_B}\epsilon,\quad
\Delta(\delta Q)=0,\quad\Delta\varphi=0,\quad
C=2-K_B,\quad \Delta\alpha_A=\frac{\epsilon}{Q}.
\`\`\`
It leaves \`D_A,P_A,T_A\` unchanged at this instant but has distinct scalar/aether state. It is not automatically a valid physical adiabatic primordial eigenmode.

## Independent check against the actual original action scalar-current equation

The previously certified restricted original action current in LW33 reads
\`\`\`math
J_\phi^t=2a^3K_{QQ}\delta Q-6a^3K_Q\Phi,\qquad
J_\phi^x=ika[2C(E_A-\chi)+2K_Q\alpha_A-\eta B_\chi/2]
\`\`\`
and the scalar Euler equation is \`-dot J_phi^t-i k J_phi^x=0\`. For the selected no-free-bath auxiliary initial state \`q_j(t_i)=dot q_j(t_i)=0\`, the direct retarded bath difference at the initial instant is \`Delta B_chi(t_i)=W_b epsilon\` **if comparing nonzero eta states**, not zero. Therefore the exact general initial spatial current variation is
\`\`\`math
\boxed{
\Delta J_\phi^x(t_i)
=ika_i\epsilon\left[2\frac{K_Q}{Q}-\frac{4C}{K_B}
-\frac{\eta W_b}{2}\right].
}\tag{1}
\`\`\`
In particular, at the **eta=0** baseline used for the one-sided tangent:
\`\`\`math
\boxed{
\Delta J_\phi^x|_{\eta=0}
=2ika_i\epsilon\left(\frac{K_Q}{Q}-\frac{2C}{K_B}\right).
}\tag{2}
\`\`\`
The temporal current variation is initially \`Delta J_phi^t(t_i)=0\` since \`Delta(delta Q)=Delta Phi=0\`. But its **derivative** is not fixed by these instantaneous equalities: the scalar Euler requires
\`\`\`math
\boxed{
\Delta\dot J_\phi^t(t_i)=
a_i k^2\epsilon\left[2\frac{K_Q}{Q}-\frac{4C}{K_B}-\frac{\eta W_b}{2}\right].
}\tag{3}
\`\`\`
Thus the independent scalar Euler equation is a *dynamical requirement on the next time derivative*, not an algebraic condition setting epsilon to zero. At eta=0 the finite-bath Euler equation is degenerate; the right-sided eta->0+ retarded branch must be declared separately.

The aether and kinematic evolution can further restrict the admissible combinations and all higher derivatives. An initial stress-map kernel is **not** proof of an independent physical mode, and a nonzero spatial scalar current is **not** by itself a failure of scalar conservation.

## A precise consequence for the observational stop

For finite-k radiation-era physical primordial perturbations, the allowed epsilon must be selected through the **joint regular/adiabatic Frobenius initial-data problem for the complete Einstein–AeST–NL0B + photons/neutrinos equations**, not by an instant Einstein-stress fit or by imposing scalar-current spatial flux = 0. The current is not required to have zero spatial flux; its divergence must be compensated by temporal charge evolution.

The original GE06 analytic source generator *explicitly excludes* the nonanalytic Y sector, but the frozen NL0C result shows that Y^(3/2) enters the action at cubic order around relaxed FLRW and adds no **linear** correction. Thus absence of Y in the linear action is an order-consistent simplification for this specific primordial linear gate; do not misidentify it as the source of the current linear obstruction. Full 3+1 linear operator equivalence and external CLASS implementation remain unverified.

**Next decisive physics task:** rather than repeated local h5/h6 onset lemmas, construct and solve one finite-k adiabatic initial-mode matrix using the completed original linear all-species action, with all constraints and original scalar charge, record whether the stress-null amplitude is removed, retained as a physical isocurvature amplitude or remains underdetermined. Then only with a source-certified physical observer move to DES Y3 MagLim4 x Source4 Asimov. No real observed shear fit yet.

## Sources

- [Original reduced scalar current and off-shell Ward](ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md)
- [Initial stress-map null direction](ge19_20261119_primordial_initial_stress_null_direction.md)
- [Frozen reduced h5/h6 onset](ge19_20261119_general_initial_chi_delayed_weyl_h5_vs_h6.md)
- [Y sector enters beyond linear](nl0c_y_sector_weakly_nonlinear_result.md)
- [First observability return gate](ge19_20261119_observability_return_single_gate_decision.md)
