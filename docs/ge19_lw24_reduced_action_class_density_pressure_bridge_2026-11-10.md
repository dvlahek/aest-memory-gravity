# GE19 LW24 — reduced action to CLASS density/pressure bridge

**Date: 2026-11-10.** A separate local SymPy proof script completed **17/17 exact checks PASS** on this bounded problem. The newly committed, source-locked canonical LW24 WSL runner is **not yet executed by the researcher**. The algebra was explored before the predata document: this is not an independent blind preregistration. No CLASS evolution, survey likelihood, or new physical parameters.

## LW23 original WSL result — exact archive

Researcher original \`ge19_lw23_r1.log\`: 335 bytes, SHA-256 \`8cb334a668ed381749a68d4ceb64e5a933084ba4526a7f8887ceed5a0ae1cf9a\`, Git blob \`617d1a66816eb1df67d6ffffcbead7ad7b759133\`.
Original \`ge19_lw23_implemented_eta_source_action_branch_20261110_r1.json\`: 3521 bytes, SHA-256 \`cb4fab1b275634e95401bbf5b4ac02022cf98949f4a6fab082276d5c161eb185\`, Git blob \`830383ffe9c39561ac358e1dbcec6d83fe3d0cf1\`. **GitHub readback matches both original git-blob hashes exactly**. Original WSL LW23 source and symbolic checks passed 10/10 each; full action-to-CLASS physical response remains open.

## Background density, pressure and adiabatic speed

The frozen GE06 reduced analytic scalar-longitudinal action (not the full 3+1 nonanalytic Y theory) contains

\[
\mathcal L_{\rm AeST}=NLR^2[K_B E^2+2(2-K_B)EX-(2-K_B)X^2+2K(Q_{\rm inv})].
\]

At relaxed FLRW \(N=1,L=R=a,b=u=0,\dot\phi=Q,E=X=0\), exact lapse variation is

\[
\left.\partial_N\mathcal L_{\rm AeST}\right|_0=2a^3(K-QK_Q).
\]

The original \`v019/patch/source/aest_memory.c\` explicitly returns \(\rho_A=(QK_Q-K)/3\), \(p_A=K/3\), \(c_a^2=K_Q/(QK_{QQ})\), and \(K_Q=I_0/a^3\). These match the reduced action's background stress conventions, accounting for its gravitational factor and CLASS's background H-squared normalization. Moreover,

\[
d\rho_A/d\ln a+3(\rho_A+p_A)=0,\qquad
dp_A/d\rho_A=K_Q/(QK_{QQ}).
\]

## New linear lapse-to-fluid stress identity

In the Newtonian longitudinal scalar sector,

\[
\delta Q=\dot\varphi-Q\Psi,\quad E_1=(ik/a)E_A,\quad
X_1=(ik/a)\chi,\quad
E_A=\dot\alpha+\Psi,\quad \chi=\varphi+Q\alpha.
\]

The linearized original action's lapse and lapse-gradient derivatives give

\[
\delta(\partial_N\mathcal L_{\rm AeST})=
-2a^3 QK_{QQ}\delta Q
+2a^2(K-QK_Q)(\delta L+2\delta R),
\]

\[
\delta(\partial_{N_x}\mathcal L_{\rm AeST})
=2a^2[K_BE_1+(2-K_B)X_1].
\]

The combination \(E_N=\partial_N\mathcal L-\partial_x\partial_{N_x}\mathcal L\), with background metric-volume terms removed, gives the restricted action-derived density

\[
\boxed{\delta\rho_A=
\frac13\left[QK_{QQ}\delta Q-
\frac{k^2}{a^2}(K_BE_A+(2-K_B)\chi)\right].}
\]

Independent longitudinal and transverse spatial variations yield

\[
\boxed{\delta p_A=K_Q\delta Q/3.}
\]

Eliminating \(\delta Q\) using \(c_a^2=K_Q/(QK_{QQ})\) now gives

\[
\boxed{\delta p_A=c_a^2\delta\rho_A+
\frac{c_a^2k^2}{3a^2}[K_BE_A+(2-K_B)\chi].}
\]

This is **exactly the algebraic CLASS AeST pressure formula** \(\Pi_A=c_a^2\delta_A + c_a^2 k^2 [K_BE_A+(2-K_B)\chi]/(3a^2\rho_A)\) when \(\delta\rho_A=\rho_A\delta_A\) and \(\delta p_A=\rho_A\Pi_A\). This independently derives the source of the extra CLASS pressure term: the lapse-gradient dependence of the original \(E,X\) action.

A post-prelock exploratory action variation also gives the reduced shift source \(\delta E_b=-2a^3K_Q\partial_x\varphi\). This identifies a momentum pathway; an exact aether+metric shift-to-CLASS \((\rho+p)\theta_A\) mapping has **not** been established yet.

## Claim boundary

**PASS, restricted:** original analytic plane-symmetric reduced action reproduces the frozen CLASS background density, pressure, sound speed, and the linear scalar lapse/pressure identity. The local symbolic probe passed 17/17 checks, including wrong-factor, missing-gradient and wrong-sign controls. Source-locked WSL program is committed for independent replay.

**OPEN:** full original 3+1 action including nonanalytic Y; independent complete momentum/aether Euler and Einstein lapse/shift constraints; ordinary-species coupled response; finite-eta auxiliary/continuum branch equivalence; physical full matter-Weyl derivative; gamma_t angular forward and nuisance-marginal DES analysis. LW22 geometry PASS and LW23 E-source PASS remain true. LW03 FAIL, LW05 cosmic shear LOS BLOCK, LW08 antisymmetric channel unresolved, H4/Z21 uncertified are unchanged. There is no detection or \(\sigma_\eta\) forecast.

## Frozen code

Predata: \`ge19/lw24_reduced_action_class_density_pressure_dictionary_predata_20261110.json\`, Git commit \`51737d759792b8251429ad3d2ef2d71a956762c4\`, blob \`7c6ba7a0a0b85af6104d1b7e398c57edf0943f40\`.

Executable: \`ge19/lw24_reduced_action_class_density_pressure_dictionary_20261110.py\`, commit \`56acb5672622d3924c378cca4965a89f7b2bce4f\`. No DES files or patched CLASS run needed, only SymPy and frozen project source files. The canonical WSL output has **not** yet been produced.

**Next physical gate:** full aether and ADM momentum-to-CLASS state identification, followed by the constrained source-to-Weyl state Jacobian. Do not fit DES residuals or launch a new k/z numerical sweep before that closure.
