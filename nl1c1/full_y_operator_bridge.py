#!/usr/bin/env python3
from pathlib import Path
import json
import math
import numpy as np

OUT=Path('results'); OUT.mkdir(exist_ok=True)
L=2*np.pi
BETAS=[1.0,0.5,0.1]
KINDS=['simple','exponential','sharp']
XTEST=np.array([1e-8,1e-6,1e-4,1e-2,1.0,1e2,1e4,1e8,1e10],float)
N1=[512,1024]
N3=32


def rel_l2(a,b):
    a=np.asarray(a); b=np.asarray(b)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(b),1e-300))


def jfun(x,beta,kind):
    x=np.asarray(x,float); A=1.0+beta
    if kind=='simple':
        return x/(A+beta*x)
    if kind=='exponential':
        y=beta*x/A
        return -np.expm1(-y)/beta
    if kind=='sharp':
        # Algebraically identical to
        # (beta*x+A-|beta*x-A|)/(2*beta*A), but evaluated piecewise to
        # avoid catastrophic cancellation for x >> A/beta.
        return np.minimum(x/A,1.0/beta)
    raise ValueError(kind)


def Jfun_x(x,beta,kind):
    """Integrated J with a0=1 dimensionless audit normalization and J(0)=0."""
    x=np.asarray(x,float); A=1.0+beta
    if kind=='simple':
        return 2.0*(x*x/(2*beta)-A*x/(beta*beta)+(A*A/beta**3)*np.log1p(beta*x/A))
    if kind=='exponential':
        c=beta/A; y=c*x
        one_minus = -np.expm1(-y)-y*np.exp(-y)  # 1-(1+y)e^-y
        return (2.0/beta)*(x*x/2.0-one_minus/(c*c))
    if kind=='sharp':
        xt=A/beta
        lo=2.0*x**3/(3.0*A)
        hi=x*x/beta-A*A/(3.0*beta**3)
        return np.where(x<=xt,lo,hi)
    raise ValueError(kind)


def kvec(n):
    return 2*np.pi*np.fft.fftfreq(n,d=L/n)


def mask1(n):
    m=np.fft.fftfreq(n)*n
    return (np.abs(m)<=n/3.0+1e-12).astype(float)


def mask3(n):
    m=np.fft.fftfreq(n)*n
    a,b,c=np.meshgrid(m,m,m,indexing='ij')
    return ((np.abs(a)<=n/3.0+1e-12)&(np.abs(b)<=n/3.0+1e-12)&(np.abs(c)<=n/3.0+1e-12)).astype(float)


def seed1(n):
    x=np.arange(n)*L/n
    return x,.7*np.cos(3*x)+.2*np.sin(5*x)+.11*np.cos(11*x)


def grad1(chi):
    k=kvec(len(chi)); return np.fft.ifft(1j*k*np.fft.fft(chi)).real


def scale_xrms_1d(chi,target):
    g=grad1(chi); xr=float(np.sqrt(np.mean(g*g)))
    return chi*(target/max(xr,1e-300))


def operator1d(chi,beta,kind):
    n=len(chi); k=kvec(n); ch=np.fft.fft(chi); g=np.fft.ifft(1j*k*ch).real
    flux=jfun(np.abs(g),beta,kind)*g
    fh=np.fft.fft(flux)*mask1(n)
    src=np.fft.ifft(1j*k*fh).real
    return src,g


def low_coeffs(a,mmax=32):
    return (np.fft.fft(a)/len(a))[:mmax+1]


def grids3(n):
    kv=kvec(n); return np.meshgrid(kv,kv,kv,indexing='ij')


def scale_xrms_3d(chi,target):
    K=grids3(chi.shape[0]); h=np.fft.fftn(chi)
    grad=[np.fft.ifftn(1j*Ki*h).real for Ki in K]
    xr=float(np.sqrt(np.mean(sum(g*g for g in grad))))
    return chi*(target/max(xr,1e-300))


def operator3d(chi,beta,kind):
    n=chi.shape[0]; K=grids3(n); h=np.fft.fftn(chi); m=mask3(n)
    grad=[np.fft.ifftn(1j*Ki*h).real for Ki in K]
    mag=np.sqrt(sum(g*g for g in grad)); jf=jfun(mag,beta,kind)
    src=np.zeros_like(chi)
    for Ki,g in zip(K,grad):
        fh=np.fft.fftn(jf*g)*m
        src += np.fft.ifftn(1j*Ki*fh).real
    return src,grad


def variational(chi,src,grad,beta,kind):
    if isinstance(grad,(list,tuple)):
        mag=np.sqrt(sum(g*g for g in grad)); dot=mag*mag
    else:
        mag=np.abs(grad); dot=grad*grad
    lhs=float(np.mean(chi*src)); rhs=float(-np.mean(jfun(mag,beta,kind)*dot))
    return lhs,rhs,float(abs(lhs-rhs)/max(abs(rhs),1e-300))


def deep_operator(chi,beta):
    n=len(chi); k=kvec(n); g=grad1(chi)
    flux=np.abs(g)*g/(1.0+beta)
    src=np.fft.ifft(1j*k*(np.fft.fft(flux)*mask1(n))).real
    return src

# Coefficient-level checks.
coeff={}; coeff_pass=True
for kind in KINDS:
    coeff[kind]={}
    for beta in BETAS:
        j=jfun(XTEST,beta,kind)
        deep_ref=XTEST[0]/(1.0+beta)
        deep_err=float(abs(j[0]-deep_ref)/deep_ref)
        high_ref=1.0/beta
        high_err=float(abs(j[-1]-high_ref)/high_ref)
        positivity=bool(np.all(j[1:]>0.0))
        bounded=bool(np.all(j>=-1e-15) and np.all(j<=high_ref*(1+1e-14)))
        monotonic=bool(np.all(np.diff(j)>=-1e-14))
        # Differentiate the integrated J with respect to Y=x^2 at fixed points
        # away from the Sharp kink.
        deriv_errs=[]
        for xt in [0.1,1.0,100.0,1e4]:
            kink=(1.0+beta)/beta
            if kind=='sharp' and abs(math.log(xt/kink))<0.1:
                continue
            y=xt*xt; dy=1e-5*max(y,1e-8)
            yp=y+dy; ym=max(y-dy,1e-16)
            num=float((Jfun_x(math.sqrt(yp),beta,kind)-Jfun_x(math.sqrt(ym),beta,kind))/(yp-ym))
            ref=float(jfun(xt,beta,kind))
            deriv_errs.append(abs(num-ref)/max(abs(ref),1e-300))
        j0=float(jfun(0.0,beta,kind))
        J0=float(Jfun_x(0.0,beta,kind))
        max_deriv=float(max(deriv_errs))
        ok=bool(abs(j0)<=1e-15 and abs(J0)<=1e-15 and positivity and bounded and monotonic and deep_err<1e-7 and high_err<2e-9 and max_deriv<2e-5)
        coeff_pass=coeff_pass and ok
        coeff[kind][str(beta)]={
            'j_values':j.tolist(),'j0':j0,'J0':J0,'positive':positivity,'bounded':bounded,'monotonic':monotonic,
            'deep_limit_relative_error_x1e8':deep_err,'high_limit_relative_error_x1e10':high_err,
            'integrated_J_derivative_max_relative_error':max_deriv,'pass':ok}

# 1D operator tests for all nine combinations.
one={}; all_operator_pass=True; max_conv=0.; max_vi=0.; max_tr=0.; max_deep=0.; max_const=0.
for kind in KINDS:
    one[kind]={}
    for beta in BETAS:
        coeffs={}; vis={}
        for n in N1:
            _,base=seed1(n); chi=scale_xrms_1d(base,1.0)
            src,g=operator1d(chi,beta,kind)
            _,_,vi=variational(chi,src,g,beta,kind)
            coeffs[n]=low_coeffs(src); vis[n]=vi
        conv=rel_l2(coeffs[512],coeffs[1024])
        n=512; _,base=seed1(n); chi=scale_xrms_1d(base,1.0); src,g=operator1d(chi,beta,kind)
        shift=37; ss,_=operator1d(np.roll(chi,shift),beta,kind); tr=rel_l2(ss,np.roll(src,shift))
        cs,_=operator1d(np.full(n,1.2345),beta,kind); cn=float(np.max(np.abs(cs)))
        chideep=scale_xrms_1d(base,1e-6); sf,_=operator1d(chideep,beta,kind); sd=deep_operator(chideep,beta); de=rel_l2(sf,sd)
        ok=bool(max(vis.values())<1e-10 and tr<1e-10 and cn<1e-12 and conv<5e-4 and de<1e-4)
        all_operator_pass=all_operator_pass and ok
        max_conv=max(max_conv,conv); max_vi=max(max_vi,max(vis.values())); max_tr=max(max_tr,tr); max_deep=max(max_deep,de); max_const=max(max_const,cn)
        one[kind][str(beta)]={'variational_relative_error_max':float(max(vis.values())),'translation_relative_error':tr,
                              'constant_null_max_abs':cn,'low_mode_512_vs_1024_relative_L2':conv,
                              'deep_reduction_relative_L2_xrms1e6':de,'pass':ok}

# 3D variational + axis permutation for all nine combinations.
q=np.arange(N3)*L/N3; X,Y,Z=np.meshgrid(q,q,q,indexing='ij')
base3=.4*np.cos(2*X+Y)+.23*np.sin(3*Y-Z)+.12*np.cos(X+2*Z)
chi3=scale_xrms_3d(base3,1.0)
three={}; max_vi3=0.; max_perm=0.; all_3d=True
for kind in KINDS:
    three[kind]={}
    for beta in BETAS:
        s,g=operator3d(chi3,beta,kind); _,_,vi=variational(chi3,s,g,beta,kind)
        cp=np.transpose(chi3,(1,0,2)); sp,_=operator3d(cp,beta,kind); perm=rel_l2(sp,np.transpose(s,(1,0,2)))
        ok=bool(vi<1e-10 and perm<1e-10 and np.all(np.isfinite(s)))
        all_3d=all_3d and ok; max_vi3=max(max_vi3,vi); max_perm=max(max_perm,perm)
        three[kind][str(beta)]={'variational_relative_error':vi,'axis_permutation_relative_error':perm,'pass':ok}

GATES={'coefficient_checks_all_nine':bool(coeff_pass),'operator_1d_all_nine':bool(all_operator_pass),'operator_3d_all_nine':bool(all_3d)}
passed=bool(all(GATES.values()))
classification='NL1C1_FULL_Y_OPERATOR_BRIDGE_PASS' if passed else 'NL1C1_FULL_Y_OPERATOR_BRIDGE_FAIL'
summary={
 'classification':classification,
 'scope':'full published AeST Y-sector interpolation/operator audit only; no physical-amplitude cosmological evolution',
 'co_primary_interpolations':KINDS,'co_primary_beta0':BETAS,'x_test':XTEST.tolist(),
 'coefficient_checks':coeff,'one_d':one,'three_d':three,
 'global_metrics':{'max_1d_variational_error':max_vi,'max_translation_error':max_tr,'max_constant_null':max_const,
                   'max_512_vs_1024_low_mode_error':max_conv,'max_deep_reduction_error':max_deep,
                   'max_3d_variational_error':max_vi3,'max_3d_axis_permutation_error':max_perm},
 'gates':GATES,'numerical_pass':passed,
 'historical_results_unchanged':True,
 'interpretation':'PASS validates the full Simple/Exponential/Sharp j(x) operators for all frozen beta0 values. It does not yet make the physical-amplitude cosmological baseline self-consistent.'
}
(OUT/'nl1c1_full_y_operator_bridge.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
if not passed:
    raise SystemExit(2)
