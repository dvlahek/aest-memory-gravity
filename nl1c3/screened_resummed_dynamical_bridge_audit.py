#!/usr/bin/env python3
from pathlib import Path
import json, math

OUT = Path('results'); OUT.mkdir(exist_ok=True)

KB = 0.0665
K2 = 9500.0
Q0 = 1e-4
BETAS = [1.0, 0.5, 0.1]
KINDS = ['simple','exponential','sharp']
XPHYS = [1.0911e7, 4.3274e7, 9.4551e7]


def jfun(x,beta,kind):
    A=1.0+beta
    if kind=='simple':
        return x/(A+beta*x)
    if kind=='exponential':
        return -math.expm1(-beta*x/A)/beta
    if kind=='sharp':
        return min(x/A,1.0/beta)
    raise ValueError(kind)


def stiffness(x,beta,kind):
    # s = |d ln j / d ln x|.  Stable analytic forms.
    A=1.0+beta
    if kind=='simple':
        return A/(A+beta*x)
    if kind=='exponential':
        y=beta*x/A
        if y>700:
            return 0.0
        den=-math.expm1(-y)
        return y*math.exp(-y)/den if den>0 else 1.0
    if kind=='sharp':
        return 1.0 if x < A/beta else 0.0
    raise ValueError(kind)

sat_rows={}
max_sat=0.0; max_stiff=0.0
for kind in KINDS:
    sat_rows[kind]={}
    for beta in BETAS:
        rows=[]
        for x in XPHYS:
            j=jfun(x,beta,kind)
            jinf=1.0/beta
            sat=abs(j-jinf)/jinf
            s=stiffness(x,beta,kind)
            max_sat=max(max_sat,sat); max_stiff=max(max_stiff,s)
            rows.append({'x':x,'j':j,'j_infinity':jinf,
                         'saturation_relative_error':sat,
                         'logarithmic_coefficient_stiffness':s})
        sat_rows[kind][str(beta)]=rows

mu2=2*K2*Q0*Q0/(2-KB)
mu=math.sqrt(mu2)

# Action-level bookkeeping after U_j = sqrt(eta) q_j:
# S_mem = eta * S_hat_mem[g,A,phi,q].  Therefore d/deta of every physical
# Euler-Lagrange equation at eta=0 is the corresponding functional derivative
# of S_hat_mem evaluated on the eta=0 finite-amplitude reference.  At X=q=0
# its direct metric stress starts quadratically and vanishes at linear FLRW;
# at a finite X0,q0 reference it is generically nonzero and must be retained.

quantitative_checks={
    'D1_saturated_coefficient_within_NL1C2_bound': max_sat <= 2e-6,
    'D1_shape_stiffness_within_NL1C2_bound': max_stiff <= 2e-6,
    'mass_scale_finite_positive': math.isfinite(mu) and mu>0,
}

analytic_status={
    'D1_saturated_Y_tangent':'closed_at_operator-coefficient_level',
    'D2_FLRW_background_preserved':'closed_by_expansion-point_separation',
    'D3_static_high-gradient_control':'closed_by_published_screened_AeST_limit',
    'D4_covariant_source_placement':'closed_functionally_from_frozen_action',
    'D5_Noether_Bianchi_consistency':'closed_functionally_if_reference_solves_memory-off_equations',
    'D6_memory_tangent_compatibility':'closed_functionally; direct finite-reference metric/scalar/aether memory sources are mandatory',
    'D7_deterministic_component_system':'not_closed: explicit gauge-fixed 3+1/component equations for the finite-amplitude AeST+memory tangent are not yet generated',
    'D8_pre_numerical_validation_plan':'frozen_in_result_note_before_any_memory-survival_run',
}

classification='NL1C3_SCREENED_RESUMMED_DYNAMICAL_BRIDGE_INCOMPLETE'
summary={
 'classification':classification,
 'scope':'analytic/structural screened-resummed bridge audit; no memory-survival result and no observational data',
 'frozen_inputs':{'KB':KB,'K2':K2,'Q0_1_per_Mpc':Q0,'beta0_co_primary':BETAS,
                  'interpolation_controls':KINDS,'physical_x_checkpoints':XPHYS},
 'saturation':sat_rows,
 'max_saturation_relative_error':max_sat,
 'max_logarithmic_coefficient_stiffness':max_stiff,
 'mu2_1_per_Mpc2':mu2,'mu_1_per_Mpc':mu,'mu_inverse_Mpc':1.0/mu,
 'quantitative_checks':quantitative_checks,
 'analytic_status':analytic_status,
 'component_level_solver_ready':False,
 'critical_result':'The eta=0 tangent around a finite screened reference cannot use only the historical E-closure forcing. The normalized NL0B action produces, at O(eta), scalar/aether forces and a direct metric stress evaluated on the nonzero reference. Those terms vanish in the original FLRW linear audit but are generically nonzero here.',
 'required_next_step':'Generate and validate the gauge-fixed 3+1/component Euler-Lagrange system for the frozen AeST plus NL0B action before any screened-resummed memory-survival calculation.',
 'historical_results_unchanged':True,
}
(OUT/'nl1c3_screened_resummed_dynamical_bridge_audit.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
if not all(quantitative_checks.values()):
    raise SystemExit(2)
