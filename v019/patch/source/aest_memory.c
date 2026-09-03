#include <math.h>
#include <stddef.h>
#include "aest_memory.h"

static const double _aest_nodes[AEST_MEMORY_V019_NODES] = {
  0.00031622776601683794,0.0007386199822079358,0.001725210549942041,
  0.0040296113202004,0.00941204967268067,0.021983926488622893,
  0.05134832907437549,0.11993539462092344,0.2801356761198867,
  0.6543189129712962,1.5283067326587687,3.5696988468260624,
  8.337822234717883,19.47483039908753,45.48777947003777,
  106.24678308940409,248.16289228368237,579.6393953384961,
  1353.8761800225418,3162.2776601683795
};

static const double _aest_weights[AEST_MEMORY_V019_NODES] = {
  0.0003549832764699438,0.0003284312438827179,0.0009516439621708512,
  0.0021660594007921947,0.00509152520669826,0.0118562892906146,
  0.027673234995271925,0.06382357085727254,0.14038300101017823,
  0.24703490212236523,0.24833679544478374,0.13923159504266835,
  0.0647440833106984,0.026983754235172484,0.012361813713965936,
  0.0047071074300463695,0.0024983339993659695,0.0005837062152394986,
  0.0008008996696559603,0.0
};

const char *aest_memory_module_version(void) { return "v0.19-eta0"; }

double aest_memory_kernel20(double A) {
  int j;
  double a2,sum=0.;
  if (A <= 0.) return 0.;
  a2=A*A;
  for (j=0;j<AEST_MEMORY_V019_NODES;j++) {
    double r2=_aest_nodes[j]*_aest_nodes[j];
    sum += _aest_weights[j]*a2/(r2+a2);
  }
  return sum;
}

int aest_memory_selfcheck(double *max_rel) {
  int j,n;
  double mr=0.;
  for (j=0;j<AEST_MEMORY_V019_NODES;j++) {
    if (!(_aest_nodes[j] > 0.) || !(_aest_weights[j] >= 0.)) return 1;
  }
  for (n=0;n<=2400;n++) {
    double t=-3.+6.*((double)n/2400.);
    double A=pow(10.,t);
    double exact=A/(1.+A);
    double rel=fabs(aest_memory_kernel20(A)-exact)/exact;
    if (rel>mr) mr=rel;
  }
  if (max_rel) *max_rel=mr;
  return (mr<2.e-4) ? 0 : 2;
}

static int aest_eval_from_Z(int model,double Q0,double K2,double Z0,double Z,
                            double *Q,double *K,double *KQ,double *KQQ) {
  double q,k,kq,kqq;
  if (!(Q0>0.) || !(K2>0.) || !(Z0>0.) || !isfinite(Z)) return 1;
  q=Q0+Z0*Z;
  if (model==_AEST_MODEL_COSH_) {
    double sh=sinh(Z), ch=cosh(Z);
    if (!isfinite(sh) || !isfinite(ch)) return 2;
    k=2.*K2*Z0*Z0*(ch-1.);
    kq=2.*K2*Z0*sh;
    kqq=2.*K2*ch;
  }
  else if (model==_AEST_MODEL_EXP_) {
    double zz=Z*Z;
    double ex=exp(zz);
    if (!isfinite(ex)) return 3;
    k=2.*K2*Z0*Z0*(ex-1.);
    kq=4.*K2*Z0*Z*ex;
    kqq=4.*K2*ex*(1.+2.*zz);
  }
  else return 4;
  if (!(q>0.) || !(kqq>0.) || !isfinite(k) || !isfinite(kq)) return 5;
  *Q=q; *K=k; *KQ=kq; *KQQ=kqq;
  return 0;
}

int aest_background_calibrate(int model,double Q0,double K2,double Z0,
                              double target,double *I0) {
  int it;
  double lo=0.,hi=1.,flo,fhi;
  double Q,K,KQ,KQQ;
  if (!I0 || !(target>0.)) return 1;
  if (aest_eval_from_Z(model,Q0,K2,Z0,lo,&Q,&K,&KQ,&KQQ)) return 2;
  flo=Q*KQ-K-target;
  if (!(flo<0.)) return 3;
  for (;;) {
    if (aest_eval_from_Z(model,Q0,K2,Z0,hi,&Q,&K,&KQ,&KQQ)) return 4;
    fhi=Q*KQ-K-target;
    if (fhi>0.) break;
    hi*=2.;
    if (hi>128.) return 5;
  }
  for (it=0;it<180;it++) {
    double mid=.5*(lo+hi),fm;
    if (aest_eval_from_Z(model,Q0,K2,Z0,mid,&Q,&K,&KQ,&KQQ)) return 6;
    fm=Q*KQ-K-target;
    if (fm>0.) hi=mid; else lo=mid;
  }
  if (aest_eval_from_Z(model,Q0,K2,Z0,.5*(lo+hi),&Q,&K,&KQ,&KQQ)) return 7;
  *I0=KQ;
  return (isfinite(*I0) && *I0>0.) ? 0 : 8;
}

static int aest_exp_Z_from_x(double x,double *Z) {
  int it;
  double L,y;
  if (!(x>0.) || !Z) return 1;
  L=log(x);
  if (x < 1.e-4) y=x*x;
  else {
    y=(L>1.) ? L : x*x;
    if (y<1.e-30) y=1.e-30;
  }
  for (it=0;it<50;it++) {
    double f=y+.5*log(y)-L;
    double fp=1.+.5/y;
    double yn=y-f/fp;
    if (!(yn>0.) || !isfinite(yn)) yn=.5*y;
    if (fabs(yn-y) < 2.e-14*(1.+y)) { y=yn; break; }
    y=yn;
  }
  *Z=sqrt(y);
  return isfinite(*Z) ? 0 : 2;
}

int aest_background_eval(int model,double Q0,double K2,double Z0,double I0,
                         double a,double *rho_class,double *p_class,double *w,
                         double *cad2,double *Q,double *KQ) {
  double Z,q,k,kq,kqq,rho8;
  if (!rho_class || !p_class || !w || !cad2 || !Q || !KQ) return 1;
  if (!(a>0.) || !(I0>0.)) return 2;
  kq=I0/(a*a*a);
  if (model==_AEST_MODEL_COSH_) {
    double x=kq/(2.*K2*Z0);
    Z=asinh(x);
  }
  else if (model==_AEST_MODEL_EXP_) {
    double x=kq/(4.*K2*Z0);
    if (aest_exp_Z_from_x(x,&Z)) return 3;
  }
  else return 4;
  if (aest_eval_from_Z(model,Q0,K2,Z0,Z,&q,&k,&kq,&kqq)) return 5;
  rho8=q*kq-k;
  if (!(rho8>0.) || !isfinite(rho8)) return 6;
  *rho_class=rho8/3.;
  *p_class=k/3.;
  *w=k/rho8;
  *cad2=kq/(q*kqq);
  *Q=q;
  *KQ=kq;
  if (!isfinite(*w) || !isfinite(*cad2) || *cad2<0.) return 7;
  return 0;
}
