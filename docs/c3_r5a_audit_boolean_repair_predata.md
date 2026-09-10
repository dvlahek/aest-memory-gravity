# C3 R5A audit-boolean technical repair — pre-data declaration

Run 34491866576 established the R5 CLASS eta=0 zero-coupling repair: all 18 alpha/E/theta comparisons were exactly zero within printed precision and `ZERO_COUPLING_PASS=True`.

The subsequent R5 reference builder stopped before signed-lambda CLASS runs because its audit dictionary contained the descriptive metadata entry `signed_lambda_is_physical_eta: False` and then incorrectly required `all(audits.values())`. The false value is the intended physical meaning, not a failed audit. All six external-bath force histories had already been constructed with finite values, full pre-z=6 history, exact requested k modes, normalized positive order-39 weights, and step size no larger than the frozen main step.

Frozen R5A repair: replace only this contradictory boolean audit representation with the logically positive check `signed_lambda_not_physical_eta: True` while retaining separate metadata `signed_lambda_is_physical_eta: False`. No force values, equations, bath integration, CLASS patch, k modes, redshifts, lambda, order, tauH0, or C3 tolerance may change.

Historical R5 run 34491866576 remains an immutable technical INCOMPLETE after a successful zero-coupling subtest. R5A continues from the same preregistered R5 physics. `FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False` regardless of outcome.