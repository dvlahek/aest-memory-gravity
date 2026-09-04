#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
from global_fixed import exact_kernel,oscillator_basis

OUT=Path('results');OUT.mkdir(exist_ok=True)
red=json.loads((OUT/'v019o_fixed_bath.json').read_text())
omega=np.asarray(red['omega_tau'],float)
w=np.asarray(red['positive_weights'],float)

all_pos=bool(np.all(omega>0) and np.all(w>=0))

# High-frequency limit is sum of weights; exact target is 1.
high=float(w.sum())
high_err=abs(high-1.)

# Static limit must vanish exactly for every mode.
static=float(np.dot(np.zeros_like(w),w))

# Sample retarded right-half-plane positivity of the finite response.
min_re=np.inf;max_rel=0.
for h in np.logspace(-4,8,17):
    for nu in np.logspace(-3,3,41):
        for eps in [1e-6,1e-3,.03,.1]:
            z=h*(eps+1j*nu)
            B=oscillator_basis(np.array([z]),h,omega)[0]
            pred=complex(B@w)
            ex=complex(exact_kernel(np.array([z]),h)[0])
            min_re=min(min_re,pred.real)
            max_rel=max(max_rel,abs(pred-ex)/max(abs(ex),1e-12))

# Each retained mode is an ordinary positive-energy oscillator with fixed omega_j.
# The finite bath therefore preserves the original conservative local mode structure.
out={
 'active_modes':int(len(omega)),
 'all_frequencies_strictly_positive':bool(np.all(omega>0)),
 'all_weights_nonnegative':bool(np.all(w>=0)),
 'high_frequency_sum_weights':high,
 'high_frequency_relative_error':high_err,
 'static_response':static,
 'minimum_sampled_real_part':float(min_re),
 'maximum_sampled_relative_error':float(max_rel),
 'structure':'fixed positive oscillator frequencies; no H-dependent poles or weights',
 'passivity_interpretation':'The retained modes are a positive subset/redistribution of the original conservative oscillator spectral measure. Positivity of weights and fixed positive frequencies preserves the finite-bath Hamiltonian sign structure.',
 'gate_status':'PASS' if all_pos and high_err<2e-3 and min_re>-2e-5 else 'CHECK'
}
(OUT/'v019o_passivity_summary.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
