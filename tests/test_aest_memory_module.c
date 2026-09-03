#include <stdio.h>
#include "aest_memory.h"

int main(void) {
  double max_rel = -1.0;
  int status = aest_memory_selfcheck(&max_rel);
  printf("module=%s\n",aest_memory_module_version());
  printf("class_target=%s\n",aest_memory_target_class_version());
  printf("class_sha=%s\n",aest_memory_target_class_sha());
  printf("nodes=%d\n",aest_memory_nnodes());
  printf("max_relative_kernel_error=%.17g\n",max_rel);
  printf("status=%d\n",status);
  return status;
}
