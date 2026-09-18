# NL1C7B4 Repair09 — local attempt 01 harness-failure freeze

## Status

Frozen record of the first local Repair09 launch attempt. This is **not** a science result and carries no Repair09 terminal classification.

## Observed local output

```text
fatal: Not a valid commit name ee97aec3e274f3996c87c622a770f5233666f7f6
LOCK ancestry failure: ee97aec3e274f3996c87c622a770f5233666f7f6
EXIT=91
```

## Localization

The failure occurred in the runner's first provenance ancestry check, before:

- Repair08 JSON or NPZ hash verification;
- dense-trace input use;
- invocation of `nl1c7b/initial_constraint_certification_repair09.py`;
- creation of a Repair09 result JSON;
- any raw B4 constraint evaluation.

Therefore this attempt is a pre-evaluation harness failure only.

## Root cause

The runner and implementation-lock text contained an incorrect full preregistration commit literal:

`ee97aec3e274f3996c87c622a770f5233666f7f6`

The actual preregistration commit already present in the branch ancestry is:

`ee97aec340b9b8dcc508d092730b795f01eb65bd`

with preregistration file blob:

`3e4f6ed8cf8a70a791f0ffef68c9b780ba7552c6`.

The preregistration file itself is unchanged. The Repair09 evaluator blob remains:

`0cd67cecfbd590cb8819ad37314dc5b49047bc93`.

No physics equation, state input, threshold, gate, case, radial point, Y family, beta value, or classification rule was evaluated or changed by this failed attempt.

## Licensed correction

A separate provenance-lock correction may replace only the incorrect preregistration commit literal in the execution harness and document the correction. The original implementation-lock file must remain historically unchanged. The corrected runner must continue to require the original preregistration blob, original evaluator blob, original implementation-lock blob, exact Repair08 hashes, and all frozen B4 thresholds.
