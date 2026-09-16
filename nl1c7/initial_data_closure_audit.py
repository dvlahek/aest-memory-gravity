#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

OUT=Path('results/nl1c7_initial_data_closure_audit.json')
OUT.parent.mkdir(parents=True,exist_ok=True)

# Frozen NL1C6 physical constants.
KB=sp.Rational(665,10000)
C=2-KB
K2=sp.Integer(9500)

# Reproduce the exact G11 principal determinant identity without asking SymPy
# to perform a generic rank reduction through the frozen Z0=1e-17 scale.
L,R,u=sp.symbols('L R u', positive=True, real=True)
vL,vR,vu,vp=sp.symbols('vL vR vu vp', real=True)
q0,x0,e0=sp.symbols('q0 x0 e0', real=True)
c=sp.cosh(u); s=sp.sinh(u)
Q=c*vp+q0
X=s*vp+x0
E=c*vu+s*vL/L+e0
Kf=sp.Function('K'); Jf=sp.Function('J'); Y=X**2
lag_generic=L*R**2*(-4*(vL/L)*(vR/R)-2*(vR/R)**2 + KB*E**2 + 2*C*E*X - C*X**2 + 2*Kf(Q) - C*Jf(Y))
H_generic=sp.hessian(lag_generic,(vL,vR,vu,vp))
det_generic=sp.factor(H_generic.det())
Kqq,j,jyy=sp.symbols('Kqq j jyy', real=True)
repl={}
for atom in det_generic.atoms(sp.Subs):
    txt=str(atom)
    if 'Derivative(K' in txt and '(_xi_1, 2)' in txt:
        repl[atom]=Kqq
    elif 'Derivative(J' in txt and '(_xi_1, 2)' in txt:
        repl[atom]=jyy
    elif 'Derivative(J' in txt:
        repl[atom]=j

det_local=sp.expand(det_generic.xreplace(repl))
Mexpr=j+2*X**2*jyy
expected_det=64*L**2*R**6*c**2*(s**2*(C**2+C*KB*(1+Mexpr))-KB*Kqq*c**2)
det_residual=sp.simplify(det_local-expected_det)
det_identity=bool(det_residual==0)

# Frozen G11 global bound: K_QQ >= 4 K2 and M <= 20 for all certified
# full-Y branches. A strictly positive bracket makes det(H) nonzero at every
# finite rapidity, therefore the four-field principal block has rank 4.
M_GLOBAL_MAX=sp.Integer(20)
KQQ_GLOBAL_MIN=4*K2
delta_kin=sp.simplify(KB*KQQ_GLOBAL_MIN-(C**2+C*KB*(1+M_GLOBAL_MAX)))
global_nonsingular=bool(delta_kin>0)
rank_symbolic=4 if det_identity and global_nonsingular else -1

# Independent exact homogeneous-background determinant check using a local
# quadratic principal representative with the frozen local K_QQ and M=0.
gK,gM=sp.symbols('gK gM', positive=True, real=True)
lag_local=L*R**2*(-4*(vL/L)*(vR/R)-2*(vR/R)**2 + KB*E**2 + 2*C*E*X - C*(1+gM)*X**2 + gK*Q**2)
H_local=sp.hessian(lag_local,(vL,vR,vu,vp))
sub_bg={L:1,R:1,u:0,q0:0,x0:0,e0:0,vL:sp.Rational(1,10),vR:sp.Rational(1,10),vu:0,vp:0,gK:KQQ_GLOBAL_MIN,gM:0}
Hbg=H_local.subs(sub_bg)
det_bg_exact=sp.simplify(Hbg.det())
rank_bg=4 if det_bg_exact!=0 else 0
det_bg=float(sp.N(det_bg_exact,30))

# Canonical initial-data count after N=1,b=0 gauge choice.
# Four independent second-order fields imply eight radial initial functions.
# The ungauged action retains two radial constraints from lapse N and shift b.
# No further primary constraint is available because the four-field principal
# block is nonsingular.
n_second_order_fields=4
n_initial_functions=2*n_second_order_fields
n_retained_constraints=2
n_free_after_constraints=n_initial_functions-n_retained_constraints

# eta=0 bath q is decoupled from grav+aest in the frozen C6 identity, so q=0
# can consistently be selected without affecting this count. Matter delta and
# velocity are prescribed source data and do not select the remaining six
# gravitational/scalar initial-mode functions.
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
    'repair01':{
        'historical_technical_failure_run':35091142502,
        'change':'generic SymPy H.rank() replaced by exact determinant identity plus frozen G11 positive kinetic-margin certificate; no science gate changed',
    },
    'principal_audit':{
        'symbolic_rank':rank_symbolic,
        'background_rank':rank_bg,
        'background_determinant':det_bg,
        'determinant_identity_matches_G11':bool(det_identity),
        'determinant_identity_residual':str(det_residual),
        'global_kinetic_lower_bound':float(delta_kin),
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
