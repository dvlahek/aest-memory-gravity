# NL1C7A A3/A4 trace extension — implementation lock

Status: **LOCKED BEFORE ANY EXTENDED CLASS TRACE RUN**

Parent C7A preregistration: `5399a2ca73165e8f97cea45934e50baf8ffb3629`.

Certified A2 gauge audit:

- workflow run: `35092206904`
- head: `0ccd15c1a7b6660a72fa1c49e8e7317967443631`
- artifact: `10444488624`
- artifact SHA256: `05b36f93e272aebf04f9887b384c695b01b399ca4e816b1549a8e5d7f8189422`

Frozen output-only trace extension:

- path: `nl1c7a/apply_trace_extension.py`
- blob SHA: `b25b6087cb1e9fd6a275ffcf0843c880d009efce`
- implementation commit: `ab5b8e5fb40b25433bc5caf2e1f6be2df09abf76`

The extension may replace only the existing v0.23 trace function prototype, trace helper body, and accepted-source trace call. It may add diagnostic state fields but may not modify background or perturbation evolution equations.

Required output fields are `k,tau,a,H_Mpc_inv,H_over_H0,chi,Q,rhoA,KQ,KQQ,delta_b,theta_b,delta_A,theta_A,alpha_A,E_A,Phi,Phi_prime,Psi`.
