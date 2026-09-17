# NL1C7B4 result — raw initial-constraint domain audit

Status: **OFFICIAL RESULT / FROZEN**

Classification:

`NL1C7B4_CONSTRAINT_IMPLEMENTATION_INCOMPLETE`

## Provenance

- official run: `35211367954`
- workflow head: `6158d481a4584e1778abdc8dbf4ce600fa381105`
- preregistration: `336c219f713fe5f573ed25223f9c723956869038`
- implementation lock: `98f9e879091e231614457b43e1fcdd8a92269d52`
- implementation blob: `8559120dc273be3174eca130ca313ed6ff5acb25`
- artifact: `10492575332`
- artifact SHA256: `9fdf56fd2c2b224c934cc15be31d5d27076971b50ab2961849c151939d60ef74`

## Result

The official C7A primary state is reproduced from the retained dense trace with maximum relative L2 mismatch

`2.8776273478160806e-14`,

well below the frozen `1e-12` interface limit. Provenance and no-state-modification gates pass.

However, the exact nonlinear C6 scalar dictionary

`Q_C6 = cosh(u) phidot + sinh(u) phi_r/L`

moves the local scalar away from the background by much more than the very narrow frozen Exp scale `Z0=1e-17 Mpc^-1`. The resulting maximum `Z^2=((Q_C6-Q0)/Z0)^2` values are

- `R_sigma=5 h^-1 Mpc`: `7.039197501241302e14` (Nr=256), `7.03908267201187e14` (Nr=512),
- `R_sigma=10 h^-1 Mpc`: `2.9061371286259155e17` (Nr=256), `2.90782525349259e17` (Nr=512),
- `R_sigma=20 h^-1 Mpc`: `6.587991480938218e17` (Nr=256), `6.592837402894424e17` (Nr=512).

For comparison, direct float64 evaluation of `exp(Z^2)` ceases to be representable above `log(float64_max)=709.782712893384`. Therefore the unmodified full Exp action cannot be evaluated by the locked ordinary float64 constraint implementation on any of the six frozen scale/grid cases.

No clipping, saturation, linearization of `Q_C6`, replacement of the Exp branch, constraint projection, or trajectory evolution was performed.

## Interpretation boundary

This result is not yet a raw Hamiltonian/momentum science FAIL. It establishes that the exact nonlinear scalar kinematics combined with the frozen `Z0` drive the Exp Q-sector far outside the direct float64 evaluation domain. A separate pre-result numerical repair may evaluate the same exact Exp contribution in log/scaled form. Only that repair can distinguish representation overflow from an actual raw-constraint failure.
