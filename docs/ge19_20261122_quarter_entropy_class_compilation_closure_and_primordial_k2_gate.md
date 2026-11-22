# GE19 — isolated quarter/enthalpy CLASS compile checkpoint: link command reached, physical primordial mode remains blocked

**Date: 2026-11-22.** Source of truth is the original researcher's uploaded [C-only CLASS compile log](../results/ge19_quarter_entropy_class_compile_20261122_r1.log) (SHA-256 `2ddea1bfdd27efc92f9491ca311fdb9ca4c3d4a3203a3089001ac0501871f0c9`; **byte-exact Git blob** `251c75d978164d986e61712c5c90b99895c78f96`). The original researcher reuploaded source-stage JSON/log and both are byte-identical to the previously archived originals (SHA-256 `ce00b0d8678d6e29792061a79cf5b1b90d5cbfe153b14370fd811f80f6eed6a4`, `d7aa4eb84e5ccce6e919143330600cd481069325ab76f1eb980022d75890654f`).

## Exact engineering evidence

- Previous source stage `GE19_ISOLATED_CLASS_SOURCE_STAGE_PASS 3`; action-quarter `E_rhs -=0.25 Q Bchi` was **already present** in historical source; only two AeST enthalpy density/gauge changes were made in the candidate. Source hash `c41ad4cad9cc18d658f80841137094349657df6ac5d68fd3c0c75cfbbe092073`, candidate `3aa1dde9eaf55a10a43f39192132fb606d4190ff3bb4b0490915d96870186b81`.
- Researcher compile log invokes `gcc/g++` for all required modules, including `source/aest_memory.c`, `source/perturbations.c`, `source/primordial.c`, standard photon/baryon/neutrino CLASS modules, and finishes with the **link command** `g++ ... -o class ... -lm`. There is **no `error:`, linker failure or make failure** shown in the 63-line original log.
- One compiler warning in **unmodified upstream** `source/distortions.c:1948`: possible snprintf format truncation. It is not an AeST or memory-source warning.
- The compile log itself **does not record the process EXIT code, an `ls`/binary ELF check or a physical CLASS execution**. Strict status is `CLASS_LINK_COMMAND_REACHED_WITH_NO_ERROR_IN_LOG` rather than a verified full simulator run.
- The source-stage JSON's `class_compiled=false` is a **historical status at the moment of staging**, not contradictory evidence about the later compiler log; preserve it unchanged.

## What the two leading initial-condition fixes *actually* prove

CLASS's pinned original adiabatic synchronous initialisation (CDM treated as effective AeST density), before the repair, is `delta_c^S=(3/4)delta_gamma^S`, followed by the Newtonian gauge density transform `delta_c^N=delta_c^S-3 mathcal H alpha`. Corrected action-consistent AeST leading adiabatic enthalpy form:

```math
delta_A^S=(1+w_A)rac34delta_gamma^S,qquad
delta_A^N=delta_A^S-3(1+w_A)mathcal Halpha.
```

Because photons transform `delta_gamma^N=delta_gamma^S-4mathcal H alpha`, an exact leading identity follows:

```math
oxed{rac{delta_A^N}{1+w_A}=rac34,delta_gamma^N}
```

This cancels the *spurious leading AeST–photon relative entropy* in Newtonian gauge. It is a **necessary** regular/adabatic condition, not a sufficient full finite-k physical mode.

For the frozen Exp parameters, earlier source-verified background bound `0<=w_A<5e-14` implies the *relative leading enthalpy correction itself* is only order `10^{-14}`, for fixed nonvanishing leading state. **Do not infer smallness of the full physical memory response**: the finite-k `X,S` oscillator/metric system can have coefficients enhanced by pressure, k, and constraint cancellations; the present change does not constrain those terms. Thus neither large empirical progress nor a new detection can honestly be claimed from the now successful build alone.

## Decision: close engineering branch; next single physics calculation

The **only remaining first blocker** is a genuine action-consistent `O(k²)` growing-state coefficient solve with full Einstein Hamiltonian/momentum/shear and photon–baryon–neutrino hierarchy in the *actual* expanding Exp background. In particular:

1. Solve the **same** primordial regular (adiabatic, no isocurvature) eigenvector, including `X_2=chi/(Qk²)`, `S_2=(K_BE_A+(2-K_B)chi)/k²`, and ordinary species density/velocity/quadrupole at matched orders; do not independently prescribe `Delta_{A,2}`, drop the coupled metric backreaction or use fixed radiation as physical.
2. Require *both* original scalar current/Ward propagation and independent Einstein constraints; reject an arbitrary homogeneous `X_2` or `E_2` selection that does not satisfy physical-past regularity.
3. Determine the baseline `chi_0(k,t)` and its one-sided eta-tangent initial-state contribution. Only then transport each oscillator from its actual physical past, compute `(q_i,p_i)` with `p=dq/dtau`, and evolve the original quarter-force physically to yield full `T_{delta_g,1}(k,z),T_{W,1}(k,z)`.
4. Project that signed cross-power through the frozen DES Y3 MagLim4×Source4/3 observer. No residual-based tuning, flat amplitude proxies, or new arbitrary finite-time resets.

**No physical CLASS/DES simulation is authorized by this compile milestone alone**; additional code to complete the (k²) primordial mode is still required. One read-only binary check can confirm compilation without running a cosmology:

```bash
CAND="$HOME/GE19_CLASS_QUARTER_ENTHALPY_20261122"
test -x "$CAND/class" && file "$CAND/class" && sha256sum "$CAND/class"
```

**Labels:** `SOURCE_STAGE_GO=true`; `CLASS_LINK_COMMAND_REACHED_NO_ERRORS_IN_LOG=true`; `BINARY_EXISTENCE_UNVERIFIED_IN_UPLOAD=true`; `FULL_PHYSICS_GO=false`; `DES_detection=false`.

## Researcher WSL executable confirmation — 2026-11-22

The researcher subsequently ran a direct **read-only** executable existence and format test in WSL for the exact isolated candidate:

```text
/home/dino/GE19_CLASS_QUARTER_ENTHALPY_20261122/class: ELF 64-bit LSB pie executable, x86-64, version 1 (GNU/Linux), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=d86c97359205ee6686e6a2beaa019f12a3dbdd5f, for GNU/Linux 3.2.0, with debug_info, not stripped
9b63ca76f1b308f31d78cfea3cf65c097f4d70eb55582188b7e587512a8230b9  /home/dino/GE19_CLASS_QUARTER_ENTHALPY_20261122/class
EXIT=0
```

This **supersedes the earlier compile-status uncertainty**: the researcher explicitly confirmed a present executable ELF file with an executable permission check and `EXIT=0`, uniquely fingerprinted by SHA-256 `9b63ca76f1b308f31d78cfea3cf65c097f4d70eb55582188b7e587512a8230b9`. Status: **CLASS_EXECUTABLE_BUILD_CONFIRMED**. Note that `file`/checksum validation does not execute cosmological evolution, test the primordial perturbations, or evaluate gravitational memory: **CLASS_PHYSICAL_EVOLUTION_NOT_RUN, FULL_PHYSICS_GO=false, DES_detection=false.**

The next and only scientifically material gate remains the action-consistent finite-k growing-mode initial-value problem with original quarter source and physically retarded prior-history-selected q/p. No recompilation or further engineering check is warranted solely from this success.
