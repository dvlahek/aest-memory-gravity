# Full-J 3D saturated constitutive closure — locked result

Classification:

`FULLJ_3D_SATURATED_CONSTITUTIVE_CLOSURE_PASS`

This result locks the preregistered 3D stochastic lattice-shell audit of the saturated constitutive closure on the central reference theory branch

- `sigma = 0`
- `kind = simple`
- `beta0 = 1.0`

using 16 frozen Gaussian angular realizations over all nine redshift checkpoints `z = [6,5,4,3,2,1.5,1,0.5,0.2]`, primary grid `64^3`, and control grid `80^3` at `z = [6,1,0.2]`.

Locked summary from the completed run:

- `finite_all = true`
- maximum weighted flux saturation residual: `2.307761543003831e-05`
- median weighted flux saturation residual: `2.979242337189048e-07`
- maximum full-operator saturation residual: `2.2806686962621596e-05`
- median full-operator saturation residual: `2.946360580835575e-07`
- minimum `1+j`: `1.9885365245008164`
- maximum shell-power ratio error relative to the saturated `2 Laplacian` closure: `4.249118070720481e-05`
- median shell-power ratio error: `5.500920746137616e-07`
- maximum `64^3 -> 80^3` change in shell ratio: `5.391095081463959e-08`
- maximum `64^3 -> 80^3` change in mean operator residual: `8.058602629789518e-07`

All preregistered gates G1--G7 passed.

The result establishes, on the locked central branch and tested shell/redshift domain, that

`div[(1+j) grad chi]`

is numerically equivalent to

`2 Laplacian chi`

at much better accuracy than the preregistered 2% operator and 5% shell-power tolerances. The error is largest at `z=6` and decreases rapidly toward late times.

Licensed scope after this PASS:

- `THREE_D_SATURATED_LAPLACIAN_CLOSURE_LICENSED=True`
- `THREE_D_ISOTROPIC_TRANSFER_CONSTRUCTION_LICENSED=True`

Still not licensed:

- `THREE_D_ISOTROPIC_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

This remains a stochastic 3D shell audit seeded by locked R2 radial amplitudes, not a brute-force 3D time evolution. The next milestone is an explicitly normalized isotropic transfer construction, with independent single-mode/separability checks before constructing a 3D Weyl power spectrum.
