# GE19 H4F3d15a — original GE05 clock-consistent conditional R1 audit

**Status:** Exact original-action **symbolic** clock identity and synthetic signed-source/envelope tests PASS locally. The original physical R1 calculation has **not** run in this package. Continuous original H1 drive `Xtrue(x)`, continuous GE05 bath on-shell, all-time error enclosure, complete action Ward, `Z21` and lensing remain OPEN.

## Why D15 needs a clock amendment

The original Repair24 R1 step solves `dz/ds=v`, `dv/ds=-3*hmid*v-r²(z-Xlin)` with `s=t/tau`, `hmid=tau*sqrt(H_i H_{i+1})`, `dx/ds=hmid` and original affine-in-step drive. The physical background satisfies `x=ln(a)` and `dx/ds=tau*H_true(x)` instead. The original D13/D14 signed FD4 and one-sided interval bath outputs **must remain immutable**, but their internal-step time derivative `v/tau` cannot automatically be used as the physical time derivative of the x-embedded original R1 solution.

For the original frozen step regarded as the field `z_step(x)`, its true background physical derivative is `dz_step/dt=gamma*v_step/tau`, with `gamma=tau*H_true(x)/hmid`. A direct original GE05 action calculation gives

```math
R_{\rm GE05}[z_{\rm step}]
=\frac{d}{dt}\left(a^3\frac{dz_{\rm step}}{dt}\right)
+a^3\left(\frac r\tau\right)^2(z_{\rm step}-X_{\rm true})
=a^3\left(\frac r\tau\right)^2\left[(1-\gamma^2)(z_{\rm step}-X_{\rm lin})+(X_{\rm lin}-X_{\rm true})\right]
+\frac{a^3\gamma H_x}{\tau}v_{\rm step}.
```

The first and third terms on the right are the **known clock component** once original Repair13 action-consistent `H_true(x),H_x(x)` and the original R1 `z,v` are supplied. The original internal-clock D15 predata identity and this x-embedded physical-clock identity are not interchangeable. The `Xlin-Xtrue` term is an **unknown original H1 continuous-drive discrepancy** until `Xtrue(x)` is independently reconstructed or enclosed by the source-locked original H1 equations. This equation does **not** assert the exact continuous bath field equals the frozen R1 field; a separate stability/propagation error is still needed.

At sampled points, original `E_q10=-sqrt(w)/(2omega)*R` and original `qx10=sqrt(w)/omega*(i*m*kfund)z` yield the original signed `+4 sum E_q10 qx10` convolution for the frozen six positive and conjugate negative modes, `m0..40`. The additional nonnegative `U_X(m,t)` is the original absolute-sum source-node and signed-mode-pair coefficient such that `|W_drive(m,t)| <= U_X(m,t) max_i |Xlin_i(t)-Xtrue_i(t)|` **at that sampled time**. The coefficient is not an absolute error bar unless the missing `Xtrue` envelope is supplied.

The H(x) source is **not fitted**: original Repair13 Friedmann `H²=(QKQ-K)/3+C/a³+rho_lambda`, conserved `I0=a³ KQ`, original stable positive Exp branch, and `H_x=(-Q KQ-3C/a³)/(2H)`. Code checks the recovered original H(x) against all original Repair13 knots and source-locked constant Lambda. Gauss-8 and Gauss-16 estimates of `∫dx/(tau H(x))` are compared against the R1 interval `Delta x / hmid` to report the actual background **clock slip**. Their numerical agreement is *not* a rigorous quadrature error interval.

## Original GE05 internal-interface distribution (D15a1 prereg amendment)

The x-embedded original R1 solution is continuous in `z` at internal interval knots, but its **physical derivative** `z_t=gamma*v/tau` can jump because the frozen `hmid` is different on the intervals to the left and right. At every original internal knot `i=1,...,Nt-2`, the original action current has the exact jump

```math
\Delta J_{z,i}=\frac{a_i^3 v_i}{\tau}\left(\frac{\tau H_i}{h_{{\rm mid},i}}-\frac{\tau H_i}{h_{{\rm mid},i-1}}\right).
```

Therefore the original `d_t J_z` has a distributional `Delta J_{z,i} delta(t-t_i)` contribution, and `E_q10` has the source-normalized impulse coefficient `-sqrt(w_j)/(2 omega_j)*Delta J_{z,i}`. D15a **separately archives** the signed original bath `+4 E_q10 qx10` impulse coefficient and its noncancelling unsigned source-node/mode-pair envelope. This is an interface *distribution*, not an ordinary sampled residual. Its knot-vector Euclidean norm cannot be added to the smooth-time W norm. It does not license an impulsive physical bath source, nor does it settle the external action boundary conditions. The D15a1 prereg amendment was written **before actual original D15a physical execution**, with prior D15a predata and source SHA locked.

## Physical scope, preregistration and tests

The preregistered local physical driver uses original `C_min/C_star/C_max × Nt128/Nt64 × Nq2048/Nq1024`, original Repair26 R1 history, original certified H3F/H3G/Z11/Repair13 and original D13/D14 actual JSON/NPZ SHA locks, with collocation fractions `theta=0,0.5,1`. It reconstructs exactly the frozen original R1 state at each point using the pinned original Repair24 propagator and preserves all original bath nodes. Original D13 sampled signed W and D13/D14 phases must reproduce before any new output is accepted. Both endpoints and the midpoint are *samples*, not a continuous interval supremum. The physical driver also retains original GE05 internal interface distributions in distinct arrays, is no-overwrite and preserves original Repair37 SCIENCE_FAIL and original D10 FAIL.

Local synthetic validation covers the exact SymPy identity, three deliberately wrong identities, original signed +/- mode-pair conservative envelopes, a nonzero complex drive-defect control, the constant-H exact-zero control, the original Exp action H/Hx derivative against independent numerical differentiation, a deliberately wrong Lambda negative control, and clock/step helper controls. These checks do **not** imply the original local R1 parent was loaded or executed here.

## Frozen new artifact SHA-256

| New file | SHA-256 |
| --- | --- |
| `ge19/h4f3d15a_predata_original_GE05_clock_consistent_conditional_collocation.json` | `c5cb22394dc8eabf12c9fe8d5f6acd57a24d90f356976122864723ec73513745` |
| `ge19/h4f3d15a_original_GE05_clock_embedded_source.py` | `14da31797282fb7959c44793f04751f1dd0ff25765424e566ca6015e759a82ae` |
| `ge19/h4f3d15a_actual_original_R1_clock_conditional.py` | `7006c5afc9cea07ee2d076ea518ad81d0722c5f19236e73d34f4f8818c1496ec` |
| `ge19/h4f3d15a_static_clock_source_test.py` | `0a313f7fc4e49e56236e8673e58c523607b6c6ca309df6e22668b5a71947de21` |
| `ge19/run_local_h4f3d15a_original_GE05_clock_conditional.sh` | `c1852131294ab39aa53808db39998546daa8d9b5d7158f7d844f70ef6a4d444c` |
| `ge19/h4f3d15a1_predata_original_GE05_interface_current_jump.json` | `da56f2c42e11ce480ee72a888f725d422c71a2e7a3c2c19d8b19cabda752874c` |
| `ge19/h4f3d15a1_original_GE05_interface_current_jump.py` | `d5e55055348cfeb9462d566d436e91da563d77c7b3f6d36b914a73c7711cce2c` |
| `ge19/h4f3d15a1_static_interface_test.py` | `e8fc7f30203acc75c271f1187fa930a4c3cd7a51500ff259fa2a1298cd515add` |

The release bundle carries these as **new files only** and also includes a source-locked GitHub Actions static workflow. Unpack into the repository root on branch `physics-first-gravitational-elasticity`; it does not replace historical D13/D14/Repair37 sources.

```bash
cd ~/aest-memory-gravity
git checkout physics-first-gravitational-elasticity
git pull --ff-only
# Unpack the D15a ZIP into this repository root first.
source .venv/bin/activate
set -o pipefail
bash ge19/run_local_h4f3d15a_original_GE05_clock_conditional.sh \
  2>&1 | tee results/ge19_H4F3D15A_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Send actual D15a JSON/NPZ, FULL log and LOCAL runner log for independent physical audit. **Do not infer** original continuous GE05 bath on-shell, all-sector H4 Noether, particular reduced `Z21` certification or lensing until original `Xtrue`, state-propagation/time/quadrature and original complete action boundary are independently handled. No observational tuning.
