# Asymptotic crossover uniqueness for B1–B3

This note records a small result that is stronger than numerical root-finding: the asymptotic route equations used in B1–B3 have exactly one nontrivial crossover above `rho=1`.

Let

\[
F_k(\rho)=B_{T,k}^{\rm asy}(\rho)-B_{D,k}^{\rm asy}(\rho).
\]

## B1

For B1,

\[
F_1(\rho)=\frac{\rho^6}{3780}
-\frac{C_9}{6}
-\frac12(1-\rho^{-2})
-\frac{A}{3}(1-\rho^{-3}).
\]

Then

\[
F_1'(\rho)
=\rho^{-4}\left(\frac{\rho^9}{630}-\rho-A\right).
\]

Define

\[
G_1(\rho)=\frac{\rho^9}{630}-\rho-A.
\]

Its derivative is

\[
G_1'(\rho)=\frac{\rho^8}{70}-1.
\]

Thus `G_1` decreases until `rho=70^(1/8)` and increases thereafter. Since `G_1(1)<0` and `G_1(rho)->infinity`, it has exactly one zero on `(1,infinity)`. Hence `F_1` first decreases and then increases. Moreover

\[
F_1(1)=\frac1{3780}-\frac{C_9}{6}<0,
\]

while `F_1(rho)->infinity`. Therefore B1 has exactly one crossover on `(1,infinity)`.

## B2

For B2,

\[
F_2(\rho)=\frac{\rho^7}{4410}
-\frac1{4410}
-\frac{A_{\rm tail}}2(1-\rho^{-2})
-e^{-4}(1-\rho^{-1}).
\]

Its derivative is

\[
F_2'(\rho)
=\rho^{-3}\left(
\frac{\rho^9}{630}-A_{\rm tail}-e^{-4}\rho
\right).
\]

Set

\[
G(\rho)=\frac{\rho^9}{630}-A_{\rm tail}-e^{-4}\rho.
\]

Then

\[
G'(\rho)=\frac{\rho^8}{70}-e^{-4}.
\]

`G'` has one zero for `rho>1`, `G(1)<0`, and `G(rho)->infinity`. Thus `G` has exactly one zero on `(1,infinity)`, so `F_2` first decreases and then increases. Since `F_2(1)=0`, `F_2'(1)<0`, and `F_2(rho)->infinity`, there is exactly one nontrivial B2 crossover above `rho=1`.

## B3

For B3,

\[
F_3(\rho)=\frac{\rho^6}{3780}
-\frac1{3780}
-\frac{A_{\rm tail}}3(1-\rho^{-3})
-\frac{e^{-4}}2(1-\rho^{-2}).
\]

Its derivative is

\[
F_3'(\rho)
=\rho^{-4}\left(
\frac{\rho^9}{630}-A_{\rm tail}-e^{-4}\rho
\right)
=\rho^{-4}G(\rho).
\]

The same `G` as in B2 controls the sign. Since `F_3(1)=0`, `F_3'(1)<0`, and `F_3(rho)->infinity`, B3 also has exactly one nontrivial crossover on `(1,infinity)`.

## Consequence

The constants

\[
\rho_*^{B1},\qquad \rho_*^{B2},\qquad \rho_*^{B3}
\]

are not artifacts of a root-finding convention. Each is the unique nontrivial positive route transition above the resolved/unresolved boundary `rho=1` for its asymptotic certificate pair.

This uniqueness statement applies to the asymptotic route equations. It does not, by itself, claim a general uniqueness theorem for arbitrary finite-`h` models outside B1–B3.
