#!/usr/bin/env python3
"""Original signed mixed H4 first-order nonbath parent and KNOWN boundary.

Only 2*(E10 F11,chi + E11 F10,chi) and 2*L/b cross boundary.
E00*F21 and L21*EL00-b21*Eb00 remain uncomputed/unknown.
Fourier reconstruction is an archive-only, preregistered 1e-12 check.
"""
from __future__ import annotations
import numpy as np

FIELDS=("N","L","R","b","u","phi","T","rho")
NX=128
RTOL=1e-12
TINY=1e-300

def low(a):
    q=np.asarray(a,float)
    if q.ndim!=2 or q.shape[1]!=NX or not np.isfinite(q).all():
        raise ValueError("D10 original Nx128 real array invalid")
    return np.asarray(np.fft.fft(q,axis=-1)[:,:41]/NX,complex)

def recover(q):
    c=np.asarray(q,complex)
    if c.ndim!=2 or c.shape[1]!=41:raise ValueError("D10 Fourier mode shape")
    h=np.zeros((c.shape[0],NX),complex)
    h[:,:41]=c
    h[:,-40:]=np.conj(c[:,1:41][:,::-1])
    return np.fft.ifft(NX*h,axis=-1).real

def rel(a,b):
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),TINY))

def archive_err(a):
    return rel(np.asarray(a,float),recover(low(a)))

def known_signed(F10,X10,E10,F11,X11,E11,dx):
    """Keep eight signed contributions and both independent L/b boundary crosses."""
    terms={n:2.0*(E10[n]*X11[n]+E11[n]*X10[n]) for n in FIELDS}
    p=sum(terms.values())
    b=(2.0*F10["L"]*E11["L"]+2.0*F11["L"]*E10["L"]
       -2.0*F10["b"]*E11["b"]-2.0*F11["b"]*E10["b"])
    dchi_b=dx(b)
    return terms,p,b,dchi_b,p-dchi_b

def evaluate_pair(F10,X10,F11,X11,schemes,dx):
    """schemes maps original FD4/FD8 to independently evaluated E10,E11."""
    saved={}
    archive=[]
    result={}
    for field in FIELDS:
        for name,x in (("F10",F10[field]),("F11",F11[field]),
                       ("F10chi",X10[field]),("F11chi",X11[field])):
            saved[name+"_"+field]=low(x)
            archive.append(archive_err(x))
    for scheme,(E10,E11) in schemes.items():
        terms,p,b,dchi_b,w=known_signed(F10,X10,E10,F11,X11,E11,dx)
        for field in FIELDS:
            for name,x in (("E10",E10[field]),("E11",E11[field]),
                           ("parent",terms[field])):
                saved[scheme+"_"+name+"_"+field]=low(x)
                archive.append(archive_err(x))
        for name,x in (("P_known",p),("B_known",b),
                       ("dchi_B_known",dchi_b),("W_known",w)):
            saved[scheme+"_"+name]=low(x)
            archive.append(archive_err(x))
        modes_p=sum(saved[scheme+"_parent_"+field] for field in FIELDS)
        signed=saved[scheme+"_P_known"]-saved[scheme+"_dchi_B_known"]
        kfund=float(dx.kfund)
        derivative=1j*kfund*np.arange(41)[None,:]*saved[scheme+"_B_known"]
        identities={
            "parent_parts_complex_FFT_relative":rel(saved[scheme+"_P_known"],modes_p),
            "signed_ward_complex_FFT_relative":rel(saved[scheme+"_W_known"],signed),
            "original_chi_derivative_symbol_relative":
                rel(saved[scheme+"_dchi_B_known"],derivative),
        }
        result[scheme]={
            "archive_only_identities":identities,
            "known_parent_real_L2_report_only":float(np.linalg.norm(p)),
            "known_boundary_real_L2_report_only":float(np.linalg.norm(b)),
            "known_ward_real_L2_report_only":float(np.linalg.norm(w)),
            "E10_real_L2_report_only":{n:float(np.linalg.norm(E10[n])) for n in FIELDS},
            "E11_real_L2_report_only":{n:float(np.linalg.norm(E11[n])) for n in FIELDS},
        }
        archive.extend(identities.values())
    max_archive=float(max(archive,default=float("inf")))
    passed=bool(np.isfinite(max_archive) and max_archive<=RTOL
                and len(FIELDS)==8
                and all(np.isfinite(q).all() for q in saved.values()))
    return saved,result,max_archive,passed
