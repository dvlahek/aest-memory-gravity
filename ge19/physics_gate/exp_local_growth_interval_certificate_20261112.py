#!/usr/bin/env python3
"""Fixed Exp sufficient interval certificate for the LOCAL frozen reduced growing root.
No CLASS integration, eta scan, Weyl gain or DES. Requires flat positive-component
FLRW with background -1 <= w_i <= 1/3; uses H(a) <= H0/a**2 for a <= 1.
"""
import argparse
import json
import subprocess
from pathlib import Path
import mpmath as mp

SOURCE_BLOBS = {
    'v019/patch/source/aest_memory.c': '9a522a653a1855eda3cb67e856f9fc10a1e73d54',
    'v019/ini/aest_exp.ini': 'f9a2bde8921a148e063f9657a8ede0a51c6a629d',
    'docs/ge19_20261112_frozen_coupled_scalar_bath_gain_conditional_root.md':
        '9c0886f4842452ead4d47e235b36ebd43508bafc',
}

def source_locks(root):
    for path, want in SOURCE_BLOBS.items():
        p = root / path
        if not p.is_file():
            raise RuntimeError('MISSING_SOURCE: ' + path)
        got = subprocess.check_output(['git', 'hash-object', str(p)],
                                      text=True, cwd=root).strip()
        if got != want:
            raise RuntimeError('SOURCE_CHANGED: ' + path + ': ' + got)
    c = (root / 'v019/patch/source/aest_memory.c').read_text()
    ini = (root / 'v019/ini/aest_exp.ini').read_text()
    for literal in ('k=2.*K2*Z0*Z0*(ex-1.);',
                    'kq=4.*K2*Z0*Z*ex;',
                    'kqq=4.*K2*ex*(1.+2.*zz);',
                    'kq=I0/(a*a*a);'):
        if literal not in c:
            raise RuntimeError('EXP_FORMULA_ANCHOR_CHANGED: ' + literal)
    for literal in ('H0 = 67.32117', 'omega_cdm = 0.1201075',
                    'aest_model = Exp', 'aest_KB = 0.1',
                    'aest_Q0 = 1e-4', 'aest_K2 = 9500',
                    'aest_Z0 = 1e-17'):
        if literal not in ini:
            raise RuntimeError('BENCHMARK_INPUT_CHANGED: ' + literal)
    print('GE19_EXP_INTERVAL_SOURCE_LOCKS_PASS 3', flush=True)

def invert(f, target):
    lo, hi = mp.mpf(0), mp.mpf(16)
    while f(hi) < target:
        hi *= 2
    for _ in range(300):
        mid = (lo + hi) / 2
        if f(mid) > target:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2

def certificate():
    mp.mp.dps = 75
    Q0, Z0, K2 = mp.mpf('1e-4'), mp.mpf('1e-17'), mp.mpf('9500')
    KB, C = mp.mpf('0.1'), mp.mpf('1.9')
    H0 = mp.mpf('67.32117') / mp.mpf('299792.458')
    target = 3 * mp.mpf('0.1201075') / mp.mpf('2997.92458')**2
    Q = lambda z: Q0 + Z0*z
    K = lambda z: 2*K2*Z0**2*(mp.exp(z*z) - 1)
    KQ = lambda z: 4*K2*Z0*z*mp.exp(z*z)
    ca2 = lambda z: Z0*z / (Q(z)*(1 + 2*z*z))
    z1 = invert(lambda z: Q(z)*KQ(z)-K(z), target)
    I0 = KQ(z1)
    amin, amax = mp.mpf('1e-8'), mp.mpf('0.7')
    zmin_a = invert(KQ, I0 / amin**3)
    Qmax = Q0 + mp.mpf('1e-16')
    ca2max = mp.mpf('1.2e-14')
    if not (z1 > 1 and Q(zmin_a) < Qmax and 0 < ca2(z1) < ca2max):
        raise RuntimeError('PARAMETER_ENVELOPES_NOT_CERTIFIED')
    # KQ=I0/a^3. A conservative upper bound on the required
    # positive-real-root threshold is
    # C*(H0/a^2+Qmax)+3*KB*(H0/a^2)^2*ca2max/Q0;
    # dropping negative -3*C*H*ca2 makes this an upper bound.
    # Multiply the strict inequality by positive a^4.
    f = lambda a: I0*a - C*H0*a*a - C*Qmax*a**4 - 3*KB*H0**2*ca2max/Q0
    flo, fhi = f(amin), f(amax)
    # f''=-2*C*H0-12*C*Qmax*a^2<0; f is concave and lies above
    # the straight chord connecting positive endpoint values.
    if not (flo > 0 and fhi > 0 and C > 0 and ca2max < mp.mpf(1)/3):
        raise RuntimeError('INTERVAL_ENDPOINT_CERTIFICATE_FAIL')
    landmarks = []
    for a_str in ('1e-8','1e-4','0.001','0.01','0.1','0.3','0.5','0.7'):
        a = mp.mpf(a_str)
        z = invert(KQ, I0/a**3)
        Hupper = H0/a**2
        threshold = C*(Hupper+Q(z)-3*Hupper*ca2(z)) + \
                    3*KB*Hupper**2*ca2(z)/Q(z)
        ratio = I0/a**3/threshold
        if ratio <= 1:
            raise RuntimeError('LOCAL_THRESHOLD_FAIL_AT_' + a_str)
        landmarks.append({'a':a_str,
                          'KQ_over_threshold_using_H_upper':mp.nstr(ratio,16),
                          'KQ':mp.nstr(I0/a**3,18),
                          'H_upper':mp.nstr(Hupper,18)})
    return {
        'classification':
        'GE19_EXP_SUFFICIENT_LOCAL_ROOT_INTERVAL_PASS_NOT_PHYSICAL_GAIN',
        'fixed_model':'Frozen AeST Exp KB=0.1, Q0=1e-4, K2=9500, Z0=1e-17, omega_cdm=0.1201075',
        'interval_a':['1e-8','0.7'],
        'assumptions':['flat FLRW','positive components with -1<=w_i<=1/3',
          'H(a)<=H0/a^2','finite positive NL0B oscillator weights and frequencies',
          'frozen reduced scalar+aether+bath operator; Delta_A external for root criterion'],
        'calibration':{'I0':mp.nstr(I0,25),'Z_at_today':mp.nstr(z1,24),
          'Z_at_a_min':mp.nstr(zmin_a,24),'H0_Mpc_inverse':mp.nstr(H0,24)},
        'conservative_envelope':{'Qmax':mp.nstr(Qmax,24),
          'ca2max':mp.nstr(ca2max,14),'Qmin':mp.nstr(Q0,24)},
        'proof':'f(a)=I0*a-C*H0*a^2-C*Qmax*a^4-3*KB*H0^2*ca2max/Q0; f concave, endpoint positive, hence positive throughout',
        'endpoint_f_margin':{'a_min':mp.nstr(flo,19),'a_max':mp.nstr(fhi,19)},
        'landmarks':landmarks,
        'actual_full_background_H_solved':False,
        'full_constraint_projected_all_species_root_certified':False,
        'physical_adiabatic_mode_excitation_certified':False,
        'time_dependent_fundamental_matrix_gain_certified':False,
        'DES_detection':False,'production_physics_go':False
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2])
    p.add_argument('--no-source-lock',action='store_true')
    p.add_argument('--out',type=Path)
    a=p.parse_args()
    if not a.no_source_lock:
        source_locks(a.repo_root.resolve())
    r=certificate()
    r['source_locks_executed']=not a.no_source_lock
    r['source_blobs']=SOURCE_BLOBS if not a.no_source_lock else {}
    print('GE19_EXP_FROZEN_LOCAL_ROOT_INTERVAL_PASS',flush=True)
    print('GE19_FULL_PHYSICS_GO False',flush=True)
    if a.out:
        dst=a.out.resolve()
        if dst.exists():
            raise RuntimeError('REFUSE_OUTPUT_OVERWRITE')
        dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
        print('GE19_EXP_LOCAL_INTERVAL_RESULT',dst,flush=True)

if __name__=='__main__':
    main()
