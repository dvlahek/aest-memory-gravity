#!/usr/bin/env python3
from pathlib import Path
import argparse, json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('class_root')
    a = ap.parse_args()
    root = Path(a.class_root).resolve()
    p = root / 'source' / 'aest_memory.c'
    s = p.read_text()

    old = '''static void _aest_tangent_load_force(void) {\n  const char *path;\n  const char *slam;\n  FILE *fp;\n  size_t cap = 0;\n  double k,tau,f;\n  if (_aest_tf_loaded) return;\n  _aest_tf_loaded = 1;\n  slam = getenv("AEST_TANGENT_LAMBDA");\n  _aest_tf_lambda = (slam == NULL) ? 0. : strtod(slam,NULL);\n  path = getenv("AEST_TANGENT_FORCE_FILE");\n  if (path == NULL || path[0] == '\\0' || _aest_tf_lambda == 0.) return;\n'''

    new = '''static void _aest_tangent_load_force(void) {\n  const char *path;\n  const char *slam;\n  FILE *fp;\n  size_t cap = 0;\n  double k,tau,f;\n  double requested_lambda;\n\n  /* v0.63 technical runtime fix: classy can evaluate several Class\n     instances inside one Python process. Refresh the signed tangent\n     amplitude for every instance, and allow the force table to be\n     loaded after an initial unforced base instance. No forcing equation\n     or predeclared physical parameter is changed here. */\n  slam = getenv("AEST_TANGENT_LAMBDA");\n  requested_lambda = (slam == NULL) ? 0. : strtod(slam,NULL);\n  if (_aest_tf_loaded) {\n    if (_aest_tf_n > 0) {\n      _aest_tf_lambda = requested_lambda;\n      return;\n    }\n    if (requested_lambda == 0.) {\n      _aest_tf_lambda = 0.;\n      return;\n    }\n    _aest_tf_loaded = 0;\n  }\n  _aest_tf_loaded = 1;\n  _aest_tf_lambda = requested_lambda;\n  path = getenv("AEST_TANGENT_FORCE_FILE");\n  if (path == NULL || path[0] == '\\0' || _aest_tf_lambda == 0.) return;\n'''

    n = s.count(old)
    if n != 1:
        raise RuntimeError(f'v0.63 classy runtime-loader anchor count={n}, expected 1')
    s = s.replace(old, new, 1)
    p.write_text(s)

    checks = {
        'multi_instance_comment': 'v0.63 technical runtime fix' in s,
        'refresh_lambda': '_aest_tf_lambda = requested_lambda;' in s,
        'allow_load_after_base': '_aest_tf_loaded = 0;' in s,
        'external_force_equation_unchanged': 'return _aest_tf_lambda*(f0 + x*(f1-f0));' in s,
    }
    report = {
        'classification': 'V063_CLASSY_MULTI_INSTANCE_TANGENT_LOADER_TECHNICAL_FIX',
        'physics_modified': False,
        'purpose': 'Allow base, +lambda, and -lambda Class instances in one Python process to use their requested runtime tangent amplitude.',
        'checks': checks,
    }
    if not all(checks.values()):
        raise RuntimeError(report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
