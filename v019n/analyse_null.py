#!/usr/bin/env python3
from pathlib import Path
import argparse,json,math

SUFFIXES=(
  'cl.dat',
  'cl_lensed.dat',
  'pk.dat',
  'background.dat',
  'thermodynamics.dat',
)


def load_numeric(path):
    rows=[]
    with open(path,'r',errors='replace') as f:
        for line in f:
            t=line.strip()
            if not t or t.startswith('#'):
                continue
            try:
                rows.append([float(x) for x in t.split()])
            except ValueError:
                pass
    if not rows:
        raise RuntimeError(f'no numeric rows in {path}')
    return rows


def find_one(out,prefix,suffix):
    matches=sorted(out.glob(prefix+'*'+suffix))
    if len(matches)!=1:
        return None
    return matches[0]


def compare_files(a,b):
    aa=load_numeric(a); bb=load_numeric(b)
    if len(aa)!=len(bb):
        return {'row_match':False,'exact_numeric':False,'max_abs':math.inf,'max_rel':math.inf}
    max_abs=0.0;max_rel=0.0;exact=True;nval=0
    for ra,rb in zip(aa,bb):
        if len(ra)!=len(rb):
            return {'row_match':False,'exact_numeric':False,'max_abs':math.inf,'max_rel':math.inf}
        for x,y in zip(ra,rb):
            nval+=1
            d=abs(x-y)
            if d!=0.0: exact=False
            max_abs=max(max_abs,d)
            max_rel=max(max_rel,d/max(abs(x),abs(y),1e-300))
    return {'row_match':True,'numeric_values':nval,'exact_numeric':exact,
            'max_abs':max_abs,'max_rel':max_rel}


def compare_pair(out,level,model_a='cdm',model_b='null'):
    details={};all_exact=True;all_machine=True;present=0
    for suffix in SUFFIXES:
        a=find_one(out,f'v019n_{model_a}_{level}_',suffix)
        b=find_one(out,f'v019n_{model_b}_{level}_',suffix)
        if a is None or b is None:
            details[suffix]={'present':False}
            continue
        present+=1
        c=compare_files(a,b);c['present']=True;c['reference']=a.name;c['test']=b.name
        details[suffix]=c
        all_exact &= c['exact_numeric']
        all_machine &= c['row_match'] and c['max_rel']<1e-12
    return {'level':level,'files_present':present,'all_numeric_exact':all_exact and present>=4,
            'all_machine_null':all_machine and present>=4,'details':details}


def self_compare(out,model):
    details={};mx=0.0;exact=True
    for suffix in ('cl.dat','cl_lensed.dat'):
        a=find_one(out,f'v019n_{model}_p0_',suffix)
        b=find_one(out,f'v019n_{model}_p3_',suffix)
        if a is None or b is None: continue
        c=compare_files(a,b);details[suffix]=c;mx=max(mx,c['max_rel']);exact &= c['exact_numeric']
    return {'exact_numeric':exact,'max_rel':mx,'details':details}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('output_dir');ap.add_argument('--json-out',default='results/v019n_null.json');args=ap.parse_args()
    out=Path(args.output_dir)
    p0=compare_pair(out,'p0');p3=compare_pair(out,'p3')
    cdm_self=self_compare(out,'cdm');null_self=self_compare(out,'null')

    if p0['all_numeric_exact'] and p3['all_numeric_exact']:
        classification='STRICT_STRUCTURAL_NULL_PASS'
        gate='PASS_STRICT_NULL'
    elif p0['all_machine_null'] and p3['all_machine_null']:
        classification='MACHINE_PRECISION_STRUCTURAL_NULL'
        gate='PASS_MACHINE_NULL'
    else:
        classification='STRUCTURAL_STATE_EFFECT_DETECTED'
        gate='CHECK'

    result={
      'p0_cdm_vs_frozen_extra_states':p0,
      'p3_cdm_vs_frozen_extra_states':p3,
      'cdm_p0_vs_p3':cdm_self,
      'null_p0_vs_p3':null_self,
      'classification':classification,
      'gate_status':gate,
      'interpretation':(
        'The null run uses the standard CDM background and standard CDM stress-energy/evolution, '
        'but carries two additional frozen zero ODE states. A strict null therefore excludes '
        'state-vector dimension/adaptive error normalization as the origin of the persistent v0.19p Exp-CDM residual.'
        if gate.startswith('PASS') else
        'The frozen extra-state control changed numerical outputs; the solver-structure explanation is not excluded.'
      ),
      'memory_enabled':False,
    }
    p=Path(args.json_out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2))
    print(json.dumps({k:result[k] for k in ['classification','gate_status','interpretation']},indent=2))

if __name__=='__main__':
    main()
