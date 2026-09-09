# NL0 equation audit: what is fixed, what is nonlinear, and what is still missing

Status: **NL0_AUDIT_COMPLETE_NONLINEAR_MEMORY_COMPLETION_REQUIRED**

This audit starts from the closed linear chain (v0.77 and v0.78 PASS) and asks what can be promoted into a controlled nonlinear calculation without changing the historical linear model.

## 1. Exact nonlinear AeST starting point

The underlying AeST theory is defined covariantly by the Skordis--Zlosnik action

\[
S=\frac{1}{16\pi \tilde G}\int d^4x\sqrt{-g}\left[
R-\frac{K_B}{2}F^{\mu\nu}F_{\mu\nu}
+2(2-K_B)J^\mu\nabla_\mu\phi
-(2-K_B)\mathcal Y
-\mathcal F(\mathcal Y,\mathcal Q)
-\lambda(A^\mu A_\mu+1)
\right]+S_m[g],
\]

with

\[
F_{\mu\nu}=2\nabla_{[\mu}A_{\nu]},\qquad
J_\mu=A^\alpha\nabla_\alpha A_\mu,
\]

\[
\mathcal Q=A^\mu\nabla_\mu\phi,\qquad
\mathcal Y=q^{\mu\nu}\nabla_\mu\phi\nabla_\nu\phi,
\qquad q_{\mu\nu}=g_{\mu\nu}+A_\mu A_\nu.
\]

This is a genuinely nonlinear relativistic field theory. A full non-perturbative Hamiltonian formulation of AeST also exists in the literature, so nonlinear AeST itself is not conceptually undefined.

References:

- C. Skordis and T. Zlosnik, Phys. Rev. Lett. 127, 161302 (2021), doi:10.1103/PhysRevLett.127.161302.
- M. Bataki, C. Skordis and T. Zlosnik, Phys. Rev. D 110, 044015 (2024), doi:10.1103/PhysRevD.110.044015.

## 2. Matter equations: what is already exact

Because matter is minimally coupled to the metric, the exact covariant statement is

\[
\nabla_\mu T^{\mu\nu}_{m}=0.
\]

For pressureless matter, the controlled weak-field/subhorizon reduction gives the standard nonlinear continuity and Euler equations in conformal time,

\[
\delta'+\nabla\cdot[(1+\delta)\mathbf v]=0,
\]

\[
\mathbf v'+\mathcal H\mathbf v+(\mathbf v\cdot\nabla)\mathbf v=-\nabla\Psi.
\]

Therefore the usual fluid convective nonlinearities are not an approximation specific to GR; they follow from minimal matter coupling once the weak-field/subhorizon limit is taken. In Fourier space these generate the standard \(\alpha\) and \(\beta\) mode-coupling vertices.

The modified-gravity content enters through the relation between \(\Psi\), the AeST fields, and the matter variables. That force/closure sector is the part that must be derived from AeST rather than borrowed from GR.

## 3. Nonlinear AeST vertices that exist before adding memory

Expanding the covariant action beyond first order generates nonlinear interactions from all of the following:

1. the Einstein tensor built from \(g_{\mu\nu}\);
2. the unit-timelike constraint \(A^\mu A_\mu=-1\);
3. the vector kinetic term \(F^2\);
4. the acceleration-scalar coupling \(J^\mu\nabla_\mu\phi\);
5. the orthogonal scalar-gradient invariant \(\mathcal Y\);
6. the nonlinear free function \(\mathcal F(\mathcal Y,\mathcal Q)\).

These are genuine modified-gravity nonlinear vertices. They are distinct from the standard fluid convective vertices.

A second-order density calculation requires the gravitational action/equations to one higher perturbative order than the current linear CLASS implementation. Equivalently, one must know the terms that source second-order metric, scalar and aether perturbations, not just the first-order transfer system.

## 4. What the current repository actually implements

The current frozen cosmological implementation is a background + **linear scalar perturbation bridge** inside CLASS. It is not a full nonlinear AeST solver.

The background module fixes the chosen \(\mathcal K(\mathcal Q)\)-sector through the Cosh/Exp parametrizations. The linear scalar system evolves the effective AeST density/velocity variables together with \(\alpha\) and

\[
E=\dot\alpha+\Psi.
\]

At linear order the repository uses

\[
\chi=Q\left(\frac{a\,\theta}{k^2}+\alpha\right),
\]

and the memory-free AeST closure

\[
E_{\rm rhs}=K_Q\chi-(2-K_B)\left[
\frac{Q\Pi}{1+w}+(H+Q)\chi-3c_{ad}^2HQ\alpha
\right].
\]

This implementation is sufficient for the certified linear response. It does **not** by itself specify all second-order AeST vertices needed for nonlinear structure formation.

In particular, the full dependence of \(\mathcal F(\mathcal Y,\mathcal Q)\) away from the FLRW/linear trajectory must be fixed before a result can be called a unique nonlinear prediction of the same theory. Linear cosmology constrains fewer derivatives of the free function than a second-order calculation can probe.

## 5. What the current memory extension implements

The preserved memory implementation is even more specific: it is a **linear scalar-sector finite positive Drude bath**.

For each bath mode,

\[
q_j'=p_j,
\]

\[
p_j'=-2\mathcal H p_j-a^2\omega_j^2q_j
+a k\omega_j\sqrt{w_j}\,\chi,
\]

and

\[
B_\chi=\eta\sum_j\left[
w_j\chi-\sqrt{w_j}\frac{a\omega_j}{k}q_j
\right].
\]

The memory modifies only the linear \(E\)-closure,

\[
E_{\rm rhs}\rightarrow E_{\rm rhs}-\frac12 Q B_\chi.
\]

The preserved source audit explicitly has

- memory background correction = 0;
- direct linear memory Einstein stress = 0.

The eta=0 variational forcing used in the certified v0.77 state tangent is therefore

\[
\left.\frac{dE'}{d\eta}\right|_{\eta=0}
=-\frac{aQ}{2K_B}B_{\chi,\rm raw}.
\]

This is exactly the linear memory model that is now numerically certified.

## 6. Critical NL0 result

**The repository does not yet contain a nonlinear or covariant completion of the memory bath.**

There is currently no action or nonlinear field system specifying what replaces \(\chi\), \(q_j\), and \(B_\chi\) when perturbation modes couple to one another.

That means we must not simply take a standard nonlinear matter solver and append the linear \(B_\chi\) term. Such a calculation could be a phenomenological model, but it could not honestly be labelled full nonlinear AeST+memory.

There are therefore two theory-completion questions before NL1:

1. **AeST completion:** fix the required nonlinear continuation of the chosen \(\mathcal F(\mathcal Y,\mathcal Q)\) sector used by the frozen cosmological model.
2. **Memory completion:** construct a nonlinear auxiliary-field or explicitly nonlocal formulation whose linearization reproduces the exact preserved finite-bath equations and \(-QB_\chi/2\) closure.

## 7. Constraints on an acceptable nonlinear memory completion

Any completion used in the strong path must satisfy all of the following before numerical results are inspected.

### R1. Preserve the existing linear model

Linearization on the same FLRW background must reproduce the frozen equations for \(q_j,p_j,B_\chi\) and the \(E\)-closure exactly, including the same \(w_j\), \(\omega_j\), \(\eta\), and \(\tau H_0\).

### R2. Preserve the background null result

The homogeneous FLRW memory correction must remain zero unless a new background effect is explicitly introduced as a new theory and separately justified.

### R3. Preserve the linear stress audit

The completion must not generate a direct \(O(\eta\,\delta)\) Einstein stress that was absent from the frozen linear model.

### R4. Causality / retarded structure

The auxiliary system or nonlocal kernel must implement a causal retarded response and retain the positive-bath construction.

### R5. No hidden post-result freedom

No new nonlinear shape parameters may be tuned to preserve the desired delay/advance sign. Any unavoidable new parameter must be declared and frozen before the corresponding nonlinear result.

### R6. Physical eta remains distinct from tangent lambda

The signed numerical tangent amplifier \(\lambda\) used in the linear validation is not a physical coupling and must not enter the nonlinear theory definition.

### R7. Define a nonlinear completion of chi

The key object is a covariant or 3+1 quantity \(\Xi[g,A,\phi,\text{matter}]\) whose first-order scalar perturbation is exactly the current \(\chi\). The bath must couple to \(\Xi\), not to a hand-inserted Fourier-space linear variable.

### R8. Mode coupling must be well-defined in real space

The present linear forcing contains a factor \(k\chi\). At nonlinear order independent Fourier modes no longer exist, so this factor must arise from a well-defined spatial operator or local auxiliary-field structure. A longitudinal aether-orthogonal auxiliary vector is one possible route because a local gradient coupling can yield a single power of \(k\) in the scalar longitudinal sector, but this is a candidate construction, not yet an established part of the theory.

## 8. What can already be carried into NL1

The following pieces are safe and do not need to be rediscovered:

- the v0.77 certified native state tangent \(\partial_\eta d_m|_0\);
- the v0.78 interpolation closure diagnosis;
- exact matter stress-energy conservation;
- standard weak-field fluid convective vertices;
- the covariant nonlinear AeST action as the baseline gravitational theory.

The following pieces are **not** yet safe:

- a second-order AeST+memory force law;
- an \(F_2^{\rm AeST+mem}\) kernel;
- spherical collapse with memory;
- an N-body memory force;
- a nonlinear \(P(k)\) prediction.

## 9. Immediate next task: NL0A

Before any nonlinear simulation, derive a minimal nonlinear memory completion and prove the following symbolic reduction chain:

\[
S_{\rm AeST}+S_{\rm mem}^{\rm candidate}
\longrightarrow
\text{nonlinear field equations}
\longrightarrow
\text{FLRW background: memory}=0
\longrightarrow
\text{first-order scalar system}
\longrightarrow
\text{exact frozen Drude bath and }-QB_\chi/2.
\]

Only after this identity is demonstrated do we freeze the second-order equations and start NL1 mode-coupling numerics.

## 10. Scientific interpretation

NL0 does not weaken the v0.77/v0.78 result. The linear memory signal remains certified.

It instead identifies precisely what is required to make the stronger statement that memory changes **nonlinear structure formation**. The next novelty is therefore theoretical as well as numerical: a nonlinear completion that is forced to reduce to an already certified linear prediction.
