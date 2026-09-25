# GE19 H4F3d2 — valid dust and bath parent Euler-current compiler

## Classification and scientific boundary

`GE19_H4F3D2_DUST_BATH_PARENT_EULER_CURRENT_COMPILER_PASS`.

This is the valid **restricted action/parent analytic gate** under the
already frozen H4F3d full corrected-parent structural preregistration.
It derives the original frozen GE07 dust and NL0B GE05 longitudinal
per-node parent Euler currents and their first-order FLRW coefficients,
then checks their exact signed physical mixed H4 Ward parent products.

It is **not** a full all-sector H4 Noether identity or an actual
corrected-parent residual evaluation. No H4F3b physical NPZ was
re-evaluated by this CI, no original Z11 binary was manufactured,
no structural tolerance was fitted and no H4/Z21 solver ran.

## Exact versioned provenance

- predata: `ge19/h4f3d2_predata_dust_bath_parent_euler_currents.json`,
  blob `6e9f83fc7f245bfedb82db53afd96ab2ba8616db`;
- actual source-bound compiler:
  `ge19/h4f3d2_dust_bath_parent_euler_currents.py`,
  blob `42b2405759402195ffb371056d9e48b70dcded71`;
- workflow:
  `.github/workflows/ge19-h4f3d2-dust-bath-euler-currents.yml`,
  blob `1ad91e73519871f6ffdeb78e0128b4838159a4d6`;
- dedicated successful Actions run `36103744644`, job
  `107971628320`, conclusion `success`;
- terminal marker:
  `GE19_H4F3D2_DUST_BATH_PARENT_EULER_COMPILER_PASS`;
- artifact name `ge19_h4f3d2_dust_bath_parent_euler_currents`,
  artifact ID `10849674680`;
- JSON `results/ge19_h4f3d2_dust_bath_parent_euler_currents.json`,
  SHA-256
  `60ff08c7ed0e47e8e52184d56c1ef329b834f1868f45e16aa8e424186df86c36`.

The CI compiled only the pinned symbolic assignment regions from the
original GE07 and GE05 source generators. It did not import their
module-level output-producing campaigns. Every frozen Git blob,
dust/bath exact analytic gate, mixed Ward coefficient and independent
manufactured directional check passed.

## Preexecution correction (no post-hoc science adjustment)

The first newly authored predata had one incorrect formula:
`E_rho10=2 a^3 rho0 (dTt-dN)`. The dust density is a
Lagrange multiplier in the frozen GE07 action. Its Euler equation is
the derivative with respect to that multiplier and cannot contain
an additional `rho0`:

`E_rho=N L R^2 (W^2-V^2-1)`;

`E_rho10=2 a^3 (dTt-dN)`.

The preregistration was explicitly corrected in commit
`2d57f1cbb7574ff6218ced4c0ec904d876eb76ed`
**before any implementation test or science data**. The initial
predata commit `7cb9e644a307fc4c7fbbbebc418da697233eb566`
is retained in Git history. The final pinned predata records both
formulas and the reason. No source coefficient, physical model,
parent input or science threshold was fitted.

A manufactured zero-derivative test was also set to its appropriate
absolute-error gate before first CI; it does not relax the exact
symbolic gates or compare any actual GE19 parent arrays.

## Derived source-bound Euler parents

The frozen dust action is

`L_d=N L R^2 rho [W^2-(T_x/L)^2-1]`,
`W=(T_t-b T_x)/N`.

Its original off-shell Euler inputs are

`E_T=-partial_t J_T^t-partial_x J_T^x`,

`J_T^t=2 L R^2 rho W`,

`J_T^x=-2 L R^2 rho b W-2 N R^2 rho T_x/L`,

and `E_rho=N L R^2[W^2-(T_x/L)^2-1]`.

The exact FLRW first-order dust currents and independent L/shift
Euler rows are tested from the original action. The homogeneous
`E_T00=0` statement is **conditional on**
`partial_t(a^3 rho0)=0`; `E_rho00=0`
requires the dust normalization shell.

For each independent frozen GE05 per-node scalar-longitudinal bath,

`L_q=N L R^2/4 [A(q)^2-(omega q-sqrt(w) X_phi)^2]`,

`J_q^t=N L R^2 A(q) A^t/2`,

`J_q^x=N L R^2 A(q) A^x/2`,

`E_q=-N L R^2 omega(omega q-sqrt(w) X_phi)/2
      -partial_t J_q^t-partial_x J_q^x`.

At the homogeneous frozen q=0, X_phi=0 FLRW point,
`J_q,t10=a^3 delta q_t/2`,
`J_q,x10=0`, and the source-bound
first-order local q Euler term is
`-a^3 omega[omega delta q-sqrt(w)(Q delta u+delta phi_x/a)]/2`.
This is the **raw per-node action** result; a later
all-sector audit must still respect the separately frozen
eta-rescaled bath convention.

The signed physical mixed Ward parent coefficient is
`E_i00 F_i21,x+2 E_i10 F_i11,x+2 E_i11 F_i10,x`
for each dust T, rho and individual q node, before
summing bath nodes. No `E_i20` term is inferred from
an eta-independent homogeneous background. The
previously frozen H4F2b complete mixed template and
H4F3d1 canonical operator signs remain unchanged.

## Open next work

Independently derive the remaining Einstein/analytic AeST,
Y and complete dust/bath metric/aether/scalar parent Euler
and action boundary contributions, keeping all lower-order
off-shell residuals and the original GE19 row projection.
Then preregister the first **actual corrected-parent**
source+canonical-operator+all-parent/boundary common-grid
structural test with an independently derived FD4/FD8
truncation tolerance.

The actual H4F3b NPZ and original certified Z11 binary were
present on the user's prior local scientific machine, but
are **not** available from this GitHub Actions checkout.
The existing valid H4F3b actual-source result stays frozen;
no manufactured replacement may be relabelled as physical.

Original Repair37 H4/Z21 science FAIL and Repair38--44
diagnostics remain immutable. Original H4 active-shift
target `1e-6` and matched temporal order `>=2.5`
remain fixed.

**Full H4 Noether NOT CERTIFIED. Z21 NOT CERTIFIED;
lensing blocked.**
