# v0.51 provenance resolution

The v0.51 objective-reproduction audit confirmed that the v0.42 canonical endpoint reproduces exactly under the locked evaluator, while the reported plus/minus/cross endpoint S/N values do not.

The cause is now identified directly in the exact v0.42 run code (`v042/refit_multistart_continued.py` at run head `f750b33d9c660679e44586902f9cecac8ad0378d`). The continuation wrapper executes:

```python
r.START = dict(STARTS[a.start])
r.main()
```

but `v031/refit_baseline.py::main()` constructs the reference spectrum with:

```python
ref_cl = run_class(class_root, ref_tag, 'base', 0.1, START)
```

Therefore, after the wrapper overwrites `r.START`, each multistart member also receives a different KB=0.1 reference cosmology. The reported v0.42 plus/minus/cross objective values are consequently start-specific-reference objectives, not values of one common locked objective.

This explains the v0.51 reproduction results:

- canonical: 2.32803921427129 -> 2.32803921427129 (exact)
- plus: 0.8590293860134628 -> 80.95906165647773 under the common locked reference
- minus: 4.472092214889027 -> 76.2743526453326
- cross: 4.259593544697129 -> 290.5410248357708

Scientific consequence: the old v0.42 four-start spread must not be interpreted as basin dependence of a single objective, and the old bridge topology that used those endpoint objective labels is not scientifically interpretable. This is a provenance/evaluator bug in the old certification wrapper, not an AeST-physics failure.

The v0.50 LM run does not make this mutation: it keeps `BASE = dict(r.START)` fixed and evaluates all starts against the same fixed KB=0.1 reference. The correct next optimizer test is therefore v0.52 continuation from the verified v0.50 endpoints under that same common objective, with the original spread gate `< 0.5` retained.
