# GE19 — exact initial-state ambiguity of the positive bath, and a non-CDM observer sanity check

**11 November 2026. Physics-first continuation without new CLASS evolution.**  
**Result:** \`REGULAR_BATH_IC_NONUNIQUE / PURE_ADIABATIC_NO_FREE_BATH_MODE_IS_AN_EXPLICIT_ASSUMPTION / NATIVE_DM_AS_PHYSICAL_GALAXY_MATTER_BLOCK / EXISTING_BARYON_WEYL_DIAGNOSTIC_POSSIBLE\`.

This is a concrete mathematical conclusion of the **original** conservative NL0B auxiliary action plus a direct check of the original **pinned CLASS** transfer definitions. It makes no claim to an independent 3+1 production model, physical \(\partial_\eta P_{\delta W}\), or detection. Frozen original action and old v019j code remain untouched.

## 1. What the action actually determines

The original GE05/NL0B positive bath per mode, with \(\eta>0\), gives
\[
L_{\mathrm{bath},j}^{(2)}=\frac{\eta a^3}{4}
\bigg[\dot q_j^{\,2}-
\left(\omega_jq_j-\sqrt{w_j}\,\frac{k\chi}{a}\right)^2\bigg].
\]
Its Euler equation in cosmic time and the corresponding CLASS conformal-time state equation are
\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}\,\frac{k\chi}{a},
\]
\[
q_j'=p_j,\qquad p_j'=-2\mathcal H p_j-a^2\omega_j^2q_j
+a k\omega_j\sqrt{w_j}\,\chi.
\]
Both statements have already been independently symbolically verified by the researcher WSL's **15/15 exact** source-locked matrix \`results/ge19_action_to_class_scalar_matrix_20261111.json\`. The code's \`v019j\` leading \`q_j=p_j=0\` IC do not follow from those equations without an extra initial-state choice.

## 2. A direct analytic counterexample to "regularity uniquely forces q=p=0"

In the unforced early FLRW epoch let \(a(t)=a_\star t^\beta\), \(H=\beta/t\) with constant \(\omega_j>0\). Then
\[
\ddot q_j+\frac{3\beta}{t}\dot q_j+\omega_j^2q_j=0.
\]
For \(\beta>1/3\), put \(\nu=(3\beta-1)/2>0\). The **explicit normalized regular homogeneous mode**
\[
\boxed{
q_{\mathrm{reg},j}(t)=C_j\,\Gamma(1+\nu)
\left(\frac{2}{\omega_jt}\right)^\nu
J_\nu(\omega_jt)
}
\]
solves the equation exactly and has expansion
\[
q_{\mathrm{reg},j}(t)
=C_j\left[
1-\frac{\omega_j^2t^2}{4(1+\nu)}+O(t^4)
\right].
\]
An exact symbolic substitution into the ODE gives zero (independently checked for radiation and matter cases), and the series follows from the Bessel expansion.

In the early **radiation** epoch \(\beta=1/2\), \(\nu=1/4\):
\[
q_{\mathrm{reg}}=C_j[1-\omega_j^2t^2/5+O(t^4)].
\]
In the early **matter** epoch \(\beta=2/3\), \(\nu=1/2\):
\[
q_{\mathrm{reg}}=C_j[1-\omega_j^2t^2/6+O(t^4)].
\]
Both are finite, with \(\dot q_j\to0\), hence also \(p_j=q_j'=a\dot q_j\to0\). Yet the arbitrary physical *normalized* amplitude \(C_j\) need not be zero. The second independent homogeneous solution scales as \(t^{1-3\beta}\) (divergent for \(\beta>1/3\)) and can be eliminated by regularity. **Regularity eliminates one integration constant but not the other.**

This is a decisive, constructive counterexample to the frozen v019j source comment's assertion that the leading \(\chi_i=0\) *uniquely* implies \(q_j=p_j=0\). A vanishing forcing at one initial time is not a condition on the complete historical homogeneous mode.

The original covariant auxiliary variable is \(U_j=\sqrt\eta\,q_j\): the regular homogeneous physical \(U_j\) amplitude goes to zero as \(\eta\to0^+\) for fixed \(C_j\), so merely requiring this **continuous \(\eta\to0\) limit does not select \(C_j=0\)**. Strict \(\eta=0\) makes the q-variable quadratic kinetic action degenerate and cannot repair the missing initial-state selection by itself.

## 3. The exact meaning of an explicitly retarded branch

For a fixed finite initial time \(t_i\), let \(u_j,v_j\) be any independent homogeneous solutions. Define the causal Green function for
\(\mathcal D_j=\partial_t^2+3H\partial_t+\omega_j^2\):
\[
G_{R,j}(t,s)=\Theta(t-s)
\frac{u_j(s)v_j(t)-v_j(s)u_j(t)}
{u_j(s)\dot v_j(s)-\dot u_j(s)v_j(s)}.
\]
Its Wronskian satisfies \(\dot{\mathcal W}=-3H\mathcal W\), so \(\mathcal W\propto a^{-3}\). The general solution is
\[
\boxed{
q_j(t)=q_{j,h}(t)+\omega_j\sqrt{w_j}k
\int_{t_i}^t ds\,G_{R,j}(t,s)\frac{\chi(s)}{a(s)} .
}
\]
Choosing \(q_{j,h}=0\) and an integrable causal drive is the **retarded, no-free-bath-mode** branch with \(q_j(t_i)=\dot q_j(t_i)=0\). It gives a causal source-only memory representation once the initial time, initial bath state and initial scalar perturbations are frozen. It is a **distinct physical initial-state prescription**, not a consequence of regularity alone.

A *pure adiabatic cosmological initial condition* could justifiably set the independent bath isocurvature/homogeneous mode to zero, because its FLRW background field is zero. But that is an additional assumption about the primordial perturbations and the absence of a bath isocurvature spectrum; the full multi-species Einstein–AeST–NL0B early-time eigenmodes and gauge constraints have **not** been independently derived. Thus the existing CLASS candidate represents **one retarded/adiabatic-proxy sector**, not every regular cosmological perturbation of the covariant theory.

Importantly, \(B_\chi=\sum_j[w_j\chi-a\omega_j\sqrt{w_j}q_j/k]\) depends on the free \(q_{j,h}\) modes. Consequently the physical Weyl response is in principle sensitive to this initial-history choice even when the local source normalization \(\gamma=1/4\) is fixed. Do **not** fit unknown \(C_j\) to observed DES residuals and call it a theory prediction.

## 4. Why the previous native CLASS d_m-W product is not yet the DES galaxy–galaxy lensing cross power

The pinned official CLASS v077 \`source/perturbations.c\` (Git blob \`c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0\`) exports a \`d_m\` transfer that normally applies
\[
\delta_m \mapsto \delta_m+3aH\theta_m/k^2.
\]
The code comment explicitly limits that transformation to *pressureless, stable matter*. Its default input \`matter_source_in_current_gauge = no\` is active in the frozen AeST Exp test. However original \`v019\` repurposes CDM-labelled states for the **AeST effective dark component with pressure \(p_A\)**; its \`rho_m\` background split and perturbative density/velocity sums also use nonidentical bookkeeping. The result is a **concrete output-convention warning**, not an established numerical transfer discrepancy or a failure of all Einstein equations.

For a consistent set of independent matter fluids, a physical comoving density uses the **actual** \(\sum_s(\rho_s+p_s)\theta_s\) and total background density; the usual pressureless CLASS correction cannot be applied unchanged to a pressureful effective mixture without proving its relation to those definitions. A bare product \`d_m * (phi+psi)/2\` is neither \(P_{\delta W}\) nor a projected DES \(\gamma_t\) observable.

The original **native CLASS mTk** source (pinned \`source/output.c\`, Git blob \`c41d7c4dab31ddb5b26ddfbccc9a3d4dfe8993e9\`) also exports the separate \`d_b\` transfer and the metric \`phi\`, \`psi\` transfers in CLASS format. Since baryons remain minimally coupled and independently evolved in the v019 source patch, the combination
\[
\boxed{[T_{\delta_b}^{N}(k,z),\quad W(k,z)=(T_\Phi+T_\Psi)/2]}
\]
is a more clearly defined, **Newtonian-gauge, implementation-level matter–metric sanity check** than the pressureful synthetic \`d_m\`. Its use avoids the specific pressureless-comoving-total-matter output conversion, but does **NOT** make baryons interchangeable with galaxy number density, nor does it certify the full action/metric evolution or source nonlinearities.

A real DES galaxy–galaxy lensing forward model needs a separate galaxy tracer and bias/HOD prescription, observer gauge/redshift effects, primordial normalization, lens/source windows, and covariance with nuisance marginalization. Thus the native \(d_bW\) transfer-amplitude product is **not** a galaxy–Weyl cross-power or detection.

## 5. Concrete read-only reuse: no additional CLASS run

One [single read-only parser](../ge19/physics_gate/inspect_existing_baryon_weyl_20261111.py) has been committed to inspect the **already-generated three** CLASS \`mTk\` tables from \`results/ge19_action_quarter_finite_eta_r1\`. It requires the same explicit native CLASS columns \`d_b,d_m,phi,psi\`, checks the k grids, and optionally checks all previous \`d_m,\Phi,\Psi\` values **exactly** against the prior canonical \`native_transfer_comparison.npz\`. It then compares the \(k\in[0.03,0.20]\,h/{\rm Mpc}\) signed \(\Delta d_b,\Delta W\) shape to the previously reported potentially contaminated \(\Delta d_m\).

Run **only** to reuse completed stored transfer tables; the original CLASS and the candidate are not invoked, compiled or edited:
~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
python3 -u ge19/physics_gate/inspect_existing_baryon_weyl_20261111.py \
  --existing-dir results/ge19_action_quarter_finite_eta_r1 \
  --prior-npz results/ge19_action_quarter_finite_eta_r1/native_transfer_comparison.npz \
  --out results/ge19_existing_baryon_weyl_20261111.json \
  2>&1 | tee results/ge19_existing_baryon_weyl_20261111.log
~~~
The parser deliberately **refuses output overwrite**. If a native \`d_b\` column is missing, stop with the error, do not synthesize it or rerun CLASS without a new physics decision. The result is a **diagnostic**, not \(\partial_\eta P_{\delta W}\), and the script has now been run on the researcher's WSL tables; its actual log and results are recorded in section 7.

## 6. Final joint physics status and strictly bounded next decision

| Domain | Honest classification |
|---|---|
| Original GE05 / GE06 plus LW33 scalar memory source \(\gamma=1/4\) | **Restricted linear scalar algebra PASS**, conditional on original dictionary |
| Original per-node oscillator Euler and normalized source | **Restricted action PASS**, independent WSL matrix 15/15 |
| Uniqueness of \(q_j=p_j=0\) from \(\chi_i=0\) and regularity | **DISPROVED** by explicit regular homogeneous solution |
| \`q=p=0\` as chosen no-free-bath-mode/adiabatic proxy | **Well-defined conditional physical hypothesis**, not unique general initial state |
| Pressureful AeST \`d_m\` as galaxy/matter survey observer | **BLOCK**, pressureless gauge-conversion assumption unverified |
| Native \`d_b,W\` as separate minimally coupled transfer sanity check | **PERMITTED READ-ONLY**, not a GGL prediction |
| All-species action-to-CLASS, constraint propagation and true retarded galaxy–Weyl observable | **OPEN/BLOCK** |
| Claimed DES memory observation | **FALSE** |

**Decision:** Freeze the new analytic result as a principled restriction: *adiabatic / no initial bath isocurvature, fixed quarter-source physical theory*. If those assumptions are not accepted, the model has additional free initial-state parameters and cannot deliver a unique memory-only observational curve. If accepted, the next objective still must close the full all-species source/constraint observer bridge — **not** another undirected LW series or a new eta sweep. The **existing** tiny, jagged finite-\(\eta\) code response cannot be promoted to a discovery by changing the observer definition after seeing it. Any comparison is a post-evidence diagnostic and must be labeled as such.

This document preserves historical results and does not alter the frozen initial-condition patch or source parameter values.


## 7. Actual researcher WSL read-only baryon–Weyl result: physical signal **not** established

**Subsequent original WSL execution (11 November 2026):** \`GE19_EXISTING_BARYON_WEYL_PRIOR_NPZ_IDENTITY_PASS\`, \`GE19_EXISTING_BARYON_WEYL_READ_ONLY_PASS 49\`, \`GE19_OBSERVATION_READY False\`. It read exactly the three existing single-z \`mTk\` native CLASS tables and reproduced the prior \`d_m,\Phi,\Psi\` NPZ values byte-for-byte for each 147-point k grid, with no new CLASS numerics, parameter sweep, projection or observed DES data.

The original *researcher-submitted bytes* are now archived and independently fetched with exact Git-blob matches:
- [WSL diagnostic JSON](../results/ge19_existing_baryon_weyl_20261111.json): SHA-256 \`8542fa6361bd28cb50ab5288b75d1e64ff1e3077a1fd58715219fd48caafabc6\`, Git blob \`583add9d56f088a984d983f2c2d980e8844b9e1b\`, **3065 bytes**.
- [WSL runner log](../results/ge19_existing_baryon_weyl_20261111.log): SHA-256 \`f1a068a1dc12c69a230fc6915120aaed9e149c3c7e0dc8397dc121746c2a16eb\`, Git blob \`a957234f73d00a4a70584e0044be24a2802ea1af\`, **214 bytes**.
- The repeatedly uploaded independent [joint source-to-CLASS matrix](../results/ge19_action_to_class_scalar_matrix_20261111.json) remains exactly archived with blob \`5375bac561091fb3d98d4f978e2664e067f9906a\`; its [WSL log](../results/ge19_action_to_class_scalar_matrix_20261111.log) has blob \`81bbc96fcf09a17e52d3267e230f442fa86da73b\`. It is a reupload, **not a new physical verification**.

Use the previously chosen screening interval \`0.03 <= k <= 0.20 h/Mpc\`, at one \`z=0.5\` and fixed \`eta=0.01\`: 49 out of 147 common k samples. Define \`\Delta T=T_{historical gamma=1/2,eta=.01}-T_{candidate gamma=1/4,eta=.01}\`. The exported normalized difference is \`\max_k|\Delta T|/\max_{all k}|T_{candidate,eta=0}|\`, **not a pointwise fractional error**, survey SNR or \`d_b W\` cross-power.

| Field | Max absolute half-minus-quarter in 49 k window | Max difference / full-k eta0 max | Adjacent sign changes (of 48) | Simple expected factor-two response deviation: \`||S_h-2S_q||/||S_h||\` |
|---|---:|---:|---:|---:|
| Native Newtonian baryon \`d_b\` | \`0.01420085750578437\` | \`7.46579788503764e-7\` | **24/48** | **2.6375921881713253** |
| Native default \`d_m\` | \`0.019479727044199535\` | \`1.0229141494283504e-6\` | **22/48** | **1.7704231830478612** |
| Weyl potential \`W\` | \`3.159558091825332e-7\` | \`5.792008214664641e-7\` | **26/48** | **1.3739827575585906** |

The signed field differences have Pearson \`corr(\Delta d_b,\Delta W)=-0.37036638744091493\`, compared with \`corr(\Delta d_m,\Delta W)=-0.801981840903826\`. The less anticorrelated baryon response and persistent high-frequency k sign switching weaken the case that the prior default pressureless-only comoving \`d_m\` observer displayed an independently robust physical memory signature. But correlated physical acoustic transfer structure and common numerical errors can both affect these statistics; **nothing here proves the response is noise** or that \`d_m\` conversion is the unique cause. No convergence study was included.

**Stop/acceptance decision:**
- **PASS:** original source-locked joint linear scalar action-to-CLASS matrix 15/15; existing mTk-to-NPZ identity, independent minimally coupled baryon column parsed; all numerical user file hashes/provenance preserved.
- **NOT PASS:** source-normalization factor-two *response scaling*, physical error-controlled \`\partial_\eta T\`, all-species constraint-to-source mapping, cosmic IC branch uniqueness, calibrated galaxy–Weyl projected cross spectrum, DES observable/likelihood.
- Do **not** compute a DES significance, publish a memory detection, modify old \`d_m\` data in hindsight, or select a preferred scaling by fitting survey residuals. The result is **\`IMPLEMENTED_NATIVE_TRANSFER_JAGGED_AND_NOT_PHYSICALLY_RESOLVED\`**.
- The next valid activity is **one unified full physical observer/equation acceptance**, not additional unmotivated CLASS runs or symbolic microtests. The separate \`gamma=1/4\` candidate and the conditional no-initial-free-bath-mode sector remain the only fixed model assumptions permitted for a *future* error-controlled survey prediction.
