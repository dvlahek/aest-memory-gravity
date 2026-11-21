# GE19 — Researcher WSL mixed-order 42/42 and corrected F3 source-lock repair

**2026-11-21, immutable checkpoint.** Two prior WSL radiation NLO artifacts were reuploaded byte-exactly; the previously archived reporter original 37/37 keeps one known vacuous **k^4** octupole coefficient gate. The genuinely mixed **O(y_m (k tau)^2)** sourced Einstein–Boltzmann proxy ran successfully in researcher WSL and has now been archived.

## Original 42-gate output

- [Researcher WSL JSON](../results/ge19_coupled_mixed_y_k2_20261121_r1.json), original Git blob \`872b78ae83e4d399790d8f27fc6a83fae4cb0c6f\`, SHA-256 \`41982bfb8c212f372856c1bd61d233ada83dc2e6f3a32719933ad926882f54b5\`.
- [Researcher WSL log](../results/ge19_coupled_mixed_y_k2_20261121_r1.log), original Git blob \`6c6215e757839c532d72345df65a0231d7f8c354\`, SHA-256 \`54058374ee8136e5a3ff1c9819250b2a99a5684464f37c92be40c32651fde439\`.
- \`GE19_MIXED_FINITE_K_SOURCE_LOCKS_PASS 3\`, \`GE19_COUPLED_MIXED_FINITE_K_SYMBOLIC_PASS 42\`, \`GE19_FULL_PHYSICS_GO False\`, **all 42 coefficient-level symbolic tests true**.

For a *pressureless proxy* AeST-like species, coupled tight-coupled photon–baryon, free massless neutrino and total Einstein equations, with \`y_m=(rho_b+rho_A)/rho_r\` and \`x=k tau\`, all terms through \`O(y_m x²)\` pass the tested coefficient residuals. The density source is
\`\`\`math
\Delta_A=-\frac{15+4R_\nu}{40}\Psi_0 x²
+\frac{15+4R_\nu}{200}\Psi_0 y_m x²+\cdots
=-\frac{15+4R_\nu}{40}\Psi_0 x²(1-y_m/5)+\cdots.
\`\`\`
The symbolic beta \`rho_b/(rho_A+rho_b)\` cancels in the mixed coefficient of \`Delta_A\` and the metric potentials. This remains a **proxy**. The Exp scalar/aether state, full action Ward, nonzero-pressure perturbation limit, retarded primordial auxiliary initial history, physical Weyl transfer, and DES are NOT certified. The 42 gates are coefficient identities within a set of linked equations, not 42 statistically independent tests of physical realism.

## Corrected octupole / causal onset test: recorded source-lock typo and repair

The researcher supplied an initial failed log, archived intact as [GE19 corrected F3 source-lock failure log](../results/ge19_corrected_f3_causal_onset_20261121_r1_FAIL_SOURCE_LOCK.log), original Git blob \`5d75550b752a0cdaea6f1926abf21c4dfbc03a3b\`, SHA-256 \`3e4cb72c85123c4b7ee0a1c119b392ecf62270bdf80f812a2b9bfc67b2305de4\`. **Cause is not physics:** the lock on \`ge19/physics_gate/action_to_class_scalar_matrix_20261111.py\` incorrectly expected 39-character \`c90a3de0b71d0ef4e6664512e6e247cd44e27dd\`, while the actual immutable blob is 40-character \`c90a3de0b71d0ef4e6664512e6e247cd44e27ddc\`. Patched **only this lock** in [corrected F3 and exact cubic onset script](../ge19/physics_gate/corrected_octupole_and_causal_memory_onset_20261121.py), commit \`109778a043239dcd5252a320488ef933e4cf03bc\`. The original failed log is retained rather than silently replaced.

A separate direct SymPy evaluation of the source-onset identities reconfirmed
\`\`\`math
q_j''(t_i)=0,\quad
q_j'''(t_i)=\omega_j\sqrt{w_j}kQ_i c_i\Delta_{A,i}/a_i,\quad
B_{\chi,\mathrm{delayed}}=-Q_i c_i\Delta_{A,i}
\left(\sum_jw_j\omega_j²\right)(t-t_i)^3/6+O((t-t_i)^4).
\`\`\`
Here the selected **finite-time zero bath and zero scalar state are assumptions**, not derived primordial physical data; this local result is **not** a W1 physical certification. The corrected script tests actual neutrino F3 k³ residual and two fail-closed negative controls rather than the previous vacuous k⁴ gate. Canonical researcher WSL corrected run is pending; do not imply a new researcher PASS yet.

**Scientific decision:** The mixed radiation+proxy matter source at \`O(y_m x²)\` is closed. No need for more GR/CLASS fitting at this order. The outstanding P0 is one covariant/action-derived, finite-k, Ward-compatible initial vector for \`X, E_A,\delta\phi,q_j,\dot q_j\` and total Einstein+Boltzmann constraints, with a genuinely propagated no-free-mode retarded history, then recompute and bound the delayed Weyl tangent. \`FULL_PHYSICS_GO = false\`; \`DES_detection = false\`.
