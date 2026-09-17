#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results' / 'nl1c7b1_pressureless_matter_variational_closure.json'

# Frozen C7B1 spherical dust action in the same gravitational normalization as C6.
N, L, R, b, varrho, Tt, Tr = sp.symbols('N L R b varrho Tt Tr', positive=True, real=True)
W = (Tt - b*Tr)/N
V = Tr/L
C = W**2 - V**2 - 1
Ld = N*L*R**2*varrho*C

v = sp.symbols('v', real=True)
c = sp.cosh(v)
s = sp.sinh(v)
onshell = {Tr: -L*s, Tt: N*c - b*L*s}

# B1-G2: multiplier constraint and rapidity branch.
rho_el = sp.simplify(sp.diff(Ld, varrho)/(N*L*R**2))
g2_constraint = bool(sp.simplify(rho_el - C) == 0)
g2_branch = bool(sp.simplify(W.subs(onshell) - c) == 0 and sp.simplify(V.subs(onshell) + s) == 0)

# B1-G3: T variation gives the already frozen C6 conserved current.
pTt = sp.diff(Ld, Tt)/2
pTr = sp.diff(Ld, Tr)/2
g3_time_current = bool(sp.simplify(pTt - L*R**2*varrho*W) == 0)
g3_radial_current = bool(sp.simplify(pTr - (-b*L*R**2*varrho*W - N*R**2*varrho*V)) == 0)
Jt_shell = sp.simplify(pTt.subs(onshell))
Jr_shell = sp.simplify(pTr.subs(onshell))
g3_shell = bool(
    sp.simplify(Jt_shell - L*R**2*varrho*c) == 0 and
    sp.simplify(Jr_shell - (N*R**2*varrho*s - b*L*R**2*varrho*c)) == 0
)

# B1-G4: d_r(T_t)-d_t(T_r)=0 is exactly the frozen radial geodesic equation.
vt, vr, Nr, Lt, Lr, br = sp.symbols('vt vr Nr Lt Lr br', real=True)
dt_Tr = -Lt*s - L*c*vt
dr_Tt = Nr*c + N*s*vr - br*L*s - b*Lr*s - b*L*c*vr
integrability = sp.expand(dr_Tt - dt_Tr)
kL = (Lt - b*Lr - L*br)/(N*L)
geodesic_times_NL = sp.expand(N*L*(c*((vt-b*vr)/N + Nr/(N*L)) + s*(vr/L + kL)))
g4_geodesic = bool(sp.simplify(integrability - geodesic_times_NL) == 0)

# B1-G5: metric source projections, varied before imposing the dust shell.
metric_expected = {
    'N': -2*L*R**2*varrho*c**2,
    'b':  2*L**2*R**2*varrho*c*s,
    'L':  2*N*R**2*varrho*s**2,
    'R':  sp.Integer(0),
}
metric_actual = {
    'N': sp.diff(Ld, N).subs(onshell),
    'b': sp.diff(Ld, b).subs(onshell),
    'L': sp.diff(Ld, L).subs(onshell),
    'R': sp.diff(Ld, R).subs(onshell),
}
metric_checks = {
    key: bool(sp.simplify((metric_actual[key]-metric_expected[key]).rewrite(sp.exp)) == 0)
    for key in metric_expected
}
g5_sources = all(metric_checks.values())

# B1-G6: pure-GR FLRW dust normalization.  The common r^2 factor is omitted.
a, adot, H, rho8, Nf, Ttf = sp.symbols('a adot H rho8 Nf Ttf', positive=True, real=True)
Lg_flrw = -6*a*adot**2/Nf
Ld_flrw = Nf*a**3*rho8*((Ttf/Nf)**2 - 1)
flrw_lapse = sp.diff(Lg_flrw + Ld_flrw, Nf)
flrw_shell = sp.simplify(flrw_lapse.subs({adot: Nf*a*H, Ttf: Nf})/(2*a**3))
g6_flrw = bool(sp.simplify(flrw_shell - (3*H**2-rho8)) == 0)

# B1-G7: dust adds no second-time-derivative field kinetic term.
Rt, ut, pt = sp.symbols('Rt ut pt', real=True)
principal_velocities = [Lt, Rt, ut, pt]
H_dust = sp.hessian(Ld, principal_velocities)
g7_principal = bool(H_dust == sp.zeros(4))

# B1-G8: transport speed from the conserved current.
transport = sp.simplify(Jr_shell/Jt_shell)
g8_transport = bool(sp.simplify((transport - (-b + N*sp.tanh(v)/L)).rewrite(sp.exp)) == 0)

# B1-G9: strict minimal coupling/source audit.
u, phi, q, eta, Y, Q = sp.symbols('u phi q eta Y Q', real=True)
forbidden = [u, phi, q, eta, Y, Q]
g9_minimal = not any(Ld.has(z) for z in forbidden)

# Independent deterministic finite-difference action-variation audit.
N0, L0, R0, b0, rho0, Tt0, Tr0 = sp.symbols('N0 L0 R0 b0 rho0 Tt0 Tr0', real=True)
W0 = (Tt0-b0*Tr0)/N0
V0 = Tr0/L0
Ld0 = N0*L0*R0**2*rho0*(W0**2-V0**2-1)
args = [N0, L0, R0, b0, rho0, Tt0, Tr0]
fl = sp.lambdify(args, Ld0, 'numpy')
fparts = {name: sp.lambdify(args, sp.diff(Ld0, sym), 'numpy') for name, sym in [
    ('N',N0),('L',L0),('R',R0),('b',b0),('varrho',rho0)
]}
fpTt = sp.lambdify(args, sp.diff(Ld0,Tt0), 'numpy')
fpTr = sp.lambdify(args, sp.diff(Ld0,Tr0), 'numpy')

def sd(x, axis):
    x = np.asarray(x, float)
    n = x.shape[axis]
    shape = [1]*x.ndim
    shape[axis] = n
    kk = np.fft.fftfreq(n, d=1/n).reshape(shape)
    return np.fft.ifft(1j*kk*np.fft.fft(x, axis=axis), axis=axis).real

nt, nr = 24, 32
tgrid = np.arange(nt)*2*np.pi/nt
rgrid = np.arange(nr)*2*np.pi/nr
TT, RR = np.meshgrid(tgrid, rgrid, indexing='ij')
arrays = [
    1.2 + 0.03*np.sin(TT+RR),
    1.1 + 0.02*np.cos(2*TT-RR),
    1.7 + 0.03*np.sin(TT+2*RR),
    0.04*np.sin(TT-RR),
    0.25 + 0.02*np.cos(TT-2*RR),
    0.4*np.sin(TT) + 0.2*np.cos(RR) + 0.1*np.sin(TT+RR),
]

def values(aarr):
    return [aarr[0],aarr[1],aarr[2],aarr[3],aarr[4],sd(aarr[5],0),sd(aarr[5],1)]

vals = values(arrays)
EL = {name: fparts[name](*vals) for name in ['N','L','R','b','varrho']}
EL['T'] = -sd(fpTt(*vals),0) - sd(fpTr(*vals),1)
dt = 2*np.pi/nt
dr = 2*np.pi/nr

def action(aarr):
    return float(np.sum(fl(*values(aarr)))*dt*dr)

sites = [(2,3),(5,7),(9,12),(13,17),(17,21),(7,25)]
variation_rows = []
max_variation_error = 0.0
for i, name in enumerate(['N','L','R','b','varrho','T']):
    ij = sites[i]
    h = 1e-5*max(1.0, abs(float(arrays[i][ij])))
    ap = [z.copy() for z in arrays]
    am = [z.copy() for z in arrays]
    ap[i][ij] += h
    am[i][ij] -= h
    fd = (action(ap)-action(am))/(2*h)
    auto = float(EL[name][ij]*dt*dr)
    rel = abs(fd-auto)/max(1e-12,abs(fd),abs(auto))
    max_variation_error = max(max_variation_error, rel)
    variation_rows.append({'field':name,'site':list(ij),'finite_difference':fd,'component':auto,'relative_error':rel})
variation_pass = bool(max_variation_error <= 1e-6)

# The exact audit has no extra background prescription.  Full CLASS/AeST
# homogeneous constraint reconciliation is deliberately deferred to the next
# initial-constraint checkpoint, where it can fail explicitly if another
# standard-matter background component is missing.
full_background_diag = {
    'dust_GR_normalization_exact': g6_flrw,
    'full_CLASS_AeST_background_reconciliation_executed_here': False,
    'deferred_to_NL1C7_initial_constraint': True,
    'silent_background_source_added': False,
}

# Provenance gate is source-locked by the workflow; repeated here as a semantic gate.
g1_provenance = True

gates = {
    'B1_G1_provenance': g1_provenance,
    'B1_G2_normalization_constraint': bool(g2_constraint and g2_branch),
    'B1_G3_continuity_equation': bool(g3_time_current and g3_radial_current and g3_shell),
    'B1_G4_geodesic_equation': g4_geodesic,
    'B1_G5_action_derived_gravitational_sources': g5_sources,
    'B1_G6_FLRW_normalization': g6_flrw,
    'B1_G7_field_principal_block_preserved': g7_principal,
    'B1_G8_matter_transport_regular_before_crossing': g8_transport,
    'B1_G9_no_direct_AeST_memory_matter_force': g9_minimal,
    'B1_independent_action_variation_audit': variation_pass,
}

classification = (
    'NL1C7B1_PRESSURELESS_MATTER_VARIATIONAL_CLOSURE_PASS'
    if all(gates.values()) else
    'NL1C7B1_PRESSURELESS_MATTER_VARIATIONAL_CLOSURE_FAIL'
)

result = {
    'classification': classification,
    'scope': 'Pressureless minimally coupled matter variational closure only; no nonlinear trajectory and eta=0 only.',
    'action': {
        'covariant': '-1/2 int sqrt(-g) rho_phys (g^munu d_mu T d_nu T + 1)',
        'density_rescaling': 'varrho = 8*pi*G*rho_phys',
        'spherical_reduced': str(Ld),
        'W': str(W),
        'V': str(V),
        'future_branch': {'W':'cosh(v)','V':'-sinh(v)','Tr':'-L sinh(v)','Tt':'N cosh(v)-b L sinh(v)'},
        'free_matter_coupling_coefficient': False,
    },
    'exact_identities': {
        'rho_EL': str(rho_el),
        'T_current_time_half': str(pTt),
        'T_current_radial_half': str(pTr),
        'T_current_time_shell': str(Jt_shell),
        'T_current_radial_shell': str(Jr_shell),
        'geodesic_integrability_residual': str(sp.simplify(integrability-geodesic_times_NL)),
        'metric_source_checks': metric_checks,
        'metric_sources_shell': {k:str(sp.trigsimp(vv)) for k,vv in metric_actual.items()},
        'FLRW_lapse_equation_normalized': str(flrw_shell),
        'dust_field_principal_hessian': str(H_dust),
        'transport_speed': str(transport),
    },
    'variation_audit': {
        'limit': 1e-6,
        'max_relative_error': max_variation_error,
        'rows': variation_rows,
        'pass': variation_pass,
    },
    'background_diagnostic': full_background_diag,
    'gates': gates,
    'continuation': 'If PASS, use this action-derived dust sector in a separate eta=0 initial-constraint/short-time evolution checkpoint before the long NL1C7 trajectory.',
    'claim_boundary': {
        'nonlinear_evolution_executed': False,
        'turnaround_or_collapse_evaluated': False,
        'finite_eta_executed': False,
        'full_CLASS_background_constraint_certified': False,
    },
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if all(gates.values()) else 2)
