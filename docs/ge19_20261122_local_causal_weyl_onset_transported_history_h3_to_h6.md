# GE19 — Finite-time history-transport theorem: the local delayed Weyl onset can be h³, h⁴, h⁵ or h⁶

**22 November 2026. Original researcher WSL result audit and a physics-first extension. No new CLASS run, numerical survey, DES data fit, or parameter adjustment.**

## 1. Verified researcher evidence

The original researcher WSL [local delayed Weyl r1 JSON](../results/ge19_local_delayed_weyl_onset_20261122_r1.json) and [log](../results/ge19_local_delayed_weyl_onset_20261122_r1.log) were byte-identically archived (original Git blobs \`86264f920393735e7183cbe48a2370e8b1ef16d6\`, \`2ea68e8259dc02f6f27f6781703c8b27551ee5fb\`; original SHA-256 \`aa060fa6df27bf52c65840448ec06bd348add0a63858d0db54a8940887e6f7df\`, \`7c628730bf157fcc0a2bc00ae18c78e92fcd18d64a2cac1999c48a6ecb214b8c\`). Source locks **4/4 PASS** and symbolic reduced-Einstein checks **10/10 PASS**. The researcher's reuploaded DES Asimov r3 JSON/log are byte-identical to existing previously archived r3 and have not been duplicated.

The original valid limited classification remains **GE19_CONDITIONAL_REDUCED_ALL_SPECIES_CAUSAL_WEYL_H6_PROVED_NOT_FULL_PRIMORDIAL**. At a *finite regular* starting time \`t_i\`, with \`chi_0(t_i)=E_0(t_i)=r_j(t_i)=dot r_j(t_i)=0\` and \`D_i=dot chi_0(t_i)=Q_i c_i Delta_{A,i} !=0\`, the one-sided eta-tangent's **retarded-minus-instantaneous** history-source comparison produces
\`\`\`math
\delta_h W_1(t_i+h)=\frac{c_i k^2 Q_iD_iM_2}{5760a_i^2}h^6+O(h^7).
\`\`\`
The \`10/10\` PASS confirms algebra under these hypotheses only: it does NOT select the physical primordial mode, establish the full covariant action-to-CLASS bridge, transport the oscillator state from the cosmological past or predict DES shear.

## 2. Strictly stronger local history-transport formula

Define \`r_j=(a omega_j sqrt(w_j)/k)q_j\`, and let \`R(t):=sum_j r_j(t)\`. The *original quarter-normalized* restricted source decomposition has
\`\`\`math
B_{\rm delayed}=-R,\qquad
(\partial_\eta\dot S)_{\rm delayed}=\frac{Q}{4}R,
\qquad S=K_B E_A+(2-K_B)\chi.
\`\`\`
Make the **same restricted all-species Einstein-projected operator assumptions** as r1: fixed finite regular \`t_i,a_i,Q_i,c_i,K_{Q,i}\` at leading Taylor order, \`k>0\`, no direct ordinary-species or metric bath stress, a common eta=0 trajectory, a common initial **eta-tangent** for retarded/instant-only source-comparison solutions, and no independent comparison-source or matter tangent at the initial time. The regular metric and ordinary-fluid response enters only through the dynamically induced \`Phi\` and higher-order source feedback. Do not require the **baseline** bath \`r_{j,0}(t_i),dot r_{j,0}(t_i)\` to vanish.

Suppose the first nonzero Taylor term of the *baseline* driven retarded bath sum at that finite time is
\`\`\`math
R_0(t_i+h)=R_m h^m+O(h^{m+1}),\qquad m=0,1,2,\ldots .
\`\`\`
The leading triangular response through the actual reduced Einstein equations is:
\`\`\`math
\delta_h S_1 = \frac{Q_i R_m}{4(m+1)}h^{m+1}+O(h^{m+2}),
\`\`\`
\`\`\`math
\delta_h\varphi_1=
\frac{c_i k^2Q_iR_m}
{4a_i^2 K_{Q,i}(m+1)(m+2)}h^{m+2}+O(h^{m+3}),
\`\`\`
\`\`\`math
\boxed{
\delta_h W_1=
\frac{c_i k^2 Q_i R_m}
{8 a_i^2(m+1)(m+2)(m+3)}
h^{m+3}+O(h^{m+4}).
}\tag{H}
\`\`\`

Here the Weyl stress projector **must** be constraint-correct:
\`W=Phi−9a² S_shear/(4k²)\`; the apparently direct electric field Weyl entry cancels identically against the other action/Einstein stress terms, as independently established in the r1 10/10 proof. Ordinary species have no separate direct eta force and begin after the relevant metric response; their leading dynamically induced shear cannot change the displayed Weyl coefficient under these smooth-source assumptions. The formula is a *conditional local series* in the original reduced Einstein-projected operator, not an independently certified full physical cosmological response.

The result is independently checked by direct term-by-term integration of the local \`S -> phi -> Phi\` chain with the same \`1/4\` original source normalization. For \`m=0,1,2,3\`, the coefficients multiplying \`c_i k²Q_iR_m/a_i²\` are, respectively, \`1/48,1/192,1/480,1/960\`. In the original r1 case, the oscillator equation gives \`R_3=M_2 D_i/6\`, so Eq. (H) gives \`c_i k²Q_iD_iM_2/(5760a_i²) h^6\` **exactly**, recovering the verified WSL result.

## 3. Explicit physically distinct histories

The same original, now nonsingular bath equation
\`\`\`math
\ddot r_j+H\dot r_j+(\omega_j^2-2H^2-\dot H)r_j
=\omega_j^2 w_j\chi
\`\`\`
implies a different local Weyl onset depending on the physical earlier history of the state at \`t_i\`:

| Earliest nonzero R term | Physical situation *as a diagnostic possibility* | Restricted history-Weyl onset |
|---|---|---|
| \`R_0=sum_jr_j(t_i)\` | Earlier history already displaced the bath | \`O(h^3)\` |
| \`R_1=sum_jdot r_j(t_i)\` with \`R_0=0\` | Bath displacement canceled, retarded momentum remains | \`O(h^4)\` |
| \`R_2=M_2 chi_i/2\` with initial r/dot r=0 but chi_i != 0 | Initially unexcited auxiliary coordinates, initially strained scalar–aether | \`O(h^5)\` |
| \`R_3=M_2 dot chi_i/6\` with r/dot r=chi_i=0 | Fully relaxed starting point, source just turns on | \`O(h^6)\` |

If \`R_0=R_1=0\` due cancellations *among multiple oscillator modes*, the displayed formula for \`R_2\` in the table additionally assumes each individual \`r_j\` and \`dot r_j\` is zero; in a cancellation across modes, \`R_2\` also contains individual free oscillator terms. Similarly, a retarded *no-free-homogeneous-mode* bath transported from the actual physical past **does not imply** \`r_j(t_i)=dot r_j(t_i)=0\` at an arbitrarily chosen finite CLASS integration time. Therefore **the h⁶ law is not universal**; an artificial finite-time q/p reset can erase h³/h⁴ contributions, and setting chi_i=0 may erase h⁵. A physical primordial mode's earlier history and on-shell regularity must determine which coefficients actually occur.

**Action-degeneracy note:** at eta=0 exactly the auxiliary kinetic term is proportional to eta, so the relevant baseline bath trajectory is the *one-sided* \`eta\to0^+\` retarded choice, not an arbitrary solution of an eta=0 auxiliary Euler equation. Do not infer new physical free modes or break the stipulated no-free homogeneous mode.

## 4. Local ordinary matter/tracer response: first coupled galaxy–Weyl clue

In the same finite-regular-time source-difference system, assume separately conserved standard *pressureless baryons* and collisionless massless radiation satisfy ordinary Newtonian-gauge continuity laws, with initially equal eta-tangent state across the two compared histories and no additional direct NL0B matter force:
\`\`\`math
\dot\delta_b=-\theta_b/a+3\dot\Phi+\ldots,\qquad
\dot\delta_\gamma=-4\theta_\gamma/(3a)+4\dot\Phi+\ldots .
\`\`\`
For a metric onset \`delta_h Phi_1=F_m h^{m+3}+O(h^{m+4})\`, the induced Euler velocities begin at \`O(h^{m+4})\` and their continuity contributions are subleading. Thus, **under the stated ideal-baryon and radiation approximations**,
\`\`\`math
\boxed{
\delta_h\delta_{b,1}=3\,\delta_h\Phi_1+O(h^{m+4}),
\quad
\delta_h\delta_{\gamma,1}=4\,\delta_h\Phi_1+O(h^{m+4}).
}
\`\`\`
These are leading local Newtonian-gauge responses of specified **ordinary fluids**, not yet the physically biased galaxy density or total AeST dark-matter transfer. The AeST effective density itself already starts \`O(h^5)\` for the r1 m=3 case, whereas the baryon and Weyl responses then start \`O(h^6)\`. In particular, the galaxy tracer cannot be replaced by the AeST effective density without an explicit tracer/bias mapping. The full k/z \`P_{\delta_gW}\` derivative requires both \`T_{\delta_g,1}\` and \`T_{W,1}\`, corrected primordial statistics and nonlinear/nuisance terms.

## 5. Decision after the WSL 10/10 result

**Verified:** reduced local response is internally consistent and *not* a pure-gauge electric term; original r1 proof archives are exact. **New conditional theorem:** the local Weyl-onset time power is fixed by the actual first nonzero transported bath-history coefficient, and can be h³, h⁴, h⁵, h⁶ rather than universally h⁶.

**Still physically blocked:** full unreduced Einstein–AeST–NL0B+all ordinary species action/multiplier and scalar Ward equivalence, primordial finite-k regular growing eigenmode, physical prior history for all modes, and globally converged \`(T_delta,1,T_W,1)(k,z)\` across DES lens support. No physical \`gamma_t\` derivative, no physical 3-sigma significance (the earlier 9.84% norm threshold is merely an idealized 26-point survey comparison), **FULL_PHYSICS_GO=false; DES_detection=false**.

**Next real action:** establish original action-consistent physical first-order state at a sufficiently early initial time and **transport the retarded bath**, not another artificial finite-time reset. Then perform one physical, all-species signed matter–Weyl tangent on a preselected lens-support k,z domain, include the original quarter source and the state’s eta derivative, and only then compute DES gamma_t shape and nuisance-projected Asimov distance. **No new synthetic flat-template or local-pass-loop campaigns.**
