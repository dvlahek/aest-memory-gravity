# GE19 Repair44 local GE06 shift/anisotropy diagnostic runner — lock

## Status

The first local Repair44 execution path is frozen. This runner is
diagnostic-only. It cannot relabel Repair37--Repair43, certify Z21, relax
the unchanged `1e-6` science target, introduce finite physical eta,
use observational data or license lensing.

Runner:
`ge19/run_local_repair44_qge06_shift_anisotropy_row_split.sh`.

Runner commit:
`d9b199a28ec64158136e61d0e1de1ed4d26bd178`.

Runner blob:
`1efd68b10963d0afadb6f85888c704e5eb586ce8`.

Static runner audit:
- run `35965456113`;
- job `107522923462`;
- conclusion `success`.

## Bound immutable source contract

Repair44 preregistration:
- commit `3fa98dd405199cbb125c0fcc0f1c00f87b382430`;
- blob `85b20ae36482cc343ce756c00970250ea51f1624`.

Repair44 implementation:
- commit `589859ac041c54e5702bf391e8623002d944a663`;
- blob `3c734e55a8ac72874e78bd48b8fdd14112cd321f`.

Implementation lock:
- commit `51cc1c14fc4aed7073e95f8a3b506580b55ca51a`;
- blob `928c24954ab86a8029701aea69ba9c44d7121282`.

Dedicated prelock:
- workflow commit `78fe09def03d16b2fa65d3bfc667a3b1b35aa463`;
- workflow blob `343354af896c612baf957bfd598b0efaa1150164`;
- run `35965318331`;
- job `107522493691`;
- conclusion `success`.

Frozen valid Repair43:
- freeze commit `91446ddb1987e834200204cb6d8c4f8c4008a5be`;
- freeze blob `2d3daec4c6f52d9d53071ee04fd8834825c2ce10`;
- JSON/FULL SHA-256:
  `559ae65ffc5d21433799e4e33aa6d91237a9aa41b9799463971bc45dabecae44`;
- NPZ SHA-256:
  `d5c8c02c7f8272dc390ce9e4d2374a35b2ce1b14da5b60e69dc8366499bfe71c`.

Frozen valid Repair42:
- JSON SHA-256:
  `4a211581a77c1ad00e14cc398ca7a19b12642f3f3e35b416314d6721f5f81e25`;
- NPZ SHA-256:
  `a60515f3d92bbd388fd2fadae6cf2dd07f3ee68e8690b07632bbe5091e9013c5`.

Frozen valid Repair41:
- JSON SHA-256:
  `1b18fede26b021e077ffe5c8b6b7ff0dc727b4defaab48e63491c86d868d1320`;
- NPZ SHA-256:
  `6bfb87ea21d55e2a1d2b16aee9bc8d7246111f91a064a78b74d2ed946ec2ba45`.

Frozen historical Repair37 science FAIL:
- JSON SHA-256:
  `da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a`;
- NPZ SHA-256:
  `572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f`.

## Execution rule

Before execution the runner verifies exact repository source blobs and all
required local parent hashes and venv activation.

Repair44 then propagates frozen PCHIP baseline and direct382/direct763
shift row0-only, anisotropy row1-only and both-constraint-row variants
at the exact original Nt128 factor-1 Radau stages.

All full two-row constraint variants must reproduce the frozen Repair43
CONSTRAINT_ONLY Z21 and shift fields.

The shift-row0-only variant must reproduce the frozen baseline Z21 exactly,
because the unchanged canonical operator does not use source row0 for
evolution or algebraic elimination. If that fails, Repair44 is an
implementation failure, not a physical finding.

A successful diagnostic can identify the dominant constraint-source row
without selecting interpolants, relaxing thresholds, certifying Z21 or
licensing lensing.
