# GE19 — uvjetni rastući mod spregnutog skalarnog aetera i pozitivne memorijske kupelji

**12. studenoga 2026.**  
**Odluka:** `REDUCED_FROZEN_GROWTH_ROOT_IF_THRESHOLD / FULL_EINSTEIN_CONSTRAINT_MODE_OPEN / PHYSICS_GO_BLOCK / NO_DES_DETECTION`.

Analiza je izvedena iz istog reduciranog, akcijski normaliziranog GE19 sustava kao prethodne WSL-provjere 15/15, 14/14 i 9/9. **Nema novih CLASS izvođenja, fitanja DES podataka, podešavanja \(\eta\) ni promjena izvornog modela.** Izolirana NL0B kupelj pasivna je, ali to *ne dokazuje* stabilnost spregnutog aeterskog podsustava.

## 1. Izvorne evolucijske jednadžbe

Vlastito vrijeme \(t\), \(H=\dot a/a\), \(C=2-K_B\), \(R_A=\rho_A+p_A=QK_Q/3\), \(c_a^2=K_Q/(QK_{QQ})\), \(\Delta_A=\delta_A/(1+w_A)+3aH\theta_A/k^2\):
\[
\dot\chi=QE_A+Qc_a^2\left[
\Delta_A-\frac{3H\chi}{Q}+\frac{k^2}{3a^2R_A}(K_BE_A+C\chi)
\right],\tag{1}
\]
\[
K_B(\dot E_A+HE_A)=
K_Q\chi-C[\dot\chi-QE_A+(H+Q)\chi]-\frac{\eta Q}{4}B_\chi,\tag{2}
\]
\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}\frac{k\chi}{a},\qquad
B_\chi=\sum_j\left(w_j\chi-\frac{a\omega_j\sqrt{w_j}}{k}q_j\right).\tag{3}
\]

Ovdje \(K_B>0,Q>0,H>0,\eta\ge0,\omega_j>0,w_j\ge0\). Svi pozitivni pomoćni modovi su uključeni, a \(\gamma=1/4\) je *izdvojeni reduciranom akcijom opravdan kandidat*.

Ako se \(\Delta_A\) u ovom podsustavu zada kao vanjska pobuda, njezin izravan vektor je **točno** \(Qc_a^2(1,-C/K_B)^T\). Za trenutno zamrznute \(q_j\), matrica \((\chi,E_A)\) ima elemente
\[
\begin{aligned}
M_{11}&=-3Hc_a^2+\frac{Qc_a^2Ck^2}{3a^2R_A},&
M_{12}&=Q\left(1+\frac{c_a^2K_Bk^2}{3a^2R_A}\right),\\
M_{21}&=\frac{K_Q-C(H+Q+M_{11})-\eta QW_b/4}{K_B},&
M_{22}&=-H-\frac{CQc_a^2k^2}{3a^2R_A},\quad W_b=\sum_jw_j .
\end{aligned}
\]
Njegov je **točan trag**
\[
\boxed{\operatorname{tr}M=-H(1+3c_a^2).}\tag{4}
\]
Negativan trag sam po sebi ne isključuje sedlastu, rastuću komponentu.

## 2. Karakteristična jednadžba sa svim pomoćnim oscilatorima

Radi *lokalne* analize zamrznimo koeficijente u jednoj FLRW epohi. Formalno uzmimo longitudinalni limit \(k\to0^+\) i \(q_j\propto k\), ali **ne** postavljajmo nezavisni fizički \(k=0\) mod. Tražimo matematičke eksponencijalne modove \(e^{\lambda t}\) s *vanjskom* \(\Delta_A=0\). Tada
\[
\frac{q_j}{\chi}=
\frac{\omega_j\sqrt{w_j}k}
{a(\lambda^2+3H\lambda+\omega_j^2)},\quad
\frac{B_\chi}{\chi}=\mathcal W(\lambda),
\]
\[
\boxed{\mathcal W(\lambda)=
\sum_j w_j\frac{\lambda(\lambda+3H)}
{\lambda^2+3H\lambda+\omega_j^2}.}\tag{5}
\]
Pritom \(E_A/\chi=(\lambda+3Hc_a^2)/Q\). Eliminiranjem svih \(q_j\) dobivamo
\[
\boxed{
F(\lambda)=
\frac{K_B}{Q}(\lambda+H)(\lambda+3Hc_a^2)
-\left[K_Q-C(H+Q-3Hc_a^2)\right]
+\frac{\eta Q}{4}\mathcal W(\lambda)=0.
}\tag{6}
\]

Za realno \(\lambda\ge0\), \(F\) je kontinuirana, a
\[
\mathcal W(0)=0,\qquad
\mathcal W'(\lambda)=
\sum_j\frac{w_j\omega_j^2(2\lambda+3H)}
{(\lambda^2+3H\lambda+\omega_j^2)^2}\ge0,
\]
\[
F'(\lambda)=\frac{K_B}{Q}[2\lambda+H(1+3c_a^2)]
+\frac{\eta Q}{4}\mathcal W'(\lambda)>0,\qquad
F(+\infty)=+\infty.
\]

**Uvjetni teorem za ovaj zamrznuti reducirani sustav:** postoji **točno jedan pozitivan realni korijen** ako i samo ako
\[
\boxed{
K_Q>(2-K_B)(H+Q-3Hc_a^2)+\frac{3K_BH^2c_a^2}{Q}.
}\tag{7}
\]
Naime \(F(0)<0\) točno pod (7). Ako uvjet nije zadovoljen, **ne postoji pozitivan realni korijen**, ali ovo samo po sebi ne isključuje druge kompleksne nestabilne modove ili prolazno pojačanje.

Za uvjet (7), pozitivna kupelj ga može **usporiti**, jer
\[
\frac{\partial\lambda}{\partial\eta}
=-\frac{Q\mathcal W(\lambda)}{4F'(\lambda)}\le0,
\]
ali ga ne može ukloniti konačnim \(\eta\), jer je \(\mathcal W(0)=0\). **Ovo se odnosi na fiksiranu lokalnu matricu**, a ne na konačno vremenski evoluirajući kozmos.

## 3. Zašto je ovo fizički relevantno, ali još nije dokaz nestabilnosti

U primjeru *daleko pojednostavljenog* ranog materijskog režima \(Q\approx Q_0\), \(K_Q\gg(2-K_B)(H+Q)\), \(H\gg Q\), \(c_a^2\simeq0\), zanemarimo vanjsku \(\Delta_A\) i vodeći bath feedback. Tada bi (samo za taj matematički podsustav)
\[
\ddot\chi+H\dot\chi-\frac{QK_Q}{K_B}\chi\simeq0.
\]
Za \(a\propto t^{2/3}\) i \(QK_Q=3f_AH^2\), gdje je \(f_A>0\) *ilustrativni*, neopaženi udio aeterskog fluida, slijedi
\[
\boxed{\chi\propto a^{\mu_\pm},\quad
\mu_\pm=\frac{1\pm\sqrt{1+48f_A/K_B}}4.}
\]
Pritom je plus grana matematički rastuća. Ovo je **uvjetna aproksimacija**, ne slobodno dopušten fizički isocurvature mod.

**Tri ključne granice zaključka:**

- \(\Delta_A\) je u fizičkoj kozmologiji **dinamička**, i preko metrike zadovoljava Einsteinova ograničenja; ne smijemo je proizvoljno proglasiti vanjskom nulom. Takva ograničenja mogu eliminirati ili promijeniti promatrani lokalni mod.
- Pozitivan korijen lokalne matrice pri zamrznutim koeficijentima nije dokaz pozitivnog Lyapunovljeva eksponenta za vremenski ovisnu evoluciju tijekom radijacijsko-materijskog prijelaza; lokalna skala rasta ne daje opažajno pojačanje.
- U stvarnom Exp benchmarku je \(K_B=0.1\) i \(c_a^2\sim10^{-14}\), ali **uvjet (7) nije numerički evaluiran kroz stvarnu pozadinu**, niti su sve vrste materije uključene u karakteristični sustav. Stare nazubljene prijenosne funkcije \(W,d_b,d_m\) nisu dokazana posljedica ovog moda.

## 4. Znanstvena odluka i točno jedan preostali fizički uvjet

**Rezultat:** pasivna NL0B kupelj **ne jamči** stabilnost pridruženog skalarnog aetera. Imamo čvrsto definiran **uvjetni kanal pojačanja** koji može objasniti zašto početni faktor \(c_a^2\ll1\) sam nije dovoljan za procjenu detektabilnosti. Nije dokazano da fizički kozmološki mod taj kanal doista može pobuditi.

**Sljedeće isključivo fizikalno pitanje**: dopušta li **puni Einstein–AeST–NL0B** početno-vrijednosni sustav, uz istu akciju, gauge, scalar-charge i Hamiltonian/momentum/shear/trace ograničenja te dinamički \(\Delta_A,\Phi,\Psi\), takav rastući mod? Ako ne dopušta — odbaciti ga kao artefakt reduciranog podsustava. Ako dopušta — tek tada kvalificirati vremenski ovisno pojačanje i eventualni fizički Weylov odziv. **Bez novih otvorenih CLASS sweepova i bez DES fitanja do te odluke.**

**Status:** `REDUCED_FROZEN_POSITIVE_REAL_ROOT_CONDITIONAL_PASS / FULL_COSMOLOGICAL_STABILITY_AND_DETECTABILITY_BLOCK`.

## 5. Reproducibilnost

- [Jedna izvršiva analiza 17 točnih identiteta](../ge19/physics_gate/coupled_frozen_gain_20261112.py). U lokalnom analitičkom izvođenju **17/17** algebarskih provjera PASS; ovaj izvorni GitHub script još nije izvršen source-locked na WSL-u.
- [Samostalni JSON iz 17 provjera](../results/ge19_coupled_frozen_gain_20261112_standalone.json), `source_locks_executed=false`.
- [Izvorni WSL 14/14](../results/ge19_first_retarded_memory_onset_20261111_wsl.json), [izvorni WSL 9/9](../results/ge19_radiation_neutrino_delta_source_20261111_wsl.json), [energetski dokaz pasivne kupelji](ge19_20261112_retarded_bath_energy_amplification_gate.md).

Samo za potvrdu ove algebre u kanonskom WSL checkoutu, **ne pokreće CLASS**:

~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
set -o pipefail
python3 -u ge19/physics_gate/coupled_frozen_gain_20261112.py \
  --out results/ge19_coupled_frozen_gain_20261112_wsl.json \
  2>&1 | tee results/ge19_coupled_frozen_gain_20261112_wsl.log
echo "EXIT=$?"
~~~

Očekivano: `GE19_GAIN_SOURCE_LOCKS_PASS 4`, `GE19_REDUCED_FROZEN_GAIN_IDENTITIES_PASS 17`, `GE19_FULL_PHYSICS_GO False`. Nijedan stari fizički izvor ili rezultat nije mijenjan.
