import numpy as np
from scipy.optimize import nnls


def retarded_A(z,h):
    z=np.asarray(z,dtype=complex)
    A=np.sqrt(z*(z+3.0*h)+0j)
    A=np.where(A.real<0,-A,A)
    return A


def exact_kernel(z,h):
    A=retarded_A(z,h)
    return A/(1.0+A)


def complex_grid(h,nomega=121):
    omega=np.logspace(-3,3,nomega)
    eps=np.array([1e-8,1e-6,1e-4,1e-2,1e-1])
    z=np.array([h*(e+1j*w) for w in omega for e in eps],dtype=complex)
    return z,exact_kernel(z,h)


def q_nodes(N=24,qmin=1e-6,qmax=4.0):
    return np.logspace(np.log10(qmin),np.log10(qmax),N)


def basis(z,h,q):
    r=h*np.asarray(q,float)
    return z[:,None]/(z[:,None]+r[None,:])


def fit_nonnegative_weights(h,N=24,nomega=121,qmin=1e-6,qmax=4.0):
    z,K=complex_grid(h,nomega)
    q=q_nodes(N,qmin,qmax)
    B=basis(z,h,q)
    scale=np.maximum(np.abs(K),1e-300)
    M=np.vstack([B.real/scale[:,None],B.imag/scale[:,None]])
    y=np.r_[K.real/scale,K.imag/scale]
    w,_=nnls(M,y,maxiter=200*N)
    pred=B@w
    rel=np.abs(pred-K)/scale
    return q,w,rel


def kernel_from_table(z,h,q,w):
    return basis(np.atleast_1d(np.asarray(z,dtype=complex)),h,q)@np.asarray(w,float)


def interpolate_weights(h,anchors,weights):
    anchors=np.asarray(anchors,float)
    W=np.asarray(weights,float)
    if h<=anchors[0]:
        return W[0].copy()
    if h>=anchors[-1]:
        return W[-1].copy()
    j=np.searchsorted(anchors,h)-1
    la=np.log(anchors)
    t=(np.log(h)-la[j])/(la[j+1]-la[j])
    return (1.0-t)*W[j]+t*W[j+1]


def metrics(rel):
    rel=np.asarray(rel,float)
    return {
      'median':float(np.median(rel)),
      'p95':float(np.quantile(rel,.95)),
      'p99':float(np.quantile(rel,.99)),
      'max':float(np.max(rel)),
    }
