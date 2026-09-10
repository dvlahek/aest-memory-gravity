# NL1C6D2C4 pre-data numeric clarification

Status: **FROZEN BEFORE D2C4 IMPLEMENTATION/RESULT**.

This note supplies the exact numerical interpretation of C4.5 in the already-preregistered D2C4 derivative-bounded completion.

For each frozen `j` interpolation and `beta0 in {1,0.5,0.1}`, evaluate

`x = [1e2,1e3,1e4,1e6]`

and `lambda_s=1/beta0`.

Require:

1. `j(x)>0` at all four points;
2. `j(x)/lambda_s` is monotone nondecreasing across the four points;
3. at `x=1e6`, `abs(j/lambda_s-1) <= 2e-5`.

For the mixed factor, at `x=1e6` and every frozen Z/sigma, require the exact analytic local modulation

`F_Y/(A*j)`

to differ from its `x->infinity` target

`1 + sigma*epsilon_mix*tanh(Z)^2`

by at most `1e-10`.

No D2C3 result is modified and no observational/nonlinear trajectory output has been evaluated when freezing this clarification.
