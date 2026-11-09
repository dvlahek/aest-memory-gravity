# GE19 G2C — NL0C Y action and the direct mixed H4 spatial Ward at zero gradient

**Date:** 2026-11-09. Branch: \`physics-first-gravitational-elasticity\`. **Analytical theorem in the original frozen reduced action, not physical all-parent H4 certification.**

**New executable proof:** \`ge19/h4f3d_g2c_y_action_mixed_ward_zero_set.py\` (commit \`d8b1cdacd506c164b3c9790ecc2729c1bcd10ca5\`). A separately executed local 31/31 SymPy self-test based on the original GE06 longitudinal invariant and frozen NL0C/Stage E formula passed; the source Git-blob lock portion of the committed program has **not yet been executed on researcher's WSL**. The script checks source blobs against **current file identity, not branch HEAD pins**, and does not run an H4 ODE.

## 1. The original frozen Y action, without a new interpolation function

Frozen NL0C on the weak-field small-gradient branch:

\`\`\`text
Y = X_mu X^mu ;    J(Y) = 2*Y^(3/2)/[3(1+beta0)a0].
L_Y = -(2-KB) sqrt(-g) J(Y).
\`\`\`

In the original plane-symmetric scalar-longitudinal reduced action, the aether-orthogonal gradient has one spatial orthonormal component

\`\`\`text
X = sinh(u)*(phi_t-b phi_chi)/N + cosh(u)*phi_chi/L,
V = N L R^2,
lambda = 2*(2-KB)/[3*(1+beta0)*a0],
L_Y = -lambda V |X|^3.
\`\`\`

This is the **existing** NL0C action, and the original Stage E coefficient is \`kappa=3lambda\`. Do not promote a different Y interpolation or add any source correction.

## 2. Exact off-shell spatial diffeomorphism, including shift connection

For \`xi(t,chi)\`, the original field variables obey

\`\`\`text
delta f = xi f_chi   (scalar f=N,R,u,phi,...),
delta L = xi L_chi+L xi_chi,
delta b = xi b_chi+xi_t-b xi_chi,
delta phi_t = xi phi_tchi+xi_t phi_chi,
delta phi_chi = xi phi_chichi+xi_chi phi_chi.
\`\`\`

The expression for \`X\` is an exact spatial scalar and \`V\` is a weight-one density. Since \`|X|^3\` is \(C^2\) (though not \(C^3\)) at \`X=0\`, its first variation is \`delta |X|^3=3X|X|delta X\`, also at the zero set. Hence for arbitrary fields, without invoking their equations of motion,

\`\`\`text
delta L_Y = d_chi(xi L_Y).                                (1)
\`\`\`

The original Y action therefore preserves the spatial Noether identity; it does **not** create a new symmetry-breaking shift source. The program has negative controls for an incorrect shift or scalar time-jet transformation.

## 3. The Y H3/H4 Euler source is confined to the aether and scalar

On frozen spatially homogeneous FLRW \`N=1, L=R=a, b=u=0, phi_t=Q, phi_chi=0\`, one has \`X00=0\`. The perturbative first gradient is

\`\`\`text
X = epsilon (g10+eta*g11)+O(epsilon^2),
g10=Q u10 + phi10_chi/a,
g11=Q u11 + phi11_chi/a.
\`\`\`

At the FLRW background, \`partial_u X=Q\`, \`partial_phi_chi X=1/a\`, while \`partial_b X=partial_L X=partial_N X=partial_phi_t X=0\`. The original perturbative orders are:

\`\`\`text
E_u,Y     = O(epsilon^2)  [generically nonzero]
E_phi,Y   = O(epsilon^2)  [generically nonzero]
E_N,Y     = O(epsilon^3)
E_L,Y     = O(epsilon^3)
E_R,Y     = O(epsilon^3)
E_b,Y     = O(epsilon^4)
\`\`\`

because the Y Lagrangian is cubic and \`partial_b X=O(epsilon^2)\`, \`partial_L X=O(epsilon)\`. Therefore \`-2 E_Y2\` yields exactly the frozen Stage E H3 source

\`\`\`text
S_u,H3,Y   = +6 lambda a^3 Q (g10 |g10|)
S_phi,H3,Y = -6 lambda a^2 d_chi(g10 |g10|).
\`\`\`

For the fixed background and \`beta0\`, the mixed \`eta\` tangent \`D[g|g|](h)=2|g|h\` gives the **original frozen Stage E H4** source

\`\`\`text
S_u,H4,Y   = +12 lambda a^3 Q |g10|g11
S_phi,H4,Y = -12 lambda a^2 d_chi(|g10|g11).
\`\`\`

The **direct H4 Y source rows for shift, isotropic, anisotropy, dust, lapse are exactly zero in this branch**, as independently confirmed by the Stage E source implementation: \`main[2]\` and \`main[3]\` are the only nonzero direct Y rows; the entire 2-row constraint array remains zero. This is direct-source sparsity, **not** a claim that Y has no effect on the coupled H4 solution or full mixed action.

## 4. Crucial additional conclusion: direct Y contribution to *mixed spatial Ward* is zero

The spatial action Noether identity is

\`\`\`text
W = sum_i E_i d_chi F_i - d_chi(L E_L - b E_b) - d_t E_b = 0.
\`\`\`

On spatially homogeneous FLRW, \`d_chi F_i00=0\`. For Y alone, \`E_u,E_phi=O(epsilon^2)\` multiply \`d_chi u,d_chi phi=O(epsilon)\`, while \`E_L=O(epsilon^3)\`, \`E_b=O(epsilon^4)\`. Hence

\`\`\`text
[d_eta d_epsilon^2 W_Y]_(epsilon=eta=0+) = 0.             (2)
\`\`\`

This is an **off-shell order-counting theorem for Y's DIRECT sector** and is fully consistent with original D12R7/D12R8 source routing. It does not imply \`W_total=0\` for actual truncated H1/Z11/H3 parents; the six source pieces, first-order Euler errors, momenta and boundary currents are still essential. Nor is it permission to delete Y aether/scalar RHS in the actual H4 solve.

**Interpretation of previous G2A:** The almost phase-aligned, beta-independent **direct shift-source** correction is compatible with the fact that the direct Y2 shift row is zero. But the action proof does not identify which other source sector creates the Cstar active shift failure, and cannot convert \`|E_b|\` into a signed complex residual.

## 5. Regularity at the zero-gradient set and proper negative controls

For scalar real \`g\`, \`F(g)=g|g|\` is \(C^1\), and \`DF(g)[h]=2|g|h\) at **all** \`g\`, including \`g=0\`. Since \`F'\` is Lipschitz with constant 2,

\`\`\`text
|F(g+eta*h)-F(g)-2eta|g|h| <= eta^2 |h|^2.
\`\`\`

For continuous, piecewise \(C^1\) (or suitable Sobolev) gradients \`g10,g11\`, both \`F(g10)\` and \`|g10|g11\` are continuous across a zero crossing; consequently their distributional spatial derivatives have **no delta mass arising solely from that crossing**. If a physical gradient actually jumps, its flux jump requires an explicit distributional interface term. This differs from the old GE05 R1 **time-derivative** jumps, which do require the independently frozen bath current jump.

Since \`F(epsilon*g)=epsilon*|epsilon|F(g)\`, its second amplitude derivative at \`epsilon=0\` differs from the left and right: the NL0C treatment is an intentional **positive-amplitude directional weakly nonlinear hierarchy**, not a globally smooth field-independent Hessian. Therefore the result **cannot be used to assert globally bounded FD8 ninth derivatives** or the missing Y zero-set FD4/FD8 \`B_total\` regularity budget.

## 6. Actual scope and next research gate

What is now analytically complete **without new numerics**: original GE06/GE05/GE07 spatial density symmetry (G2B), original nonanalytic NL0C Y off-shell density symmetry, **zero direct Y mixed H4 spatial Ward term**, exactly preserved Stage E aether/scalar H3/H4 source, and no new zero-gradient delta from continuous gradients.

What is still NOT certified: original signed full all-parent \`R_parent\`, \`B_parent\`, \`E_L\`, complex signed \`E_b\`, their common-time physical dynamics and independent original FD4/FD8+roundoff/zero-set budget. Recovering stage forcing alone (G2A) cannot fill these gaps.

**Stop repeated algebraic-source numerics.** The next discriminating physical work is one common-source **signed Euler-parent and action boundary test** with original H1/Z11, validated GE05 bath, corrected Z20/q20, and Y from *original action*; proceed only if the original signed complex canonical states and sufficient continuous-error evidence can actually be recovered. Do not adjust frozen coefficients, historical final \`1e-6\` H4 shift threshold, temporal order \`>=2.5\`, or claim \(Z_{21}\)/lensing.

**Unchanged:** D55Cr11f narrowly certified continuum bath H-channel for primary Cstar six modes; Cr12abR2 \`IMPLEMENTATION_FAIL\` + active H4 shift \`1.217597e-6\` science FAIL; D55Cr12ad historical closeout \`1.21759654e-6\`, original frozen campaign CLOSED; full H4 Ward **OPEN**.
