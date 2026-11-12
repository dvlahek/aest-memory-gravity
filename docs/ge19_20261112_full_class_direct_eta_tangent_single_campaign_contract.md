# GE19 — exactly one full-CLASS direct eta-tangent implementation campaign: frozen contract

**12 November 2026. State of evidence:** source-locked WSL 4/4 late-dust proxy tangent **PASS**, full CLASS **NOT YET IMPLEMENTED**, no DES detection. This is a concrete engineering acceptance contract, **not** a claim that source modifications below were implemented or executed. No additional eta amplitude sweep and no post-hoc tuning.

## Why the WSL result does not decide observability

The original researcher's [WSL JSON](../results/ge19_late_dust_tangent_20261112_wsl.json) and [WSL log](../results/ge19_late_dust_tangent_20261112_wsl.log) were uploaded and byte-exactly archived, and matched the earlier standalone run except for source-lock provenance. On the restricted AeST + pressureless standard-dust proxy + Lambda system with 15 order-16 bath nodes, k=0.1 h/Mpc and z=19 to 0.5, the direct W/W0 derivative is 1.947568593367276e-20 per unit eta. DOP853/Radau relative difference is about 1.2e-12 and independently propagated density satisfies Hamiltonian at roughly 1e-15 relative.

**The numerical number is not a full GE19 prediction.** At z=19 all chi,E,q,p were reset to zero, so the entire primordial forced memory was deleted. The proxy has no photon temperature/polarization, no neutrino hierarchy/shear, no full radiation/matter transition, and no real galaxy observer. A physically amplified early retarded response can be completely absent from this restricted calculation.

## Frozen target and actual source entrypoints

- Original CLASS v077 parent: lesgourg/class_public, commit e85808324f51fc694d12e3ed7439552a3c3f9540. Original source/perturbations.c blob c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0.
- Keep the frozen Exp input with original Q0, K2, Z0, KB, H0 and matter densities, the separate *quarter action-compatible candidate* for E, and normalized order-16 positive NL0B nodes. Do not overwrite the historical half-source branch.
- The actual CLASS C functions that need intervention are perturbations_solve (ode callbacks and source scheduling), perturbations_derivs (the full species + metric system), perturbations_vector_init (dynamic approximation-vector rebuild), perturbations_einstein (Psi and Phi-prime), and perturbations_sources (readout).
- Original v019/apply_patch_v019.py and v019j/apply_memory_patch.py establish the AeST-specific CDM-slot stress/velocity and q/p state indices. In conformal time, the quarter candidate's E row has a direct eta-dependent contribution -a Q eta Bchi/(4 KB), with Bchi = sum_j[w_j chi - sqrt(w_j)*(a omega_j/k)*q_j]. **Do not put eta inside Bchi and again multiply it outside.**

## Exact baseline + tangent mathematics

At eta=0, integrate the ENTIRE native CLASS perturbation state Y0, **including q/p that remain continuously driven but do not backreact**. With identical model, k, time, primordial adiabatic/no-free-bath initial state, calculate the companion derivative Y1 = partial_eta Y|eta=0 by

    dY0/dtau = F0(tau,Y0)
    dY1/dtau = F0(tau,Y1) + e_E * [-a(tau)*Q(tau)*Bchi(Y0)/(4*KB)]

for every active approximation interval. This is valid only after source-level verification that the eta=0 native scalar RHS is **linear in Y** at fixed background and approximation state, so F0(tau,0)=0 and additivity hold. If hidden nonlinearity is found, use an analytic Jacobian-vector product instead; do not assume linearity.

The full Y1 includes the metric variable, all photons and polarization, baryon density/velocity, UR/ncdm hierarchy, AeST fluid and aether, and auxiliary q/p if still allocated. Do not integrate a standalone (chi,E) tangent and call it Weyl.

**Implementation choice:** prefer an augmented baseline/tangent state in the SAME CLASS interval and integrator, so both see identical k/tau/background/approximation switches. Derivative callbacks must maintain separate temporary Einstein-source workspaces (or demonstrably reentrant evaluations); simply calling the original perturbations_derivs twice on shared mutable workspace can corrupt the source. Alternatively use two-phase baseline/forced-tangent runs only if Bchi0(t,k) is recorded on an adequately resolved, error-certified source grid and interpolated without skipping rapid bath oscillations. Do not append raw implicit-solver RHS callback points as a time-ordered trajectory: implicit/stiff solvers may evaluate times out of order.

**Vector-switch transfer:** each CLASS approximation-vector rebuild is a map R(tau) on the physical perturbation state. Both Y0 and Y1 require the **same linear rebuild**. Source terms and background-dependent offsets must be audited; the tangent map is J_R*Y1 plus any explicit eta derivative (zero for fixed eta-independent switches, only after verification). Check TCA/RSA/UFA/NCDM transitions explicitly. The AeST alpha/E/q/p coordinates must survive switch and retain the selected primordial retarded history.

**Initial state:** start at the genuine pinned early radiation epoch with the single physically allowed leading multi-species adiabatic growing mode, no independent bath homogeneous q/p excitation, and no artificial z=19 reset. The already derived leading mode has chi=E=q=p=0 only at its leading order; verify the next-order initial inhomogeneous state/boundary before production interpretation. Y1(t_i)=0 requires initial conditions themselves independent of eta; document and verify this assumption.

At output, evaluate the tangent gravitational Weyl transfer using actual species shear:

    W1(t,k) = Phi1(t,k) - (9*a(t)^2/(4*k^2))*S_sigma,1(t,k).

A baseline/tangent comparison must use identical physical variables and gauge; native CLASS d_m is NOT a validated galaxy overdensity when its CDM slot is repurposed to pressureful AeST.

## Predeclared single-campaign acceptance, with explicit stops

1. **Compile/source lock**: parent original CLASS, original AeST and separate quarter candidate sources unchanged except a versioned tangent feature. One fixed k=0.1 h/Mpc, fixed z=0.5 target, frozen input cosmology and both approximation schedules recorded. No GitHub Actions.
2. **Algebra + implementation identity**: independent single-RHS tests F0(0)=0, F0(u+v)=F0(u)+F0(v) (or exact Jacobian-vector), correct -a Q Bchi0/(4KB) injection, zero direct q/p stress in relaxed zero-background limit, and equation-of-motion sign/units.
3. **No source regression**: at eta=0 and tangent disabled, original CLASS transfer outputs are unchanged within a predeclared solver error; bath q/p evolved in eta=0 baseline but do not spuriously backreact. Failure = implementation BLOCK, not a physics null.
4. **Full primordial history**: single adiabatic initial curvature mode, q/p retarded no-free-mode, all photons/baryons/neutrinos included; NO z=19 bath reset. Confirm matching active hierarchy/IC and source-vector dimensions at each approximation transition.
5. **Einstein + Ward checks**: independently evaluate Hamiltonian, momentum, shear, trace and LW33 scalar-charge identities for the baseline **and tangent** with the same actual finite-k, all-species source. A PASS must include independently evolved sources, not merely identities used to reconstruct them.
6. **A posteriori numerical qualification**: rerun the exact one-k, one-z fixed state at tighter integrator tolerances or with an independent evolver and source sampling; quote absolute and relative errors of W1 and W0, not just relative tolerance flags. If |W1| is below a reliable numerical error floor, classify INCONCLUSIVE, not zero signal.
7. **Observation gate**: only if physical W1 is nonzero and error-qualified, construct the primordial-normalized physical galaxy–Weyl cross-power and DES Y3 lens-source redshift projection, with bias/IA/photo-z covariance. No claim of significance from a raw native transfer W or default d_m W product.

**Stop immediately** on mismatched class source, non-retarded primordial state, non-differentiable approximation switch, missing neutrino species, failed source constraints, or unconverged W1. Do not compensate by changing eta, choosing a different k, tuning bias or performing another blanket numerical campaign.

## What the available evidence actually demonstrates

- 14/14 first retarded source, 9/9 radiation-neutrino source, 17/17 frozen coupled bath and 21/21 Einstein all-species conserved-stress projection: all independently reproduced on researcher WSL at their stated reduced/order scopes.
- Fixed Exp sufficient local positive-root criterion: researcher source-locked PASS across 1e-8 <= a <= 0.7, but not a full global instability.
- **Now** a source-locked, independently solver-converged direct tangent and tiny response are established only in a **post-recombination dust proxy**. This is the correct method pilot, not a DES observation.
- Full CLASS tangent code, all-species primordial constraint-compatible evolution, its actual W1 and DES significance: **NOT YET AVAILABLE**.

**Decision:** proceed to ONE actual full-source tangent implementation; do not repeat the late-dust experiment, old half-vs-quarter finite differences or additional LW stage numbers.
