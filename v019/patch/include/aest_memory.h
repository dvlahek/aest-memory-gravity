#ifndef __AEST_MEMORY_V019__
#define __AEST_MEMORY_V019__

#ifdef __cplusplus
extern "C" {
#endif

#define _AEST_MODEL_COSH_ 1
#define _AEST_MODEL_EXP_ 2
#define AEST_MEMORY_V019_NODES 20

const char *aest_memory_module_version(void);
double aest_memory_kernel20(double A);
int aest_memory_selfcheck(double *max_rel);

int aest_background_calibrate(int model,
                              double Q0,
                              double K2,
                              double Z0,
                              double target_eightpiG_rho,
                              double *I0);

int aest_background_eval(int model,
                         double Q0,
                         double K2,
                         double Z0,
                         double I0,
                         double a,
                         double *rho_class,
                         double *p_class,
                         double *w,
                         double *cad2,
                         double *Q,
                         double *KQ);

#ifdef __cplusplus
}
#endif

#endif
