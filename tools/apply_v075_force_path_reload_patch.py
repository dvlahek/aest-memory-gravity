#!/usr/bin/env python3
from pathlib import Path
import argparse
import json


def replace_once(path, old, new, label):
    p = Path(path)
    s = p.read_text()
    n = s.count(old)
    if n != 1:
        raise RuntimeError(f'{label}: expected one anchor, found {n} in {p}')
    p.write_text(s.replace(old, new, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('class_root')
    args = ap.parse_args()
    root = Path(args.class_root).resolve()
    repo = Path(__file__).resolve().parents[1]
    src = root / 'source' / 'aest_memory.c'

    replace_once(
        src,
        'static int _aest_tf_loaded = 0;\nstatic double _aest_tf_lambda = 0.;\n',
        'static int _aest_tf_loaded = 0;\nstatic char _aest_tf_loaded_path[4096] = "";\nstatic double _aest_tf_lambda = 0.;\n',
        'v075 force-path state',
    )

    old = '''  slam = getenv("AEST_TANGENT_LAMBDA");\n  requested_lambda = (slam == NULL) ? 0. : strtod(slam,NULL);\n  if (_aest_tf_loaded) {\n    if (_aest_tf_n > 0) {\n      _aest_tf_lambda = requested_lambda;\n      return;\n    }\n    if (requested_lambda == 0.) {\n      _aest_tf_lambda = 0.;\n      return;\n    }\n    _aest_tf_loaded = 0;\n  }\n  _aest_tf_loaded = 1;\n  _aest_tf_lambda = requested_lambda;\n  path = getenv("AEST_TANGENT_FORCE_FILE");\n  if (path == NULL || path[0] == '\\0' || _aest_tf_lambda == 0.) return;\n'''

    new = '''  slam = getenv("AEST_TANGENT_LAMBDA");\n  requested_lambda = (slam == NULL) ? 0. : strtod(slam,NULL);\n  path = getenv("AEST_TANGENT_FORCE_FILE");\n\n  /* v0.75 technical runtime fix: v0.75 evaluates several preregistered\n     k-resolution levels inside one Python process, with a distinct forcing\n     table path for each level. The v0.63 multi-instance fix refreshed only\n     lambda and therefore could retain the previous resolution's table.\n     Reload only when the requested force-file path changes. */\n  if (_aest_tf_loaded && _aest_tf_n > 0) {\n    if (path != NULL && path[0] != '\\0' && strcmp(path,_aest_tf_loaded_path) == 0) {\n      _aest_tf_lambda = requested_lambda;\n      return;\n    }\n    free(_aest_tf_k);\n    free(_aest_tf_tau);\n    free(_aest_tf_f);\n    _aest_tf_k = NULL;\n    _aest_tf_tau = NULL;\n    _aest_tf_f = NULL;\n    _aest_tf_n = 0;\n    _aest_tf_cache_k = -1.;\n    _aest_tf_cache_lo = 0;\n    _aest_tf_cache_hi = 0;\n    _aest_tf_loaded = 0;\n    _aest_tf_loaded_path[0] = '\\0';\n  }\n  if (_aest_tf_loaded) {\n    if (requested_lambda == 0.) {\n      _aest_tf_lambda = 0.;\n      return;\n    }\n    _aest_tf_loaded = 0;\n  }\n  _aest_tf_loaded = 1;\n  _aest_tf_lambda = requested_lambda;\n  if (path == NULL || path[0] == '\\0' || _aest_tf_lambda == 0.) return;\n'''

    replace_once(src, old, new, 'v075 force-path reload logic')

    replace_once(
        src,
        '''  fclose(fp);\n  if (_aest_tf_n < 2) {\n''',
        '''  fclose(fp);\n  snprintf(_aest_tf_loaded_path,sizeof(_aest_tf_loaded_path),"%s",path);\n  if (_aest_tf_n < 2) {\n''',
        'v075 remember loaded force path',
    )

    s = src.read_text()
    checks = {
        'path_state_present': 'static char _aest_tf_loaded_path[4096]' in s,
        'path_change_detected': 'strcmp(path,_aest_tf_loaded_path) == 0' in s,
        'old_table_freed_on_path_change': 'free(_aest_tf_k);' in s and 'free(_aest_tf_tau);' in s and 'free(_aest_tf_f);' in s,
        'loaded_path_recorded': 'snprintf(_aest_tf_loaded_path,sizeof(_aest_tf_loaded_path),"%s",path);' in s,
        'strict_k_match_unchanged': 'if (rel > 2.e-10)' in s,
        'external_force_interpolation_unchanged': 'return _aest_tf_lambda*(f0 + x*(f1-f0));' in s,
    }
    report = {
        'classification': 'V075_MULTI_RESOLUTION_FORCE_PATH_RELOAD_TECHNICAL_FIX',
        'source_failed_runs': [34282625854, 34283332671, 34283360599],
        'failure_mode': 'successive resolution levels reused the first loaded AEST_TANGENT_FORCE_FILE because the v0.63 loader refreshed lambda but not the file path',
        'physics_modified': False,
        'solver_tolerances_modified': False,
        'resolution_sequence_modified': False,
        'fixed_grid_modified': False,
        'tangent_amplitudes_modified': False,
        'science_gates_modified': False,
        'strict_force_k_matching_modified': False,
        'checks': checks,
    }
    if not all(checks.values()):
        raise RuntimeError(report)
    (repo / 'results').mkdir(exist_ok=True)
    (repo / 'results' / 'v075_force_path_reload_patch.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
