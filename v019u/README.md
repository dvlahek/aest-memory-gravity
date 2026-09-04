# v0.19u — first tauH0=1 finite-memory CLASS response with validated compressed bath

v0.19t found a 39-mode positive fixed-frequency bath that reproduces the stable N=16384 continuum response on held-out tauH0=1 AeST CLASS source histories with max normalized waveform error below 5e-4. A richer 47-mode checkpoint is retained as an independent bath-order control.

This gate inserts those two positive baths into the existing v0.19j CLASS memory implementation and repeats the finite-eta CMB response test at tauH0=1.

For each bath order, eta=0 carries exactly the same auxiliary state vector as eta>0. The finite-memory response is therefore measured after same-bath eta=0 subtraction, removing the ODE-vector common mode.

Primary tests:

- eta linearity for the 39-mode bath using eta={0.003,0.01,0.03};
- response-shape cosine consistency across eta;
- 39-mode versus 47-mode response convergence at eta=0.01;
- exact background and thermodynamics independence from eta;
- eta=0 recovery and nonzero finite-memory signal.

This is a numerical CLASS response gate, not a Planck likelihood constraint. It remains restricted to tauH0=1, the first finite-memory cosmology benchmark already used in v0.19j.
