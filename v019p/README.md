# v0.19p — eta=0 precision and quasi-null convergence test

This campaign isolates the small v0.19 eta=0 CMB differences before any memory
coupling is enabled.

The `Exp` benchmark has a background numerically indistinguishable from matched CDM
at the precision reported by v0.19, so it is used as a **quasi-null background
control**. It is not called a strict null theory because its eta=0 AeST perturbation
closure is still active.

Four precision levels are compared:

- `p0`: standard CLASS precision used in v0.19;
- `p1`: `tol_perturb_integration=1e-6`, `perturb_sampling_stepsize=0.01`;
- `p2`: `2e-7`, `0.005`;
- `p3`: `5e-8`, `0.0025`.

For CDM and Exp, all four levels are run. Cosh is run at `p0` and `p3` as a
nontrivial-background control.

The primary metric is the largest peak-normalized difference among TT, EE and TE
(columns 2–4 of CLASS `cl.dat` / `cl_lensed.dat`) over 30 <= ell <= 2500. The
all-column maximum is also reported, but is not used as the main convergence gate
because tiny cross-spectra can inflate relative ratios.

Interpretation:

- if Exp-CDM shrinks strongly with precision and approaches the CDM self-convergence
  floor, the v0.19 residual is mainly numerical;
- if Exp-CDM remains stable while the CDM self-convergence floor collapses, the
  residual belongs to the current eta=0 proxy bridge rather than ordinary CLASS
  integration error;
- neither outcome turns the regular chi_i=0 proxy into the unpublished exact AeST
  radiation-era adiabatic initial condition.

Memory remains strictly OFF in this campaign.
