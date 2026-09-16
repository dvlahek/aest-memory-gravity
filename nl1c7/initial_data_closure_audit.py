#!/usr/bin/env python3
import json, math
from pathlib import Path
import sympy as sp

OUT=Path('results/nl1c7_initial_data_closure_audit.json')
OUT.parent.mkdir(parents=True,exist_ok=True)

# Frozen NL1C6 physical constants.
KB=sp.Rational(665,10000)
C=2-KB
K2=sp.Integer(9500)
Q0=sp.Float('1e-4',50)
Z0=sp.Float('1e-17',50)

# Gauge-fixed NL1C6 dynamical variables and velocities.
L,R,u=sp.symbols('L R u', positive=True, real=True)
vL,vR,vu,vp=sp.symbols('vL vR vu vp', real=True)
pr,ur=sp.symbols('pr ur', real=True)
c=sp.cosh(u); s=sp.sinh(u)
Q=c*vp+s*pr/L
X=s*vp+c*pr/L
E=c*vu+s*(vL/L+ur/L)
Z=(Q-Q0)/Z0
K=2*K2*Z0**2*(sp.exp(Z**2)-1)

# For the rank audit only the local second-velocity derivative of the frozen
# full-Y sector matters. Represent it by M >= 0, exactly as certified in G11.
M=sp.symbols('M', nonnegative=True, real=True)
lag_principal=L*R**2*(-4*(vL/L)*(vR/R)-2*(vR/R)**2 + KB*E**2 + 2*C*E*X - C*(1+M)*X**2 + 2*K)
vel=(vL,vR,vu,vp)
H=sp.hessian(lag_principal,vel)
rank_symbolic=H.rank()

detH=sp.factor(H.det())
KQQ=4*K2*sp.exp(Z**2)*(1+2*Z**2)
expected=64*L**2*R**6*c**2*(s**2*(C**2+C*KB*(1+M))-KB*KQQ*c**2)
det_identity=sp.simplify(detH-expected)==0

# Evaluate the principal block exactly at the frozen homogeneous eta=0
# background point used to start a cosmological growing-mode construction.
sub_bg={L:1,R:1,u:0,pr:0,ur:0,vL:sp.Rational(1,10),vR:sp.Rational(1,10),vu:0,vp:Q0,M:0}
Hbg=H.subs(sub_bg)
rank_bg=int(Hbg.rank())
det_bg=float(sp.N(Hbg.det(),30))

# Canonical initial-data count after N=1,b=0 gauge choice.
# Four independent second-order fields imply eight radial initial functions.
# The ungauged action retains two first-class radial constraints from lapse N
# and radial shift b. No further primary constraint is present in the four-field
# principal block because rank(H)=4.
n_second_order_fields=4
n_initial_functions=2*n_second_order_fields
n_retained_constraints=2
n_free_after_constraints=n_initial_functions-n_retained_constraints

# eta=0 bath q is decoupled from grav+aest in the frozen C6 identity, so q=0
# can consistently be selected without affecting this count. Matter delta and
# velocity are prescribed source data and do not supply additional equations
# selecting the six gravitational/scalar initial-mode functions.
profile_specifies=['matter_density_overdensity','matter_growing_mode_velocity']
missing_mode_selection=[
    'metric/scalar/aether growing-mode amplitudes',
    'relative phases between the propagating eta0 spherical modes',
    'exclusion of homogeneous/free scalar-aether wave content',
]

unique_from_frozen_profile=False
classification='NL1C7_INITIAL_DATA_CLOSURE_INCOMPLETE'
gates={
    'I1_parent_principal_block_full_rank': bool(rank_symbolic==4 and rank_bg==4 and det_bg!=0.0),
    'I2_G11_determinant_identity_reproduced': bool(det_identity),
    'I3_two_retained_constraints_only': bool(n_retained_constraints==2),
    'I4_profile_does_not_uniquely_select_eta0_mode': bool(n_free_after_constraints>0 and not unique_from_frozen_profile),
    'I5_no_trajectory_executed_before_unique_initial_data': True,
}

result={
    'classification':classification,
    'scope':'NL1C7 pre-evolution eta=0 initial-data closure audit only; no trajectory, no finite eta, no collapse or splashback result.',
    'frozen_parent':{
        'G11_run':35089436959,
        'G11_head':'0f868057e788423b588cda5bc654287c784ebee7',
        'G11_artifact':10442933686,
        'G11_artifact_sha256':'12b83f6f67f473937514005f6a87764646407e3b2141b4451d47bd92b62c6ddc',
    },
    'principal_audit':{
        'symbolic_rank':int(rank_symbolic),
        'background_rank':rank_bg,
        'background_determinant':det_bg,
        'determinant_identity_matches_G11':bool(det_identity),
    },
    'initial_data_count':{
        'second_order_fields':['L','R','u','phi'],
        'n_second_order_fields':n_second_order_fields,
        'n_initial_radial_functions_before_constraints':n_initial_functions,
        'retained_constraints':['Hamiltonian/lapse','radial momentum/shift'],
        'n_retained_constraints':n_retained_constraints,
        'n_free_radial_functions_after_constraints':n_free_after_constraints,
        'bath_q_at_eta0':'decoupled from grav+aest; q=0 is consistent and does not remove the remaining eta0 gravitational/scalar mode freedom',
    },
    'frozen_profile_supplies':profile_specifies,
    'missing_mode_selection':missing_mode_selection,
    'reason':'Regular-center and asymptotic-background boundary conditions constrain radial behavior but do not choose the remaining propagating eta=0 metric/scalar/aether mode content. A separate pre-data growing-mode bridge is required before a unique nonlinear trajectory can be run.',
    'gates':gates,
    'next_licensed_step':'Construct and certify an eta=0 linear growing-mode initial-data bridge from the already frozen cosmological solution into the NL1C6 spherical variables; then rerun NL1C7 without changing the frozen overdensity profile or evolution gates.',
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
