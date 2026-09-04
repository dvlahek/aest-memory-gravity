# v0.19t — tauH0=1 positive fixed-bath compression

v0.19s showed that one sparse fixed bath cannot represent the full `tau H0 = 1 ... 0.001` family with the requested accuracy. The failure is concentrated at the smallest tau values. This does not obstruct the first finite-memory cosmology gate, which has always used `tau H0 = 1`.

For `tau H0 = 1`, the direct v0.19r N=512 tan-theta quadrature is already much more accurate: on the held-out Cosh/Exp source histories its worst normalized L2 error relative to the N=16384 continuum reference is below `5e-4`.

v0.19t therefore asks a narrower numerical question: can that already validated tauH0=1 response be compressed to a practical positive fixed-frequency bath?

The candidate frequencies are the direct N=512 tan-theta nodes. Positive weights are selected on alternating training k values and validated on the interlaced k values for both Cosh and Exp. The retained frequencies and weights are constant in time and independent of H(t).

Primary compressed gate:

- median held-out L2 `< 2e-4`;
- p95 `< 5e-4`;
- worst case `< 1e-3`;
- at most 128 active modes;
- all frequencies and weights positive;
- total weight normalized to one.

If sparse compression does not pass, the direct N=512 bath remains a validated fallback for the first tauH0=1 small-eta CLASS response diagnostic. A compression failure is not a failure of the continuum memory model.
