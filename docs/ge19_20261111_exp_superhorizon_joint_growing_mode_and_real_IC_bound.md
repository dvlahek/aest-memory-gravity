# GE19 — vodeći zajednički superhorizontski mod i stvarna veličina AeST IC nesklada

**Datum:** 11. studenoga 2026.  
**Klasifikacija:** `LEADING_RADIATION_ADIABATIC_MODE_SUPPORTED / FINITE_K_COUPLED_MEMORY_OPEN / PHYSICS_GO_BLOCK / DES_NOT_DETECTED`.

Ovaj dokument zaključuje jedan fizikalni račun, **bez nove CLASS numerike, bez DES fita i bez mijenjanja zamrznute teorije**. Izvršiv izvor i samostalni JSON sa 16/16 simboličkih provjera arhivirani su na istoj grani. Kanonska **izvorno zaključana WSL reprodukcija još nije izvedena** za ovaj konkretan novi test.

## 1. Fizikalna pozadina iz zamrznutog Exp modela

Originalni izvor `v019/patch/source/aest_memory.c` i izvorni benchmark `v019/ini/aest_exp.ini` definiraju

\[
Q=Q_0+Z_0Z,\qquad
K=2K_2Z_0^2(e^{Z^2}-1),\qquad
K_Q=4K_2Z_0Ze^{Z^2}=I_0/a^3,
\]

gdje su \(Q_0=10^{-4}\), \(Z_0=10^{-17}\), \(K_2=9500\), a normalizacija je određena \(\omega_{\rm cdm}=0.1201075\), kao *ciljna gustoća efektivnog AeST fluida*, ne dodatna fizička CDM komponenta.

Definiramo \(\rho_A=(QK_Q-K)/3\), \(p_A=K/3\), \(w_A=p_A/\rho_A\) i \(c_a^2=K_Q/(QK_{QQ})\). Iz izvornog oblika slijedi
\[
\frac{K}{K_Q}=\frac{Z_0(1-e^{-Z^2})}{2Z},\quad
w_A=\frac{K/K_Q}{Q-K/K_Q},\quad
c_a^2=\frac{Z_0Z}{Q(1+2Z^2)}.
\]

U neovisno izračunatoj pozadini za \(0<a\le1\) dobiveno je
\[
0<w_A\lesssim1.14\times10^{-14},\qquad
0<c_a^2\lesssim1.11\times10^{-14}.
\]
Primjeri: \(a=1\): \(w_A=1.13822100959218\times10^{-14}\), \(c_a^2=1.10947351103636\times10^{-14}\); \(a=10^{-4}\): \(w_A=7.33328154803501\times10^{-15}\); \(a=10^{-8}\): \(w_A=5.81680091313316\times10^{-15}\).

**Promjena zaključka o početnim uvjetima:** naslijeđeni CDM izraz \(\delta_A=(3/4)\delta_\gamma\) nije matematički jednako točan kao adijabatski \(\delta_A=(3/4)(1+w_A)\delta_\gamma\) kad je \(w_A\ne0\), ali **za ovaj zamrznuti Exp benchmark njegova vodeća relativna razlika reda je \(10^{-14}\)**. To samo po sebi ne objašnjava prethodni nazubljeni \(10^{-6}\)-odziv. Nema razloga zbog toga ad hoc mijenjati izvorne CLASS podatke.

## 2. Zajednički vodeći fizički adijabatski mod

Pretpostavke: rana radijacijska era \(a\propto\tau\), \(\mathcal H=1/\tau\), \(k\tau\ll1\), \(\rho_A/\rho_r\ll1\), čvrsto vezani fotoni i barioni, slobodno strujajuća neutrina s frakcijom radijacije \(R_\nu\), jedan adijabatski rastući mod amplitude \(\Psi_0\), i **izabrani** homogeni pomoćni modovi \(q_{j,h}=0\).

Rješenje vodećeg reda, u originalnim CLASS/Newtonian konvencijama:
\[
\begin{gathered}
\Psi=\Psi_0,\qquad
\Phi=(1+2R_\nu/5)\Psi_0,\\
\delta_\gamma=\delta_\nu=-2\Psi_0,\quad
\delta_b=-3\Psi_0/2,\quad
\delta_A=-3(1+w_A)\Psi_0/2,\\
\theta_\gamma=\theta_\nu=\theta_b=\theta_A=k^2\tau\Psi_0/2,\qquad
\sigma_\nu=(k\tau)^2\Psi_0/15,\\
\varphi_A=aQ\tau\Psi_0/2,\quad
\alpha_A=-a\tau\Psi_0/2,\quad
\delta Q=-3Qc_a^2\Psi_0/2,\\
\chi=\varphi_A+Q\alpha_A=0,\quad
E_A=\dot\alpha_A+\Psi=0,\quad
q_j=p_j=0\ \text{u odabranoj neuzbuđenoj kupelji}.
\end{gathered}
\]

Izvorna AeST gustoća iz akcije, uz \(\chi=E_A=0\), daje
\[
D_A^{\rm action}=\frac{QK_{QQ}\delta Q}{3}
=-\frac12QK_Q\Psi_0
=\rho_A\delta_A.
\]
Jednadžba tlaka, skalarna faza, AeST Eulerova jednadžba brzine i vodeća kontinuitetna jednadžba su sukladne; radijacijske Einsteinove Hamiltonova i impulsna jednadžba te neutrinska smična perturbacija također prolaze vodeće provjere. Prema originalnom naboju, njegov vremenski dio je očuvan u granici \(k\tau\to0\) budući da je \(a^3K_Q=I_0\). Slobodni NL0B modovi su **isključeni kao dodatna početna pretpostavka**; regularnost sama po sebi ih ne isključuje.

Ukupno **16/16 preciznih simboličkih identiteta** iz reproducibilnog programa prolaze u samostalnoj analizi. Time se ne dokazuje cijeli konačno-\(k\) eigenvektor, jedinstvenost adijabatskog početnog stanja ni numerička stabilnost integracije.

**Važno:** u ovom vodećem modu \(B_\chi=0\), pa \(\eta\)-memorija nema izravni vodeći odgovor. Ovo nije argument da je teorija bez memorije: odgovor počinje u sljedećim nenultim redovima.

## 3. Što ostaje otvoreno

Jedini sada fizikalno opravdan korak jest **jedan zajednički sljedeći red superhorizontskog razvoja** kroz \(\mathcal O((k\tau)^2)\) i \(\mathcal O(\rho_A/\rho_r)\), uključujući vremenske promjene \(w_A,c_a^2\), smičnost neutrina, AeST skalar/aeter i retarded \(q_j,p_j\). Treba izvesti gdje se prvi put pojavljuju nenulti \(\chi,E_A,B_\chi\), i potvrditi da ista akcija daje Einsteinove izvore i scalar-charge Ward identitet.

Bez tog zatvaranja **nema** `PHYSICS_GO`, proizvodnog fizikalnog \(\partial_\eta P_{gW}\), kvalificirane numeričke konvergencije ili DES Y3 detekcije. Prijašnja jaka oscilacija predznaka u prijenosnim funkcijama nije opravdano proglašena ni signalom ni numeričkom pogreškom.

## 4. Provenijencija i reproducibilnost

- [Jedan izvršivi program za 16 identiteta](../ge19/physics_gate/frozen_exp_superhorizon_growing_mode_20261111.py), Git blob `e0a2562b2c728c1deef2eadb784f6c750aeef3b7`.
- [Arhivirani samostalni JSON](../results/ge19_frozen_exp_leading_growing_mode_20261111_standalone.json), Git blob `49c86301f95cff22bb764e1b7f52aca013c590f6`, klasifikacija `production_physics_go=false`.
- [Prethodni zajednički all-species izvorni pregled](ge19_20261111_all_species_Einstein_operator_and_adiabatic_IC_block.md).

Po potrebi jedno **kratko WSL potvrđivanje originalnih zaključanih izvora**, koje ne pokreće CLASS:

~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
set -o pipefail
python3 -u ge19/physics_gate/frozen_exp_superhorizon_growing_mode_20261111.py \
  --out results/ge19_frozen_exp_leading_growing_mode_20261111_wsl.json \
  2>&1 | tee results/ge19_frozen_exp_leading_growing_mode_20261111_wsl.log
echo "EXIT=${PIPESTATUS[0]}"
~~~

Očekivano: `GE19_FROZEN_EXP_SOURCE_LOCKS_PASS 4`, `GE19_FROZEN_EXP_LEADING_GROWING_MODE_PASS 16` i `GE19_FULL_PHYSICS_GO False`. Uporaba druge izvorne revizije ili neuspjeh testa mora biti prijavljen, a ne automatski popravljan.
