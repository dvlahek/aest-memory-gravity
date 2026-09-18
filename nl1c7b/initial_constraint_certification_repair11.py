#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair02 as r2
import nl1c7b.initial_constraint_certification_repair09 as r9

R8_NPZ_SHA256 = '4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R8_JSON_SHA256 = '054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R10_JSON_SHA256 = 'f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d'
R10_CLASS = 'NL1C7B4_REPAIR10_RAW_SOURCE_LOCALIZATION_DIAGNOSTIC_PASS'
IMPL_LIMIT = 1e-10
HOTSPOT_LIMIT = 1e-12
SLOPE_MIN = 1.8
SLOPE_MAX = 2.2
LAMBDAS = (1.0, 0.5, 0.25, 0.125)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def rel_or_abs(a, b, tol):
    a = float(a)
    b = float(b)
    ae = abs(a - b)
    re = ae / max(abs(a), abs(b), 1e-300)
    return bool(np.isfinite(ae) and np.isfinite(re) and (ae <= tol or re <= tol)), ae, re


def normalized_array_error(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    num = float(np.max(np.abs(a - b)))
    den = max(float(np.max(np.abs(a))), float(np.max(np.abs(b))), 1e-300)
    return num / den


def symbolic_audit():
    N,L,R,b,u,Lt,Rt,ut,pt,Nr,Lr,Rr,br,ur,pr = sp.symbols(
        'N L R b u Lt Rt ut pt Nr Lr Rr br ur pr', real=True
    )
    KB,C = sp.symbols('KB C', real=True)
    c = sp.cosh(u)
    s = sp.sinh(u)
    kL = (Lt - b*Lr - L*br)/(N*L)
    sigma = (pt - b*pr)/N
    X = s*sigma + c*pr/L
    E = c*((ut-b*ur)/N + Nr/(N*L)) + s*(kL + ur/L)
    P = N*L*R**2
    LE2 = P*KB*E**2
    LEX = P*2*C*E*X
    gauge = {N:1, b:0, Nr:0, br:0}

    Eg = sp.simplify(E.subs(gauge))
    Xg = sp.simplify(X.subs(gauge))
    Eb = sp.simplify(sp.diff(E,b).subs(gauge))
    Ebr = sp.simplify(sp.diff(E,br).subs(gauge))
    Xb = sp.simplify(sp.diff(X,b).subs(gauge))
    Xbr = sp.simplify(sp.diff(X,br).subs(gauge))

    targets = {
        'E_gauge': c*ut + s*(Lt/L + ur/L),
        'X_gauge': s*pt + c*pr/L,
        'dE_db': -c*ur - s*Lr/L,
        'dE_dbr': -s,
        'dX_db': -s*pr,
        'dX_dbr': sp.Integer(0),
        'dLE2_db': 2*KB*L*R**2*Eg*Eb,
        'dLE2_dbr': -2*KB*L*R**2*Eg*s,
        'dLEX_db': 2*C*L*R**2*(Eb*Xg - Eg*s*pr),
        'dLEX_dbr': -2*C*L*R**2*s*Xg,
    }
    observed = {
        'E_gauge': Eg,
        'X_gauge': Xg,
        'dE_db': Eb,
        'dE_dbr': Ebr,
        'dX_db': Xb,
        'dX_dbr': Xbr,
        'dLE2_db': sp.simplify(sp.diff(LE2,b).subs(gauge)),
        'dLE2_dbr': sp.simplify(sp.diff(LE2,br).subs(gauge)),
        'dLEX_db': sp.simplify(sp.diff(LEX,b).subs(gauge)),
        'dLEX_dbr': sp.simplify(sp.diff(LEX,br).subs(gauge)),
    }
    identity_rows = {}
    identities_ok = True
    for name in targets:
        ok = bool(sp.simplify(observed[name] - targets[name]) == 0)
        identity_rows[name] = ok
        identities_ok &= ok

    # Formal perturbation audit in the zero-N_r initial gauge.
    rr,eps,a,H,Q = sp.symbols('r epsilon a H Q', real=True, nonzero=True)
    lf = sp.Function('l')(rr)
    R1 = sp.Function('R1')(rr)
    ltf = sp.Function('lt1')(rr)
    u1 = sp.Function('u1')(rr)
    ut1 = sp.Function('ut1')(rr)
    p1 = sp.Function('p1')(rr)
    phi1 = sp.Function('phi1')(rr)

    Le = a + eps*lf
    Re = a*rr + eps*R1
    Lte = a*H + eps*ltf
    ue = eps*u1
    ute = eps*ut1
    pte = Q + eps*p1
    pre = eps*sp.diff(phi1,rr)
    Lre = eps*sp.diff(lf,rr)
    ure = eps*sp.diff(u1,rr)
    ce = sp.cosh(ue)
    se = sp.sinh(ue)
    Ee = ce*ute + se*(Lte/Le + ure/Le)
    Xe = se*pte + ce*pre/Le
    Ebe = -ce*ure - se*Lre/Le
    Ebre = -se
    Xbe = -se*pre

    fb_e2 = 2*KB*Le*Re**2*Ee*Ebe
    fbr_e2 = 2*KB*Le*Re**2*Ee*Ebre
    fb_ex = 2*C*Le*Re**2*(Ebe*Xe + Ee*Xbe)
    fbr_ex = -2*C*Le*Re**2*se*Xe
    cm_e2 = sp.expand(fb_e2 - sp.diff(fbr_e2,rr))
    cm_ex = sp.expand(fb_ex - sp.diff(fbr_ex,rr))

    lin_e2 = sp.simplify(sp.diff(cm_e2,eps).subs(eps,0))
    lin_ex = sp.simplify(sp.diff(cm_ex,eps).subs(eps,0))
    quad_e2 = sp.simplify(sp.diff(cm_e2,eps,2).subs(eps,0)/2)
    quad_ex = sp.simplify(sp.diff(cm_ex,eps,2).subs(eps,0)/2)
    E1 = ut1 + H*u1
    X1 = Q*u1 + sp.diff(phi1,rr)/a
    target_quad_e2 = 2*KB*a**3*u1*sp.diff(rr**2*E1,rr)
    target_quad_ex = 2*C*a**3*u1*sp.diff(rr**2*X1,rr)

    first_order = {
        'E2_linear_zero': bool(lin_e2 == 0),
        'EX_linear_zero': bool(lin_ex == 0),
    }
    quadratic = {
        'E2_quadratic_closed_form': bool(sp.simplify(quad_e2-target_quad_e2) == 0),
        'EX_quadratic_closed_form': bool(sp.simplify(quad_ex-target_quad_ex) == 0),
    }
    return {
        'gauge_identities': identity_rows,
        'gauge_identities_pass': bool(identities_ok),
        'first_order': first_order,
        'first_order_pass': bool(all(first_order.values())),
        'quadratic': quadratic,
        'quadratic_pass': bool(all(quadratic.values())),
        'first_order_source_statement': {
            'AeST_E2': 'zero',
            'AeST_EX': 'zero',
        },
        'quadratic_closed_forms': {
            'AeST_E2': '2*K_B*a^3*u1*d_r(r^2*E1)',
            'AeST_EX': '2*C*a^3*u1*d_r(r^2*X1)',
            'E1': 'udot1 + H*u1',
            'X1': 'Q*u1 + phi1_r/a',
        },
    }


def exact_esector_arrays(st, qbg, funcs):
    r = np.asarray(st['r'],float)
    D = b4.dmat(r)
    n = len(r)
    L = b4.AI + np.asarray(st['L_minus_a'],float)
    R = b4.AI*r + np.asarray(st['R_minus_ar'],float)
    Lt = b4.AI*b4.H_DIRECT + np.asarray(st['Ldot_minus_aH'],float)
    Rt = b4.AI*b4.H_DIRECT*r + np.asarray(st['Rdot_minus_aHr'],float)
    u = np.asarray(st['u'],float)
    ut = np.asarray(st['udot'],float)
    pr = D @ np.asarray(st['phi'],float)
    Lr = D @ L
    Rr = D @ R
    ur = D @ u
    dq = np.asarray(st['phidot_minus_Q'],float)
    c = np.cosh(u)
    s = np.sinh(u)
    qtarget = qbg + dq
    pt = (qtarget - s*pr/L)/c
    args = [L,R,u,Lt,Rt,ut,pt,Lr,Rr,ur,pr]

    frozen = {}
    for name in ('AeST_E2','AeST_EX'):
        fs = funcs[name]
        fb = r2.arrval(fs[2],args,n)
        fbr = r2.arrval(fs[3],args,n)
        fbr = np.array(fbr,copy=True)
        fbr[0] = 0.0
        frozen[name] = np.asarray(fb - D@fbr,float)

    E = c*ut + s*(Lt/L + ur/L)
    X = s*pt + c*pr/L
    Eb = -c*ur - s*Lr/L
    Ebr = -s
    Xb = -s*pr

    fb_e2 = 2.0*b4.KB*L*R**2*E*Eb
    fbr_e2 = 2.0*b4.KB*L*R**2*E*Ebr
    fb_ex = 2.0*b4.C*L*R**2*(Eb*X + E*Xb)
    fbr_ex = -2.0*b4.C*L*R**2*s*X
    fbr_e2 = np.array(fbr_e2,copy=True); fbr_e2[0]=0.0
    fbr_ex = np.array(fbr_ex,copy=True); fbr_ex[0]=0.0
    closed = {
        'AeST_E2': np.asarray(fb_e2 - D@fbr_e2,float),
        'AeST_EX': np.asarray(fb_ex - D@fbr_ex,float),
    }
    return frozen, closed


def scaled_esector_arrays(st, qbg, lam):
    r = np.asarray(st['r'],float)
    D = b4.dmat(r)
    a = b4.AI
    L0 = a + np.asarray(st['L_minus_a'],float)
    R0 = a*r + np.asarray(st['R_minus_ar'],float)
    Lt0 = a*b4.H_DIRECT + np.asarray(st['Ldot_minus_aH'],float)
    u0 = np.asarray(st['u'],float)
    ut0 = np.asarray(st['udot'],float)
    phi0 = np.asarray(st['phi'],float)
    dq0 = np.asarray(st['phidot_minus_Q'],float)

    L = a + lam*(L0-a)
    R = a*r + lam*(R0-a*r)
    Lt = a*b4.H_DIRECT + lam*(Lt0-a*b4.H_DIRECT)
    u = lam*u0
    ut = lam*ut0
    phi = lam*phi0
    dq = lam*dq0

    pr = D@phi
    Lr = D@L
    ur = D@u
    c = np.cosh(u)
    s = np.sinh(u)
    qtarget = qbg + dq
    pt = (qtarget - s*pr/L)/c
    E = c*ut + s*(Lt/L + ur/L)
    X = s*pt + c*pr/L
    Eb = -c*ur - s*Lr/L
    Ebr = -s
    Xb = -s*pr

    fb_e2 = 2.0*b4.KB*L*R**2*E*Eb
    fbr_e2 = 2.0*b4.KB*L*R**2*E*Ebr
    fb_ex = 2.0*b4.C*L*R**2*(Eb*X + E*Xb)
    fbr_ex = -2.0*b4.C*L*R**2*s*X
    fbr_e2=np.array(fbr_e2,copy=True); fbr_e2[0]=0.0
    fbr_ex=np.array(fbr_ex,copy=True); fbr_ex[0]=0.0
    return {
        'AeST_E2': np.asarray(fb_e2-D@fbr_e2,float),
        'AeST_EX': np.asarray(fb_ex-D@fbr_ex,float),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair08-json',required=True)
    ap.add_argument('--repair08-npz',required=True)
    ap.add_argument('--repair10-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    cov=json.loads(Path(a.coverage_json).read_text())
    r8j=json.loads(Path(a.repair08_json).read_text())
    r10j=json.loads(Path(a.repair10_json).read_text())
    off=np.load(a.repair08_npz)

    r8_npz_sha=sha256_file(a.repair08_npz)
    r8_json_sha=sha256_file(a.repair08_json)
    r10_json_sha=sha256_file(a.repair10_json)

    z=rec.read_trace(a.trace)
    ks,gs=rec.groups(z)
    tv_rec=rec.at_ai(gs,'pchip')
    ks_b4,gs_b4=b4.groups(b4.read_trace(a.trace))
    tv_b4=b4.at_ai(gs_b4)
    h=float(cov['h'])

    r8g=r8j.get('gates',{})
    r10g=r10j.get('gates',{})
    g1=bool(
        r8_npz_sha==R8_NPZ_SHA256
        and r8_json_sha==R8_JSON_SHA256
        and r10_json_sha==R10_JSON_SHA256
        and r8j.get('classification')=='NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED'
        and len(r8g)==10 and all(r8g.values())
        and r10j.get('classification')==R10_CLASS
        and len(r10g)==6 and all(r10g.values())
        and cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max')==0
        and cov.get('n_native_times')==179
        and len(ks)==128 and np.array_equal(ks,ks_b4)
    )

    sym=symbolic_audit()
    g2=bool(sym['gauge_identities_pass'])
    g3=bool(sym['first_order_pass'])
    g4=bool(sym['quadratic_pass'])

    scalar_ai,scalar_independent,scalar_finite,_=r8.scalar_composites_at_ai(ks,gs,'pchip')
    states={}
    for scale in b4.SCALES:
        states[(scale,256)]=r9.load_primary_state(off,scale)
        states[(scale,512)]=r9.repaired_state_nr(scale,512,ks,h,tv_b4,tv_rec,scalar_ai)

    qbg=b4.stable_q_from_kq(float(np.median(tv_b4['KQ'])))
    funcs,_,_=r1.build_nonK()

    implementation_rows=[]
    arrays={}
    g5=True
    for scale in b4.SCALES:
        for nr in (256,512):
            frozen,closed=exact_esector_arrays(states[(scale,nr)],qbg,funcs)
            arrays[(float(scale),int(nr))]=frozen
            mask=np.arange(len(states[(scale,nr)]['r']))>0
            row={'scale_hinv_Mpc':float(scale),'Nr':int(nr)}
            for name in ('AeST_E2','AeST_EX'):
                err=normalized_array_error(frozen[name][mask],closed[name][mask])
                row[name+'_normalized_error']=err
                row[name+'_pass']=bool(np.isfinite(err) and err<=IMPL_LIMIT)
                g5 &= row[name+'_pass']
            implementation_rows.append(row)

    hotspot_rows=[]
    g6=bool(len(r10j.get('localization_rows',[]))==54)
    for row in r10j.get('localization_rows',[]):
        scale=float(row['scale_hinv_Mpc']); nr=int(row['Nr'])
        idx=int(row['M_hotspot']['index'])
        arr=arrays[(scale,nr)]
        outrow={'scale_hinv_Mpc':scale,'Nr':nr,'Y_kind':row['Y_kind'],'beta0':float(row['beta0']),'index':idx}
        for name in ('AeST_E2','AeST_EX'):
            observed=float(arr[name][idx])
            expected=float(row['M_hotspot']['signed_sources'][name])
            ok,ae,re=rel_or_abs(observed,expected,HOTSPOT_LIMIT)
            outrow[name+'_observed']=observed
            outrow[name+'_repair10']=expected
            outrow[name+'_abs_error']=ae
            outrow[name+'_relative_error']=re
            outrow[name+'_pass']=ok
            g6 &= ok
        hotspot_rows.append(outrow)

    scaling_rows=[]
    g7=True
    for scale in b4.SCALES:
        for nr in (256,512):
            st=states[(scale,nr)]
            mask=np.arange(len(st['r']))>0
            norms={name:[] for name in ('AeST_E2','AeST_EX')}
            for lam in LAMBDAS:
                aa=scaled_esector_arrays(st,qbg,lam)
                for name in norms:
                    norms[name].append(float(np.linalg.norm(aa[name][mask])))
            row={'scale_hinv_Mpc':float(scale),'Nr':int(nr),'lambdas':list(LAMBDAS)}
            for name in norms:
                slopes=[]
                for x,y in zip(norms[name][:-1],norms[name][1:]):
                    p=float(math.log(x/y,2.0)) if x>0 and y>0 and np.isfinite(x) and np.isfinite(y) else float('nan')
                    slopes.append(p)
                    g7 &= bool(np.isfinite(p) and SLOPE_MIN<=p<=SLOPE_MAX)
                row[name+'_norms']=norms[name]
                row[name+'_adjacent_log2_slopes']=slopes
            scaling_rows.append(row)

    fourier_consistency=bool(g3 and sym['first_order_source_statement']['AeST_E2']=='zero' and sym['first_order_source_statement']['AeST_EX']=='zero')
    claim_boundary={
        'state_written_or_projected':False,
        'coefficient_fitted_or_rescaled':False,
        'source_inserted_or_removed':False,
        'sign_changed':False,
        'historical_threshold_changed':False,
        'radial_points_removed':False,
        'Y_beta_or_scale_selected':False,
        'nonlinear_evolution_executed':False,
        'finite_eta_executed':False,
        'B4_pass_claimed':False,
        'observational_detection_claimed':False,
    }
    g8=bool(fourier_consistency and not any(claim_boundary.values()))

    gates={
        'R11_G1_frozen_provenance':g1,
        'R11_G2_exact_gauge_shift_identities':g2,
        'R11_G3_first_order_vanishing':g3,
        'R11_G4_quadratic_coefficients':g4,
        'R11_G5_frozen_implementation_equivalence':bool(g5),
        'R11_G6_Repair10_hotspot_reproduction':bool(g6),
        'R11_G7_quadratic_amplitude_scaling':bool(g7),
        'R11_G8_linear_Fourier_consistency_and_claim_boundary':g8,
    }

    if all(gates.values()):
        cls='NL1C7B4_REPAIR11_ESECTOR_ANALYTIC_COVARIANT_AUDIT_PASS'; rc=0
    elif g1 and g2 and g3 and g4 and (not g5 or not g6):
        cls='NL1C7B4_REPAIR11_ESECTOR_INTERFACE_MISMATCH'; rc=2
    else:
        cls='NL1C7B4_REPAIR11_IMPLEMENTATION_FAIL'; rc=2

    all_slopes=[]
    for row in scaling_rows:
        all_slopes += row['AeST_E2_adjacent_log2_slopes']
        all_slopes += row['AeST_EX_adjacent_log2_slopes']

    result={
        'classification':cls,
        'scope':'Repair11 analytic/covariant audit of frozen AeST E2 and EX radial-momentum contributions on B3/Repair08; no state repair or evolution.',
        'provenance':{
            'repair08_npz_sha256':r8_npz_sha,
            'repair08_json_sha256':r8_json_sha,
            'repair10_json_sha256':r10_json_sha,
            'repair10_result_freeze_commit':'de03f563ee3e8700b3159be5a46b73633c85db8d',
            'repair11_prereg_commit':'02e1e7eaffd08aa289830810250057314594b9cf',
        },
        'symbolic_audit':sym,
        'implementation_equivalence':{
            'limit':IMPL_LIMIT,
            'rows':implementation_rows,
            'pass':bool(g5),
        },
        'repair10_hotspot_reproduction':{
            'limit':HOTSPOT_LIMIT,
            'rows':hotspot_rows,
            'pass':bool(g6),
        },
        'amplitude_scaling':{
            'lambda_values':list(LAMBDAS),
            'slope_interval':[SLOPE_MIN,SLOPE_MAX],
            'rows':scaling_rows,
            'min_slope':float(min(all_slopes)) if all_slopes else float('nan'),
            'max_slope':float(max(all_slopes)) if all_slopes else float('nan'),
            'pass':bool(g7),
        },
        'linear_fourier_consistency':{
            'represented_source':'a[varrho_b theta_b + Q K_Q theta_A]',
            'AeST_E2_first_order_source':'zero',
            'AeST_EX_first_order_source':'zero',
            'E_sector_absence_from_linear_source_consistent':fourier_consistency,
        },
        'state_anchor':{
            'scalar_canonical_vs_independent_at_ai_relative_L2':r9.rel_sym(scalar_ai,scalar_independent),
            'scalar_finite':bool(scalar_finite),
        },
        'gates':gates,
        'claim_boundary':claim_boundary,
        'interpretation_boundary':{
            'Repair10_E2_dominance_reinterpreted_as_quadratic_if_pass':bool(all(gates.values())),
            'B4_passed':False,
            'model_coefficient_error_claimed':False,
            'linear_interface_error_claimed':False,
        },
    }

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
