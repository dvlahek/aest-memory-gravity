# NL1C6D2C6A pre-result implementation clarification: initial chi derivative

This clarification is committed before the first D2C6A trajectory result is available. It does not change any preregistered physics, grid, timestep, checkpoint, or PASS/FAIL threshold.

The initial implementation constructed `dchi/dtau` by first sampling a derived `chi(tau)` spline across the full dense CLASS history. The certified corrected background interpolation used by D2C6A intentionally covers only the physical audit interval `0 <= z <= 6`; sampling the full earlier dense history can therefore request the background outside that interpolation domain.

The implementation is replaced by the exact chain rule at the physical initial time `z=6`:

\[
\chi=Q\left(a\Theta/k^2+\alpha\right),
\]

\[
\chi'=Q'\left(a\Theta/k^2+\alpha\right)
+Q\left(a'\Theta/k^2+a\Theta'/k^2+\alpha'\right),
\]

with `Q' = a Qdot` and `a' = a^2 H` in conformal time. `Theta'` and `alpha'` are derivatives of the already frozen cubic splines through the corrected CLASS dense histories.

This removes an unnecessary auxiliary interpolation and introduces no new fitted parameter or numerical tolerance.