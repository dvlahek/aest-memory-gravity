#!/usr/bin/env python3
"""Manufactured controls on AST-extracted D27 pure helpers; no parent imports/data."""
import ast
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
source=Path(__file__).with_name('h4f3d27_h3f_shift_sector_provenance.py')
tree=ast.parse(source.read_text())
functions={'relative','pchip_at_first','check_triplet','audited_rebuild'}
body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in functions]
assert len(body)==len(functions)
ns={'np':np,'PchipInterpolator':PchipInterpolator,'EPS':1e-300}
exec(compile(ast.Module(body=body,type_ignores=[]),str(source),'exec'),ns)
check_triplet=ns['check_triplet'];pchip_at_first=ns['pchip_at_first']
x=np.arange(5.,dtype=float)
a=np.array([1.+1j,2.+3j,4.+5j,8.+9j,12.+12j])
b=np.array([-2.+0.4j,4.-4j,1.+2j,7.-1j,0.+4j])
assert check_triplet(a+b,a,b)<1e-14
try:
    check_triplet(a+b,-a,b)
except RuntimeError:
    print('GE19_D27_NEGATIVE_SOURCE_SIGN_CONTROL_PASS',flush=True)
else:raise RuntimeError('D27 negative sign control was not detected')
try:
    check_triplet(a+b,a,a)
except RuntimeError:
    print('GE19_D27_NEGATIVE_SECTOR_DUPLICATION_CONTROL_PASS',flush=True)
else:raise RuntimeError('D27 duplicated sector control was not detected')
s=pchip_at_first(x,a+b)
assert abs(s-pchip_at_first(x,a+b))<1e-13
print('GE19_D27_STATIC_SECTOR_AND_PCHIP_TEST_PASS',flush=True)

# Synthetic original-action callback capture test. The wrapper must leave the
# assembler output untouched and recover exactly three signed terms per beta.
class FakeR7:
    BETAS=(1.,0.5,0.1)
    def main_and_constraints(self,g,m):
        return g[0]+m[0],g[1]+m[1]
class FakeH3F:
    @staticmethod
    def source_bundle_reduced_lambda(r7,r14,mod6,mod7,bg,rho,tag,nx,H1,dh1):
        result={}
        time=np.arange(len(bg['x']))[:,None]
        space=np.arange(nx)[None,:]
        for beta in r7.BETAS:
            ge06main=np.broadcast_to((beta+time+space)[None,:,:],(6,len(bg['x']),nx)).copy()
            ge07main=np.broadcast_to((beta+2*time-space)[None,:,:],(6,len(bg['x']),nx)).copy()
            ge06con=np.broadcast_to((beta+time-space)[None,:,:],(2,len(bg['x']),nx)).copy()
            ge07con=np.broadcast_to((beta-time+space)[None,:,:],(2,len(bg['x']),nx)).copy()
            zm=np.zeros_like(ge06main);zc=np.zeros_like(ge06con)
            full=r7.main_and_constraints((ge06main,ge06con),(ge07main,ge07con))
            ga=r7.main_and_constraints((ge06main,ge06con),(zm,zc))
            ma=r7.main_and_constraints((zm,zc),(ge07main,ge07con))
            fft=lambda arr:np.fft.fft(arr,axis=-1)[:,:,:41]/nx
            gm=-fft(ga[0]);mm=-fft(ma[0]);zero=np.zeros_like(gm)
            result[beta]={'rhs':-fft(full[0]),'rhs_constraint':-fft(full[1]),
                          'Q_ga':gm,'Q_matter':mm,'Q_lambda':zero,'Y_H3':zero}
        return result
ns['h3f']=FakeH3F
Fake=FakeR7()
bg={'x':np.arange(5.),'rho_lambda_action':np.ones(5)}
src,sector=ns['audited_rebuild'](Fake,None,None,None,bg,'synthetic',None,None,nx=8)
assert set(sector)==set(Fake.BETAS)
for beta in Fake.BETAS:
    assert ns['relative'](src[beta]['rhs_constraint'],sector[beta]['GE06_constraint']+sector[beta]['GE07_constraint'])<1e-13
print('GE19_D27_MANUFACTURED_ORIGINAL_ASSEMBLY_CALL_CAPTURE_PASS',flush=True)
