# v0.19i — radiation-era AeST adiabatic initial-condition gate

This gate revisits the eta=0 scalar initial conditions before any memory coupling is enabled.

The starting point is the scalar system of Skordis & Zlosnik, Phys. Rev. Lett. 127, 161302 (2021), arXiv:2007.00082. In Newtonian gauge they define

\[
\chi = \varphi + \bar Q\,\alpha,
\qquad
E = \dot\alpha + \Psi,
\qquad
\theta = \frac{\varphi}{\bar Q}.
\]

The important observation is that `chi` and `E` are invariant under the scalar time-shift that generates the adiabatic long-wavelength mode. With an infinitesimal time shift `T(x)` one has, up to the sign convention used here,

\[
\varphi\rightarrow\varphi-\bar Q T,
\qquad
\alpha\rightarrow\alpha+T,
\qquad
\Psi\rightarrow\Psi-\dot T,
\]

so that

\[
\chi\rightarrow\chi,
\qquad
E\rightarrow E.
\]

A perturbation generated from the homogeneous FLRW solution by this common time shift therefore has

\[
\boxed{\chi=0,\qquad E=0}
\]

in the strict superhorizon limit. Since `theta = varphi/Q`, this gives

\[
\boxed{\alpha=-\theta,\qquad E=0}
\]

at leading order in gradients.

The density part follows from vanishing relative entropy. For the AeST effective component,

\[
\frac{\delta_A}{1+w_A}
=
\frac{\delta_c}{1+w_c}
=
\frac34\delta_\gamma
\]

at leading adiabatic order. Since `w_c=0`, the CLASS initial value should therefore be

\[
\boxed{\delta_A=(1+w_A)\,\delta_c}
\]

while the velocity potential is shared by the adiabatic mode. In the v0.19 CLASS bridge the stored velocity variable is the usual divergence `Theta_A`, related to the paper's potential by

\[
\theta_A=\frac{a\,\Theta_A}{k^2}.
\]

Hence the CLASS implementation is

\[
\boxed{
\delta_A=(1+w_A)\delta_c,
\qquad
\Theta_A=\Theta_c,
\qquad
\alpha_A=-\frac{a\Theta_A}{k^2},
\qquad
E_A=0.
}
\]

This is the regular **leading superhorizon adiabatic mode**. It is stronger than the former wording "regular proxy": the `chi=E=0` part follows from the long-wavelength adiabatic time-shift construction. However, this alone does not prove that all finite-gradient terms have been included. In general

\[
\chi,E = O\!\left[(k/\mathcal H)^2\right]
\]

corrections may appear.

For this reason v0.19i has two independent gates:

1. an algebraic/asymptotic derivation gate for the leading mode above;
2. a CLASS initial-time convergence ladder. The same Cosh and Exp models are started progressively farther outside the horizon while using the strict v0.19p perturbation tolerances.

If the CMB spectra and the Exp–CDM residual converge as the start is pushed earlier, the omitted finite-gradient IC terms are numerically irrelevant at the required accuracy. If they move systematically, v0.19i is not closed and the next step is an explicit Frobenius expansion through `O((k tau)^2)`.

Memory remains exactly OFF throughout v0.19i.
