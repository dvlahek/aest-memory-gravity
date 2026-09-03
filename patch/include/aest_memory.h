#ifndef __AEST_MEMORY_V018__
#define __AEST_MEMORY_V018__

#ifdef __cplusplus
extern "C" {
#endif

#define AEST_MEMORY_V018_TARGET_VERSION "v3.3.4"
#define AEST_MEMORY_V018_TARGET_SHA "e85808324f51fc694d12e3ed7439552a3c3f9540"
#define AEST_MEMORY_V018_NODES 20

const char *aest_memory_module_version(void);
const char *aest_memory_target_class_version(void);
const char *aest_memory_target_class_sha(void);
int aest_memory_nnodes(void);
double aest_memory_node(int j);
double aest_memory_weight(int j);
double aest_memory_kernel20(double A);
int aest_memory_selfcheck(double *max_rel);

#ifdef __cplusplus
}
#endif

#endif
