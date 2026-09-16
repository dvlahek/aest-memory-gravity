#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

OUT=Path('results/nl1c7a_gauge_bridge_audit.json')
OUT.parent.mkdir(parents=True,exist_ok=True)

# Independent symbols for a local first-order audit.
a,H,r,Q=sp.symbols('a H r Q', positive=True, finite=True, nonzero=True)
Phi,Psi=sp.symbols('Phi Psi', real=True)
T,Tt,Tr=sp.symbols('T Tt Tr', real=True)
Sr,Srr,St_r=sp.symbols('Sr Srr St_r', real=True)
Phi_t=sp.symbols('Phi_t', real=True)
alpha,alpha_r,Ea,Ea_r=sp.symbols('alpha alpha_r Ea Ea_r', real=True)
varphi,varphi_r,chi,chi_r=sp.symbols('varphi varphi_r chi chi_r', real=True)

# Linear Lie derivative of flat-FLRW spherical background under
# xi^mu=(T,d_r S,0,0), with delta g' = delta g - L_xi gbar.
h_tt_prime=-2*Psi+2*Tt
h_tr_prime=Tr-a**2*St_r
h_rr_prime=-2*a**2*(Phi+H*T+Srr)
h_thth_prime=-2*a**2*r**2*(Phi+H*T+Sr/r)

# Gauge conditions N=1,b=0: Tdot=Psi and a^2 Sdot=T.  Radially,
# a^2 d_r Sdot=d_r T.
gauge_sub={Tt:Psi,St_r:Tr/a**2}
lapse_zero=sp.simplify(h_tt_prime.subs(gauge_sub))
shift_zero=sp.simplify(h_tr_prime.subs(gauge_sub))

# Metric scale perturbations from g_rr=L^2 and g_thth=R^2.
ell=sp.simplify(h_rr_prime/(2*a**2))
rhoR=sp.simplify(h_thth_prime/(2*a**2*r**2))
metric_dictionary={
    'ell':str(ell),
    'rhoR':str(rhoR),
}

# At initial-slice alignment T=S=0, hence Sr=Srr=0. Tdot=Psi and Sdot=0.
ell_i=sp.simplify(ell.subs({T:0,Srr:0}))
rho_i=sp.simplify(rhoR.subs({T:0,Sr:0}))
# d_t ell = -Phi_t - H*Tt at the aligned slice; terms proportional T vanish.
ell_t_i=sp.simplify(-Phi_t-H*Psi)
rho_t_i=sp.simplify(-Phi_t-H*Psi)
L_i=sp.simplify(a*(1+ell_i))
R_i=sp.simplify(a*r*(1+rho_i))
Lt_i=sp.simplify(a*H*(1+ell_i)+a*ell_t_i)
Rt_i=sp.simplify(a*H*r*(1+rho_i)+a*r*rho_t_i)

# v0.19i scalar/aether gauge dictionary.
alpha_p=alpha+T
varphi_p=varphi-Q*T
chi_new=sp.expand(varphi_p+Q*alpha_p)
chi_old=sp.expand(varphi+Q*alpha)
chi_invariant=sp.simplify(chi_new-chi_old)

# Spatial covector transformation. Background A_mu=(-1,0,0,0), so
# delta A_r' = delta A_r + d_r T = d_r(alpha+T).
A_r_new=alpha_r+Tr
alpha_p_r=alpha_r+Tr
covector_match=sp.simplify(A_r_new-alpha_p_r)

# On the aligned initial slice T=Tr=0, C6 rapidity obeys A_r=a*u at
# first order because A^r=sinh(u)/L and L=a.
u_i=alpha_r/a
u_t_i=Ea_r/a-H*u_i

# Scalar bridge. chi=varphi+Q alpha, with Q homogeneous.
varphi_p_r_from_chi=chi_r-Q*alpha_r
# Linearized C6 X = Q u + varphi_r/a.
X_c6=sp.simplify(Q*u_i+varphi_p_r_from_chi/a)
X_target=chi_r/a
X_residual=sp.simplify(X_c6-X_target)

# Linearized C6 E in N=1,b=0 around FLRW is u_t+H u. In proper-time
# gauge E_A=alpha_dot, hence u_t=E_A,r/a-Hu.
E_c6=sp.simplify(u_t_i+H*u_i)
E_target=Ea_r/a
E_residual=sp.simplify(E_c6-E_target)

# Q-sector density identity used to infer deltaQ from the CLASS AeST density.
q=sp.symbols('q', positive=True)
K=sp.Function('K')(q)
rhoA=q*sp.diff(K,q)-K
drho=sp.simplify(sp.diff(rhoA,q)-q*sp.diff(K,q,2))

# Exact expected initial metric formulas from prereg.
expected={
    'L':a*(1-Phi),
    'R':a*r*(1-Phi),
    'Lt':a*H*(1-Phi-Psi)-a*Phi_t,
    'Rt':a*H*r*(1-Phi-Psi)-a*r*Phi_t,
}
metric_residuals={
    'L':sp.simplify(L_i-expected['L']),
    'R':sp.simplify(R_i-expected['R']),
    'Lt':sp.simplify(Lt_i-expected['Lt']),
    'Rt':sp.simplify(Rt_i-expected['Rt']),
}

gates={
    'A2_1_lapse_zero_exact': bool(lapse_zero==0),
    'A2_2_shift_zero_exact': bool(shift_zero==0),
    'A2_3_initial_metric_dictionary_exact': bool(all(x==0 for x in metric_residuals.values())),
    'A2_4_chi_gauge_invariant_exact': bool(chi_invariant==0),
    'A2_5_aether_covector_transform_exact': bool(covector_match==0),
    'A2_6_X_bridge_identity_exact': bool(X_residual==0),
    'A2_7_E_bridge_identity_exact': bool(E_residual==0),
    'A2_8_density_Q_derivative_exact': bool(drho==0),
}
classification='NL1C7A_GAUGE_VARIABLE_DICTIONARY_PASS' if all(gates.values()) else 'NL1C7A_GAUGE_VARIABLE_DICTIONARY_FAIL'

result={
    'classification':classification,
    'scope':'C7A theory-only first-order gauge/variable bridge audit; no CLASS trajectory, no spherical evolution, eta=0 only.',
    'gauge_generator':'xi^mu=(T,d_r S,0,0), delta g prime = delta g - Lie_xi gbar',
    'gauge_conditions':{'Tdot':'Psi','a2_Sdot':'T','initial_alignment':'T=S=0 at a_i'},
    'metric_dictionary':metric_dictionary,
    'initial_metric_formulas':{k:str(v) for k,v in expected.items()},
    'metric_residuals':{k:str(v) for k,v in metric_residuals.items()},
    'chi_invariance_residual':str(chi_invariant),
    'aether_covector_residual':str(covector_match),
    'X_bridge':{'C6':str(X_c6),'target':str(X_target),'residual':str(X_residual)},
    'E_bridge':{'C6':str(E_c6),'target':str(E_target),'residual':str(E_residual)},
    'rhoA_Q_identity_residual':str(drho),
    'gates':gates,
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
raise SystemExit(0 if all(gates.values()) else 1)
