#include <stdio.h>
#include <math.h>
#include "aest_memory.h"

static int run_one(int model,double KB,double Q0,double K2,double Z0,
                   double H0,double Omega) {
  double I0,target=3.*Omega*H0*H0;
  double rho,p,w,cad,Q,KQ;
  int i;
  (void)KB;
  if (aest_background_calibrate(model,Q0,K2,Z0,target,&I0)) return 10+model;
  if (aest_background_eval(model,Q0,K2,Z0,I0,1.,&rho,&p,&w,&cad,&Q,&KQ)) return 20+model;
  printf("model=%d I0=%.17g rho_today=%.17g target_rho=%.17g rel=%.3e w_today=%.3e cad2_today=%.3e Q_today=%.17g\n",
         model,I0,rho,target/3.,fabs(rho-target/3.)/(target/3.),w,cad,Q);
  if (fabs(rho-target/3.)/(target/3.)>2e-12) return 30+model;
  for (i=0;i<=240;i++) {
    double loga=-12.+12.*i/240.;
    double a=pow(10.,loga);
    if (aest_background_eval(model,Q0,K2,Z0,I0,a,&rho,&p,&w,&cad,&Q,&KQ)) return 40+model;
    if (!(rho>0.) || !(p>=0.) || !(w>=0.) || !(cad>=0.) || !isfinite(rho)) return 50+model;
  }
  return 0;
}

int main(void) {
  const double H0=(67.32117/299792.458);
  const double h=0.6732117;
  const double Omega=.1201075/(h*h);
  double mr=-1.;
  int s1,s2,sm;
  sm=aest_memory_selfcheck(&mr);
  s1=run_one(_AEST_MODEL_COSH_,.5,.1,7.5e3,1e-9,H0,Omega);
  s2=run_one(_AEST_MODEL_EXP_,.1,1e-4,9.5e3,1e-17,H0,Omega);
  printf("kernel_max_rel=%.17g kernel_status=%d cosh_status=%d exp_status=%d\n",mr,sm,s1,s2);
  return (sm||s1||s2) ? 1 : 0;
}
