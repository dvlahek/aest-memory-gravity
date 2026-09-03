#include <math.h>
#include <stddef.h>
#include "aest_memory.h"

static const double _aest_nodes[AEST_MEMORY_V018_NODES] = {
  0.00031622776601683794,
  0.00073861998220793579,
  0.0017252105499420409,
  0.0040296113202003998,
  0.0094120496726806703,
  0.021983926488622893,
  0.05134832907437549,
  0.11993539462092344,
  0.28013567611988671,
  0.65431891297129618,
  1.5283067326587687,
  3.5696988468260624,
  8.3378222347178834,
  19.47483039908753,
  45.487779470037772,
  106.24678308940409,
  248.16289228368237,
  579.63939533849612,
  1353.8761800225418,
  3162.2776601683795
};

static const double _aest_weights[AEST_MEMORY_V018_NODES] = {
  0.00035498327646994379,
  0.00032843124388271791,
  0.00095164396217085119,
  0.0021660594007921947,
  0.0050915252066982596,
  0.011856289290614601,
  0.027673234995271925,
  0.063823570857272541,
  0.14038300101017823,
  0.24703490212236523,
  0.24833679544478374,
  0.13923159504266835,
  0.064744083310698405,
  0.026983754235172484,
  0.012361813713965936,
  0.0047071074300463695,
  0.0024983339993659695,
  0.00058370621523949856,
  0.00080089966965596034,
  0
};

const char *aest_memory_module_version(void) {
  return "v0.18";
}

const char *aest_memory_target_class_version(void) {
  return AEST_MEMORY_V018_TARGET_VERSION;
}

const char *aest_memory_target_class_sha(void) {
  return AEST_MEMORY_V018_TARGET_SHA;
}

int aest_memory_nnodes(void) {
  return AEST_MEMORY_V018_NODES;
}

double aest_memory_node(int j) {
  if (j < 0 || j >= AEST_MEMORY_V018_NODES) return -1.0;
  return _aest_nodes[j];
}

double aest_memory_weight(int j) {
  if (j < 0 || j >= AEST_MEMORY_V018_NODES) return -1.0;
  return _aest_weights[j];
}

double aest_memory_kernel20(double A) {
  double a2, sum;
  int j;
  if (A <= 0.0) return 0.0;
  a2 = A*A;
  sum = 0.0;
  for (j=0; j<AEST_MEMORY_V018_NODES; ++j) {
    double r2 = _aest_nodes[j]*_aest_nodes[j];
    sum += _aest_weights[j] * a2/(r2+a2);
  }
  return sum;
}

int aest_memory_selfcheck(double *max_rel) {
  int j,n;
  double mr = 0.0;
  for (j=0; j<AEST_MEMORY_V018_NODES; ++j) {
    if (!(_aest_nodes[j] > 0.0)) return 1;
    if (!(_aest_weights[j] >= 0.0)) return 2;
  }
  for (n=0; n<=2400; ++n) {
    double t = -3.0 + 6.0*((double)n/2400.0);
    double A = pow(10.0,t);
    double exact = A/(1.0+A);
    double approx = aest_memory_kernel20(A);
    double rel = fabs(approx-exact)/exact;
    if (rel > mr) mr = rel;
  }
  if (max_rel != NULL) *max_rel = mr;
  if (!(mr < 2.0e-4)) return 3;
  return 0;
}
