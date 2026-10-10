#!/usr/bin/env python3
"""Pure manufactured checks of D27R1 additive audit; no physical parent files."""
import ast
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
source=Path(__file__).with_name('h4f3d27r1_signed_fft_sector_roundoff_audit.py')
tree=ast.parse(source.read_text())
functions={'relative','pchip_at_first','check_triplet','check_original_real_shift','audited_rebuild'}
body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in functions]
assert len(body)==len(functions)
ns={'np':np,'PchipInterpolator':PchipInterpolator,'EPS':1e-300}
exec(compile(ast.Module(body=body,type_ignores=[]),str(source),'exec'),ns)
tri=ns['check_original_real_shift'];old=ns['check_triplet'];rel=ns['relative']
a=np.arange(9,dtype=float).reshape((3,3));b=-a+0.25
assert tri(a+b,a,b)
for bad in (a+b+1e-6,a-b):
    try:tri(bad,a,b)
    except RuntimeError:pass
    else:raise AssertionError('D27R1 real-space mismatch negative control not detected')
print('GE19_D27R1_REAL_SPACE_NEGATIVE_CONTROLS_PASS',flush=True)

# Deliberately manufactured tiny Fourier mode: original real-space full
# source is EXACTLY the GE06+GE07 sum, but separately computed FFTs are
# not distributive at small cancelled Fourier amplitudes.
n=1024;t=2*np.pi*np.arange(n)/n
rng=np.random.default_rng(17)
ga=rng.normal(size=n);ma=-ga+1e-15*np.cos(14*t);full=ga+ma
assert tri(full,ga,ma)
f=lambda z:np.fft.fft(z)[14]/n
st,sg,sm=f(full),f(ga),f(ma)
original_failed_relative=rel([st],[sg+sm])
assert original_failed_relative>1e-4,(original_failed_relative,st,sg,sm)
try:old([st],[sg],[sm])
except RuntimeError:pass
else:raise AssertionError('Original D27 tiny-mode relative FAIL must remain reproducible')
signed_remainder=st-sg-sm
assert abs(signed_remainder)>0
assert abs((sg+sm+signed_remainder)-st) <= 16*np.finfo(float).eps*(abs(sg)+abs(sm)+abs(st))
print('GE19_D27R1_MANUFACTURED_EXACT_REAL_BUT_TINY_FFT_RELATIVE_FAIL_PRESERVED',flush=True)

# The original three-call GE06/GE07 source callback must be untouched.
class FakeR7:
    BETAS=(1.,0.5,0.1)
    def main_and_constraints(self,g,m):
        return g[0]+m[0],g[1]+m[1]
class FakeH3F:
    @staticmethod
    def source_bundle_reduced_lambda(r7,r14,mod6,mod7,bg,rho,tag,nx,H1,dh1):
        result={}
        time=np.arange(len(bg['x']))[:,None];space=np.arange(nx)[None,:]
        for beta in r7.BETAS:
            gmain=np.broadcast_to((beta+time+space)[None,:,:],(6,len(bg['x']),nx)).copy()
            mmain=np.broadcast_to((beta+2*time-space)[None,:,:],(6,len(bg['x']),nx)).copy()
            gcon=np.broadcast_to((beta+time-space)[None,:,:],(2,len(bg['x']),nx)).copy()
            mcon=np.broadcast_to((beta-time+space)[None,:,:],(2,len(bg['x']),nx)).copy()
            zm=np.zeros_like(gmain);zc=np.zeros_like(gcon)
            full=r7.main_and_constraints((gmain,gcon),(mmain,mcon))
            g=r7.main_and_constraints((gmain,gcon),(zm,zc))
            m=r7.main_and_constraints((zm,zc),(mmain,mcon))
            fft=lambda arr:np.fft.fft(arr,axis=-1)[:,:,:41]/nx
            gm=-fft(g[0]);mm=-fft(m[0]);zero=np.zeros_like(gm)
            result[beta]={'rhs':-fft(full[0]),'rhs_constraint':-fft(full[1]),
                'Q_ga':gm,'Q_matter':mm,'Q_lambda':zero,'Y_H3':zero}
        return result
ns['h3f']=FakeH3F
fake=FakeR7();bg={'x':np.arange(5.),'rho_lambda_action':np.ones(5)}
sources,sectors=ns['audited_rebuild'](fake,None,None,None,bg,'synthetic',None,None,nx=8)
for beta in fake.BETAS:
    real=np.asarray(sectors[beta]['real_shift_triplet'])
    assert real.shape==(3,5,8)
    assert tri(real[2],real[0],real[1])
    assert rel(sources[beta]['rhs_constraint'],sectors[beta]['GE06_constraint']+sectors[beta]['GE07_constraint'])<1e-13
print('GE19_D27R1_MANUFACTURED_ACTION_SOURCE_CAPTURE_PASS',flush=True)
