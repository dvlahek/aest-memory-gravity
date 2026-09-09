#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np

OUT = Path('results')
OUT.mkdir(exist_ok=True)
L = 2.0*np.pi
KB = 0.0665
A0 = 1.2e-10
BETAS = [1.0,0.5,0.1]
N1 = [256,512,1024]
N3 = 32


def rel_l2(a,b):
    a=np.asarray(a); b=np.asarray(b)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(b),1e-300))


def kvec(n,L=L):
    return 2*np.pi*np.fft.fftfreq(n,d=L/n)


def mask1(n):
    m=np.fft.fftfreq(n)*n
    return (np.abs(m) <= (n/3.0+1e-12)).astype(float)


def operator1d(chi,beta=0.0,L=L):
    n=len(chi); k=kvec(n,L)
    ch=np.fft.fft(chi)
    gx=np.fft.ifft(1j*k*ch).real
    flux=np.abs(gx)*gx
    fh=np.fft.fft(flux)*mask1(n)
    src=np.fft.ifft(1j*k*fh).real/(1.0+beta)
    return src,gx


def low_coeffs(a,mmax):
    h=np.fft.fft(a)/len(a)
    return h[:mmax+1]


def grids3(n,L=L):
    kv=kvec(n,L)
    return np.meshgrid(kv,kv,kv,indexing='ij')


def mask3(n):
    m=np.fft.fftfreq(n)*n
    a,b,c=np.meshgrid(m,m,m,indexing='ij')
    return ((np.abs(a)<=n/3.0+1e-12)&(np.abs(b)<=n/3.0+1e-12)&(np.abs(c)<=n/3.0+1e-12)).astype(float)


def operator3d(chi,beta=0.0,L=L):
    n=chi.shape[0]
    K=grids3(n,L); ch=np.fft.fftn(chi); m=mask3(n)
    grad=[np.fft.ifftn(1j*Ki*ch).real for Ki in K]
    mag=np.sqrt(sum(g*g for g in grad))
    src=np.zeros_like(chi)
    for Ki,g in zip(K,grad):
        fh=np.fft.fftn(mag*g)*m
        src += np.fft.ifftn(1j*Ki*fh).real
    src /= (1.0+beta)
    return src,grad


def var_identity(chi,src,grad,beta=0.0):
    mag=np.sqrt(sum(g*g for g in grad)) if isinstance(grad,(list,tuple)) else np.abs(grad)
    lhs=float(np.mean(chi*src))
    rhs=float(-np.mean(mag**3)/(1.0+beta))
    err=abs(lhs-rhs)/max(abs(rhs),1e-300)
    return lhs,rhs,float(err)


# 1D deterministic seed and convergence.
one={}
coeff={}
for n in N1:
    x=np.arange(n)*L/n
    chi=.7*np.cos(3*x)+.2*np.sin(5*x)+.11*np.cos(11*x)
    src,g=operator1d(chi,0.0)
    lhs,rhs,vi=var_identity(chi,src,g,0.0)
    coeff[n]=low_coeffs(src,32)
    one[str(n)]={'variational_lhs':lhs,'variational_rhs':rhs,'variational_relative_error':vi,'max_abs_source':float(np.max(np.abs(src)))}

conv_512_1024=rel_l2(coeff[512],coeff[1024])
conv_256_1024=rel_l2(coeff[256],coeff[1024])

# Primary N=512 structural tests.
n=512; x=np.arange(n)*L/n
chi=.7*np.cos(3*x)+.2*np.sin(5*x)+.11*np.cos(11*x)
src,g=operator1d(chi,0.0)
hom={}
for amp in [0.25,0.5,2.0,4.0]:
    sa,_=operator1d(amp*chi,0.0)
    hom[str(amp)]=rel_l2(sa/(amp*amp),src)
shift=37
shifted,_=operator1d(np.roll(chi,shift),0.0)
translation=rel_l2(shifted,np.roll(src,shift))

const_src,_=operator1d(np.full(n,1.2345),0.0)
constant_null=float(np.max(np.abs(const_src)))

# beta0 scaling is co-primary and must follow exactly 1/(1+beta0).
base_norm=float(np.linalg.norm(src))
beta_rows={}; beta_err=0.0
for beta in BETAS:
    sb,_=operator1d(chi,beta)
    ratio=float(np.linalg.norm(sb)/base_norm)
    expected=1.0/(1.0+beta)
    err=abs(ratio-expected)/expected
    beta_err=max(beta_err,err)
    beta_rows[str(beta)]={'measured_norm_ratio_to_beta0_zero':ratio,'expected_ratio':expected,'relative_error':float(err)}

# For chi=cos(3x), |chi_x|chi_x is anti-periodic under x->x+pi/3.
# Its divergence therefore contains the 3,9,15,... harmonic sequence; the rest
# below mode 40 is numerical/dealiasing leakage.
single=np.cos(3*x)
ss,_=operator1d(single,0.0)
h=np.abs(np.fft.fft(ss)/n)
allowed={m for m in range(3,40,6)}
forbidden=[h[m] for m in range(1,40) if m not in allowed]
forbidden_ratio=float(max(forbidden)/max(np.max(h[1:40]),1e-300))

# 3D deterministic seed and isotropy/permutation audit.
n=N3; q=np.arange(n)*L/n
X,Y,Z=np.meshgrid(q,q,q,indexing='ij')
chi3=.4*np.cos(2*X+Y)+.23*np.sin(3*Y-Z)+.12*np.cos(X+2*Z)
s3,g3=operator3d(chi3,0.0)
lhs3,rhs3,vi3=var_identity(chi3,s3,g3,0.0)
chip=np.transpose(chi3,(1,0,2))
sp,_=operator3d(chip,0.0)
perm=rel_l2(sp,np.transpose(s3,(1,0,2)))

all_arrays=[src,g,s3]+g3
finite=bool(all(np.all(np.isfinite(a)) for a in all_arrays))

GATES={
 'all_outputs_finite':finite,
 'constant_field_null':constant_null<=1e-12,
 'one_d_variational_identity':max(v['variational_relative_error'] for v in one.values())<=1e-10,
 'one_d_positive_homogeneity':max(hom.values())<=1e-12,
 'one_d_integer_translation':translation<=1e-10,
 'one_d_512_vs_1024_low_mode_convergence':conv_512_1024<=5e-4,
 'one_d_single_mode_forbidden_harmonics':forbidden_ratio<=1e-4,
 'beta0_scaling':beta_err<=1e-12,
 'three_d_variational_identity':vi3<=1e-10,
 'three_d_axis_permutation':perm<=1e-10,
}
passed=bool(all(GATES.values()))
classification='NL1A_PSEUDOSPECTRAL_OPERATOR_BRIDGE_PASS' if passed else 'NL1A_PSEUDOSPECTRAL_OPERATOR_BRIDGE_FAIL'

summary={
 'classification':classification,
 'scope':'deterministic theory/operator implementation audit only; no physical nonlinear growth claim',
 'frozen_inputs':{'KB':KB,'a0_m_s2':A0,'beta0_co_primary':BETAS,'L':L,'N1':N1,'N3':N3,'dealiasing':'2/3 nonlinear-flux mask'},
 'full_physical_prefactor':'2(2-KB)/[(1+beta0)a0] multiplies the reported normalized operator',
 'one_d':one,
 'one_d_convergence':{'relative_L2_256_vs_1024_low_modes_m0_32':conv_256_1024,'relative_L2_512_vs_1024_low_modes_m0_32':conv_512_1024},
 'one_d_homogeneity_relative_errors':hom,
 'one_d_translation_relative_error':translation,
 'constant_field_null_max_abs':constant_null,
 'single_mode_forbidden_harmonic_ratio':forbidden_ratio,
 'beta0_scaling':beta_rows,
 'beta0_scaling_max_relative_error':beta_err,
 'three_d':{'variational_lhs':lhs3,'variational_rhs':rhs3,'variational_relative_error':vi3,'axis_permutation_relative_error':perm,'max_abs_source':float(np.max(np.abs(s3)))},
 'gates':GATES,
 'numerical_pass':passed,
 'interpretation':'PASS certifies the pseudospectral implementation of the exact NL0C leading Y-sector operator and its structural identities. It does not certify a nonlinear AeST growth prediction. NL1B must freeze the actual second-order dynamics before growth is computed.'
}
(OUT/'nl1a_pseudospectral_operator_bridge.json').write_text(json.dumps(summary,indent=2))
np.savez_compressed(OUT/'nl1a_pseudospectral_operator_bridge.npz',x=x,chi_1d=chi,source_1d=src,grad_1d=g,chi_3d=chi3,source_3d=s3)
print(json.dumps(summary,indent=2))
if not passed:
    raise SystemExit(2)
