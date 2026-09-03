# AeST + memory v0.19
## First active eta=0 CLASS bridge

The effective AeST background is defined by

\[
8\pi G\rho_A = Q K_Q-K,\qquad 8\pi G P_A=K,\qquad K_Q=I_0/a^3.
\]

CLASS stores densities in Friedmann units, hence

\[
\rho_A^{\rm CLASS}=(QK_Q-K)/3,\qquad P_A^{\rm CLASS}=K/3.
\]

The present integration constant is calibrated so that the AeST component has the same present density as the input `omega_cdm` target.

For the scalar perturbation bridge, CLASS's CDM slots become \(\delta_A\) and velocity divergence \(\Theta_A\). The additional states are \(\alpha\) and \(E\). With

\[
u_A=\frac{a\Theta_A}{k^2},\qquad \chi=Q(u_A+\alpha),
\]

\[
\Pi_A=c_{\rm ad}^2\delta_A+\frac{c_{\rm ad}^2 k^2}{3a^2\rho_A^{\rm CLASS}}[K_BE+(2-K_B)\chi].
\]

The eta=0 evolution is the published AeST effective-fluid closure written in conformal time. Memory is not active in v0.19.

The initial-condition proxy

\[
\alpha_i=-a_i\Theta_{A,i}/k^2,\qquad E_i=0
\]

sets \(\chi_i=0\). This is a regular diagnostic proxy, not a claim to reconstruct the unpublished exact AeST radiation-era initial conditions.
