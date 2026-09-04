# v0.20 — core-ΛCDM memory-fingerprint gate

This stage asks a different question from v0.19: not merely whether the Exp finite-memory CMB tangent exists, but whether its TT/EE/TE shape is distinguishable from the tangent space of the six core ΛCDM parameters.

The primary memory response is the eta=0 variational forcing tangent extracted with numerical amplifier lambda=1000. Lambda=300 is retained as an internal numerical control. Both are diagnostic amplifiers of the exact first-order forcing and are not physical eta values.

The nuisance tangent space contains central finite-difference responses to H0, omega_b, omega_cdm, tau_reio, n_s, and ln A_s. Every nuisance derivative is evaluated at two step sizes. Projection is performed in the full-sky cosmic-variance metric for the joint unlensed TT/EE/TE covariance over 30 <= ell <= 2500.

The principal outputs are

- the raw cosmic-variance S/N per unit eta;
- the marginalized cosmic-variance S/N per unit eta after projecting out the six-dimensional core-ΛCDM tangent space;
- the retained fraction ||S_eta^perp||_CV / ||S_eta||_CV;
- the eta values corresponding to ideal full-sky CV-limited S/N = 1 and 3;
- multipole-band contributions to the residual signal;
- finite-step convergence of all nuisance directions and lambda=300 versus lambda=1000 memory control.

A large retained fraction is evidence for a distinct memory spectral fingerprint. A small retained fraction means that the leading Exp memory response is largely degenerate with ordinary cosmological parameter changes. This stage is deliberately limited to the core six-parameter ΛCDM tangent space, unlensed spectra, and an ideal cosmic-variance metric. It is not yet a Planck likelihood, foreground, lensing, experimental-noise, or extended-parameter forecast.
