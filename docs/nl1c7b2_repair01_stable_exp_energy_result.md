# NL1C7B2 Repair01 stable Exp background-energy result

Final classification:

`NL1C7B2_REPAIR01_HOMOGENEOUS_BACKGROUND_SECTOR_INCOMPLETE`

Official provenance:

- run `35193003807`
- head `6804934c12b7fa02bbec3c5e1d06ec31466f1c44`
- artifact `10484278813`
- artifact SHA256 `76f24778c432b018724c90cdbb3c6a586dd37698fa9ae4eb644cf8acd0b99059`
- historical B2 run `35190742632` remains immutable.

Repair01 used the frozen CLASS Exp `KQ -> Z` inversion instead of the cancellation-limited `(Q-Q0)/Z0` reconstruction. No physical parameter, interpolation rule or gate changed.

Results at `a_i=0.02`:

- stable scalar-energy relative error: `3.4627212054553847e-15`
- stable KQ formula relative error: `3.2621603932371898e-15`
- B2-G2 exact homogeneous lapse identity: PASS
- B2-G3 scalar-energy consistency: PASS
- B2-G4 baryon normalization: PASS
- B2-G5 homogeneous Hamiltonian closure: FAIL
- B2-G6 k/interpolation control: PASS
- signed unassigned homogeneous remainder: `0.00010529789814922824 Mpc^-2`
- remainder fraction of `3H^2`: `0.01740837590930068`.

All Repair01 gates R1-R4 pass. Therefore the remaining discrepancy is a real omitted homogeneous standard-background sector relative to the present spherical action, not an AeST energy-reconstruction error.

No radial initial constraint, nonlinear evolution, finite eta, turnaround or collapse calculation was executed.