# NL1C7B4 Repair05 implementation lock — analytic linear momentum identity

Status: **IMPLEMENTATION LOCK / PRE-RUN**

Predata commit: `96223c4faf1f912f6c47df830a5c50702b2b2ed5`

Implementation commit: `775574efe52870a6a790bdc7d8bc6d72ad4f2e92`

Implementation file: `nl1c7b/initial_constraint_certification_repair05.py`

Implementation blob SHA: `7e5df51c8616966263ce1899a0386a16c74528dc`

Parent Repair04 run: `35223365082`

Parent Repair04 artifact: `10498905089`

Parent artifact SHA256: `1192b25acc1099bd24ff07c1e0b58c448d946513c895307a7c364aa9cfe66f3f`

Parent Repair04 result-freeze commit: `148b5f51b08fae9eb3cf1b49404cca99816bb639`

Retained C7A state artifact: `10481526695`, SHA256 `c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c`.

Retained C7A dense trace artifact: `10469031693`, SHA256 `193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`.

The implementation uses exact symbolic Jacobians of the frozen local momentum Euler-Lagrange sources at the homogeneous background, plus closed-form analytic first-order Exp-K and dust contributions. The Y/J first derivative is fixed to zero by its small-X order and is subject to the preregistered analytic-zero gate. No finite-difference tangent contributes to the primary result.

No state projection, fitted coefficient, sign flip, Y/scale selection, radial standard-species insertion, nonlinear evolution, or finite-eta calculation is permitted in this checkpoint.
