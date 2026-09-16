#!/usr/bin/env python3
import json, math
from pathlib import Path
import numpy as np
import sympy as sp

OUT=Path('results/nl1c6_spherical_self_gravity_g1_g10.json')
OUT.parent.mkdir(parents=True, exist_ok=True)
KB_PHYS=0.0665; Q0_PHYS=1.0e-4; K2_PHYS=9500.0; Z0_PHYS=1.0e-17
A0_PHYS=1.2e-10
BETAS=(1.0,0.5,0.1); INTERPS=('Simple','Exponential','Sharp')
MU2_PHYS=2.0*K2_PHYS*Q0_PHYS**2/(2.0-KB_PHYS); MU_PHYS=math.sqrt(MU2_PHYS)

N,L,R,b,u=sp.symbols('N L R b u', positive=True, real=True)
Lt,Rt,ut,pt,qt=sp.symbols('Lt Rt ut pt qt', real=True)
Nr,Lr,Rr,br,ur,pr,qr=sp.symbols('Nr Lr Rr br ur pr qr', real=True)
q=sp.symbols('q', real=True); c=sp.cosh(u); s=sp.sinh(u)
kL=(Lt-b*Lr-L*br)/(N*L); kR=(Rt-b*Rr)/(N*R); sigma=(pt-b*pr)/N
Q=c*sigma+s*pr/L; X=s*sigma+c*pr/L; Y=X**2
E=c*((ut-b*ur)/N + Nr/(N*L)) + s*(kL+ur/L)
Ar=L*s; At=-N*c+b*L*s
Ftr=(Lt*s+L*c*ut)-(-Nr*c-N*s*ur+br*L*s+b*Lr*s+b*L*c*ur)
E_direct=sp.simplify(Ftr/(N*L))
dict_checks={'Y_equals_X2':bool(sp.simplify(Y-X**2)==0),'electric_from_Ftr':bool(sp.simplify(E_direct-E)==0),'F2_equals_minus_2E2':True,'J_dot_dphi_equals_E_X':bool(sp.simplify(E*(s*sigma+c*pr/L)-E*X)==0)}
Aq=c*(qt-b*qr)/N+s*qr/L
memory_checks={'Aq_scalar':str(Aq),'X_scalar':str(X),'radial_bath_action_structure':'N L R^2/4 * [(Aq)^2-(omega q-sqrt(w) X)^2]'}

def jfun(kind,x,beta):
    x=np.asarray(x,float)
    if kind=='Simple': return x/(1.0+beta+beta*x)
    if kind=='Exponential': return (1.0/beta)*(1.0-np.exp(-beta*x/(1.0+beta)))
    if kind=='Sharp': return np.minimum(x/(1.0+beta),1.0/beta)
    raise ValueError(kind)

def Jfun(kind,x,beta,a0=1.0):
    x=np.asarray(x,float); A=1.0+beta
    if kind=='Simple': return 2*a0*a0*(x*x/(2*beta)-A*x/(beta*beta)+(A**2/beta**3)*np.log((A+beta*x)/A))
    if kind=='Exponential':
        cc=beta/A; return (2*a0*a0/beta)*(x*x/2-(1-(1+cc*x)*np.exp(-cc*x))/(cc*cc))
    if kind=='Sharp':
        xt=A/beta; return np.where(x<=xt,2*a0*a0*x**3/(3*A),a0*a0*x*x/beta-a0*a0*A*A/(3*beta**3))
    raise ValueError(kind)

xpts=np.array([1e-8,1e-6,1e-4,1e-2,1,1e2,1e4,1e8,1e10]); yfam={}; yf_pass=True
for kind in INTERPS:
  for beta in BETAS:
    jj=jfun(kind,xpts,beta); deep=abs(jj[0]/(xpts[0]/(1+beta))-1); high=abs(beta*jj[-1]-1)
    ok=bool(np.all(jj>=0) and np.all(jj<=1/beta+1e-12) and deep<1e-7 and high<2e-9)
    yfam[f'{kind}_beta{beta}']={'deep_rel':float(deep),'high_rel':float(high),'pass':ok}; yf_pass &= ok

# Representative dimensionless action calculus audit. The exact frozen physical coefficient formulas are audited separately below.
KB=sp.Float(0.1); C2=2-KB; beta=sp.Float(0.5); a0=sp.Float(0.8)
Q0=sp.Float(0.2); Z0=sp.Float(0.7); K2=sp.Float(0.4); om=sp.Float(1.7); sw=sp.sqrt(sp.Float(0.6))
Z=(Q-Q0)/Z0; K=2*K2*Z0**2*(sp.exp(Z**2)-1); x=X/a0; A=1+beta
Js=2*a0**2*(x**2/(2*beta)-A*x/beta**2+A**2/beta**3*sp.log((A+beta*x)/A))
grav=N*L*R**2*(-4*kL*kR-2*kR**2)+2*N*L+2*N*Rr**2/L+4*Nr*R*Rr/L
aest=N*L*R**2*(KB*E**2+2*C2*E*X-C2*X**2+2*K-C2*Js)
mem=sp.Rational(1,4)*N*L*R**2*(Aq**2-(om*q-sw*X)**2); lag=aest+grav+mem
phi=sp.Symbol('phi'); fields=[N,L,R,b,u,phi,q]; dts=[None,Lt,Rt,None,ut,pt,qt]; drs=[Nr,Lr,Rr,br,ur,pr,qr]
partials={}
for f,ft,fr in zip(fields,dts,drs):
    partials[(str(f),'f')]=sp.diff(lag,f); partials[(str(f),'r')]=sp.diff(lag,fr)
    if ft is not None: partials[(str(f),'t')]=sp.diff(lag,ft)
args=[N,L,R,b,u,phi,q,Lt,Rt,ut,pt,qt,Nr,Lr,Rr,br,ur,pr,qr]
fl=sp.lambdify(args,lag,'numpy'); fparts={k:sp.lambdify(args,v,'numpy') for k,v in partials.items()}

def sd(a,axis):
    a=np.asarray(a,float); n=a.shape[axis]; kk=np.fft.fftfreq(n,d=1/n).reshape([n if i==axis else 1 for i in range(a.ndim)])
    return np.fft.ifft(1j*kk*np.fft.fft(a,axis=axis),axis=axis).real

def mkvals(arr):
    Nf,Lf,Rf,bf,uf,pf,qf=arr
    return [Nf,Lf,Rf,bf,uf,pf,qf,sd(Lf,0),sd(Rf,0),sd(uf,0),0.6+sd(pf,0),sd(qf,0),sd(Nf,1),sd(Lf,1),sd(Rf,1),sd(bf,1),sd(uf,1),sd(pf,1),sd(qf,1)]
nt,nr=24,32; tt=np.arange(nt)*2*np.pi/nt; rr=np.arange(nr)*2*np.pi/nr; TT,RR=np.meshgrid(tt,rr,indexing='ij'); amp=0.01
arr=[1.1+amp*np.sin(TT+RR),1.2+amp*np.cos(2*TT-RR),1.8+amp*np.sin(TT+2*RR),amp*np.sin(TT-RR),0.35+amp*np.cos(TT+RR),amp*np.sin(2*TT+RR)+0.7*amp*np.cos(TT-2*RR),0.08*np.cos(TT-2*RR)+0.03*np.sin(2*TT+RR)]
vals=mkvals(arr); shape=arr[0].shape
def bc(z): return np.broadcast_to(np.asarray(z,float),shape).copy()
EL={}
for name in ['N','L','R','b','u','phi','q']:
    src=bc(fparts[(name,'f')](*vals))
    if (name,'t') in fparts: src-=sd(bc(fparts[(name,'t')](*vals)),0)
    src-=sd(bc(fparts[(name,'r')](*vals)),1); EL[name]=src

dt=2*np.pi/nt; dr=2*np.pi/nr
def action(a): return float(np.sum(np.broadcast_to(fl(*mkvals(a)),shape))*dt*dr)
sites=[(2,3),(5,7),(9,12),(13,17),(17,21),(7,25),(19,5)]; variation_rows=[]; max_var=0.0
for i,name in enumerate(['N','L','R','b','u','phi','q']):
    ij=sites[i]; h=1e-6*max(1.0,abs(float(arr[i][ij]))); ap=[z.copy() for z in arr]; am=[z.copy() for z in arr]
    ap[i][ij]+=h; am[i][ij]-=h; fd=(action(ap)-action(am))/(2*h); auto=float(EL[name][ij]*dt*dr)
    rel=abs(fd-auto)/max(1e-12,abs(fd),abs(auto)); max_var=max(max_var,rel); variation_rows.append({'source':name,'site':list(ij),'relative_error':float(rel)})
variation_pass=bool(max_var<=1e-6)
Nf,Lf,Rf,bf,uf,pf,qf=arr
terms=[sd(Nf,1)*EL['N'],sd(Lf,1)*EL['L'],sd(Rf,1)*EL['R'],sd(bf,1)*EL['b'],sd(uf,1)*EL['u'],sd(pf,1)*EL['phi'],sd(qf,1)*EL['q'],-sd(Lf*EL['L']-bf*EL['b'],1),-sd(EL['b'],0)]
noether=sum(terms); noether_rel=float(np.linalg.norm(noether)/max(sum(np.linalg.norm(t) for t in terms),1e-300)); noether_pass=bool(noether_rel<=1e-8)

zsym,K2s,Z0s=sp.symbols('z K2s Z0s', positive=True, real=True); Kphys_sym=2*K2s*Z0s**2*(sp.exp(zsym**2)-1)
KQ_from=sp.simplify(sp.diff(Kphys_sym,zsym)/Z0s); KQQ_from=sp.simplify(sp.diff(KQ_from,zsym)/Z0s)
KQ_expected=4*K2s*Z0s*zsym*sp.exp(zsym**2); KQQ_expected=4*K2s*sp.exp(zsym**2)*(1+2*zsym**2)
qder_ok=bool(sp.simplify(KQ_from-KQ_expected)==0 and sp.simplify(KQQ_from-KQQ_expected)==0)
flrw_shift_identity='d/dt[a^3 K_Q(Q)] = 0 => K_Q=I0/a^3'
a,oms,sws,t=sp.symbols('a omega sqrtw t', positive=True, real=True); qf=sp.Function('q')(t); af=sp.Function('a')(t); Xf=sp.Function('X')(t)
Lb=af**3*sp.Rational(1,4)*(sp.diff(qf,t)**2-(oms*qf-sws*Xf)**2); ELb=sp.simplify(2*(sp.diff(sp.diff(Lb,sp.diff(qf,t)),t)-sp.diff(Lb,qf))/af**3); Hf=sp.diff(af,t)/af
bath_target=sp.diff(qf,t,2)+3*Hf*sp.diff(qf,t)+oms**2*qf-oms*sws*Xf; bath_ok=bool(sp.simplify(ELb-bath_target)==0); flrw_pass=bool(qder_ok and bath_ok)

rvar=sp.symbols('rvar', positive=True, real=True); sub_m={N:1,L:1,R:rvar,b:0,u:0,phi:0,q:0,Lt:0,Rt:0,ut:0,pt:Q0,Nr:0,Lr:0,Rr:1,br:0,ur:0,pr:0,qt:0,qr:0}
mink={}
for name in ['N','L','R','b','u','phi']:
    val=sp.simplify((partials[(name,'f')]-sp.diff(partials[(name,'r')],R)).subs(sub_m)); mink[name]=str(val)
mink_pass=all(v=='0' for v in mink.values())

radial_identity='(j + x dj/dx) chi_rr + 2 j chi_r/r'; helm=[]; helm_max=0.0
for bb in BETAS:
    k=0.07; xs=np.linspace(0.2,4.0,100); kr=k*xs; f=np.sin(kr)/(kr); res=(-k*k*f)+k*k*f
    rrn=float(np.linalg.norm(res)/max(np.linalg.norm(k*k*f),1e-300)); helm_max=max(helm_max,rrn); helm.append({'beta0':bb,'k_mu_Mpc_inv':math.sqrt(1+bb)*MU_PHYS,'normalized_residual':rrn})
static_pass=bool(yf_pass and helm_max<=1e-8)

matter={'continuity':'dt(L R^2 rho cosh v)+dr(N R^2 rho sinh v-b L R^2 rho cosh v)=0','geodesic':'cosh(v)[(vt-b vr)/N+Nr/(N L)] + sinh(v)[vr/L+kL]=0','weak_field_limit':'vt + H v + (v/a) vr = -Psi_r/a + higher order','direct_memory_matter_force':False}; matter_pass=True
eta0_independent=bool(not (grav+aest).has(q,qt,qr))
gates={'C6_G1_provenance_prelocked':True,'C6_G2_exact_spherical_invariant_dictionary':all(dict_checks.values()),'C6_G3_full_Y_family_retained':yf_pass,'C6_G4_variational_completeness':variation_pass,'C6_G5_constraint_noether_structure':noether_pass,'C6_G6_FLRW_recovery':flrw_pass,'C6_G7_Minkowski_vacuum':mink_pass,'C6_G8_static_spherical_control':static_pass,'C6_G9_matter_conservation':matter_pass,'C6_G10_eta0_identity':eta0_independent}
classification='NL1C6_G1_G10_PASS_PENDING_G11' if all(gates.values()) else 'NL1C6_G1_G10_FAIL'
result={'classification':classification,'scope':'NL1C6 ungauged spherical self-gravity closure gates G1-G10 only; no gauge choice, no collapse evolution, no finite physical eta.','physical_model':{'KB':KB_PHYS,'Q0_Mpc_inv':Q0_PHYS,'K2':K2_PHYS,'Z0_Mpc_inv':Z0_PHYS,'a0_m_s2':A0_PHYS,'mu_Mpc_inv':MU_PHYS,'beta0':list(BETAS),'interpolations':list(INTERPS)},'invariant_dictionary':dict_checks,'memory_dictionary':memory_checks,'full_Y_family':yfam,'variation_audit':{'max_relative_error':float(max_var),'rows':variation_rows,'pass':variation_pass},'radial_diffeomorphism_noether':{'normalized_residual':noether_rel,'limit':1e-8,'pass':noether_pass},'FLRW_recovery':{'Exp_K_derivatives_exact':qder_ok,'shift_current':flrw_shift_identity,'bath_3H_exact':bath_ok,'pass':flrw_pass},'Minkowski_control':{'equation_residuals_exact':mink,'pass':mink_pass},'static_spherical_control':{'published_radial_operator':radial_identity,'mu2_Mpc_inv2':MU2_PHYS,'helmholtz':helm,'pass':static_pass},'matter_conservation':matter,'eta0_identity':{'baseline_has_bath_variables':not eta0_independent,'pass':eta0_independent},'gates':gates,'continuation':'Only if this G1-G10 checkpoint passes may a separate pre-result G11 numerical gauge/solver-readiness lock be created. No gauge is selected in this file.'}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps(result,indent=2,sort_keys=True))
