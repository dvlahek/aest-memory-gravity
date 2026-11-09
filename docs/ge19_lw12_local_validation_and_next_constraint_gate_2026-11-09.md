# GE19 LW12 — original local WSL result validated, geometric subblock closed

Date: 2026-11-09. **Actual researcher WSL source result:** `GE19_LW12_EXACT_AEST_PHI_DIRECT_JACOBIAN_BLOCK_PASS_FULL_AEFF_OPEN`. The source result JSON is stored **unchanged** at [results/ge19_lw12_aest_metric_partial_jacobian_20261109.json](../results/ge19_lw12_aest_metric_partial_jacobian_20261109.json), Git commit `428cd02b97ccc0761975e8a4d9d9671c60ced4eb`, SHA-256 `fdec5a67d0ba5a7f22fa9b59e22116b18e6b94dce8e18578a526c36164d0b00f`, 4071 bytes. Read-back from GitHub matched the original file byte-for-byte.

## Validation

- All **eight canonical LW12 symbolic gates PASS**. Frozen corrected r1 predata blob `4490f60447ffc21204cad5763097a0fbc62c5904` matched.
- Original LW10 local input SHA256 `10e8dd7f3eaa988a48966ce7892e1da653f4215c4ce09499a4c62981cf350851` matched and original patched CLASS base commit remained `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- The complete 5×5 **partial** direct Jacobian for `(delta_A,theta_A,alpha_A,E_A,Phi)` was produced. The 5×2 `S,M` stress-input matrix is `[[3Hconf*g,3g],[-k2,0],[a,0],[0,0],[Hconf,1]]` in this state order, with `g=1+w_A`. Both input columns are nonzero.
- Exact impulse-source contractions: `C e_E=0`, `C A_AA e_E=0`, `C A_AA² e_E=K_B*c_a²*k²/2` and `G_WE~(K_B*c_a²*k²/4)Delta²` **conditional on the previously stated smooth-regime shear and constraint assumptions**. The formal memory-source local product is `-aQ*c_a²*k²*Delta²*Braw/8`. These agree algebraically with the previous [independent LW12 symbolic replay](../results/ge19_lw12_aest_metric_partial_jacobian_symbolic_replay_20261109.json) and LW11 formula.
- The separately uploaded original LW10 copy and LW11/LW12 symbolic replay preserve prior classifications; they are controls, not new experimental evidence. No original input was retuned.

## What this does *not* establish

`global_Aeff_closed=false`, `other_species_A_AO_A_OA_A_OO_assembled=false`, `Einstein_Hamiltonian_Noether_constraint_propagation_certified=false`, `global_retarded_G_WE_evaluated=false`, `two_physical_history_pair_certified=false`, `DES_ACT_detection=false`. The five-variable equations are an exact frozen AeST+Phi **partial block** when all other-species state perturbations are held fixed, not a complete model with photons, baryons, neutrinos and approximation transitions. Further, physical bath B is not freely controllable like a mathematical delta impulse.

**Scientific next step:** before a numerically constructed full Green, derive the exact *total-fluid* linear Newtonian-gauge Hamiltonian constraint propagation identity under standard GR background/Friedmann and conserved aggregate stress, and then test whether the actual modified CLASS branches and physical AeST memory system satisfy its hypotheses. A conditional analytic identity is necessary but **not** a full Ward certification.

Stop repeated source-time grid sweeps, H4 rescue numerics and posthoc DES fitting. LW03 radial FAIL, LW05 full LOS BLOCK, LW08 differential source uncertainty and H4/Z21 open remain intact.
