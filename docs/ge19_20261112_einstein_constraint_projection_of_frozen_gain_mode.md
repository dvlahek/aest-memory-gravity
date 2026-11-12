# GE19 — Einsteinova ograničenja protiv umjetno neovisnog rastućeg moda

**12. studenoga 2026. | Fizika, bez nove CLASS numerike.**  
**Status:** `WSL_17_OF_17_SOURCE_LOCKED_PASS / REDUCED_FROZEN_ROOT_CONDITIONALLY_VALID / AEST_ONLY_DELTA_ZERO_GROWING_MODE_EXCLUDED_BY_CONSTRAINTS / FULL_MULTISPECIES_GAIN_OPEN`.

Ovo je **nova provjera fizičke dopuštenosti** ranije potvrđenog rastućeg korijena. Koristi već izvedena Hamiltonovo, impulsno i beztragno Einsteinovo ograničenje GE19/LW30/LW31; ne pretpostavlja novu modifikaciju akcije, ne podešava \(\eta\) i ne pokreće CLASS.

## 1. Točno potvrđeni izvorni WSL dokazi

Originalni korisnički WSL izlazi, arhivirani u repozitoriju i potvrđeni Git blobovima istovjetnim dostavljenim bajtovima:
- [`ge19_coupled_frozen_gain_20261112_wsl.json`](../results/ge19_coupled_frozen_gain_20261112_wsl.json) — 17/17 PASS, originalna 4/4 zaključana izvora, SHA-256 `b32487f1180ed2daad0995e86a3f3d2adeff33de403a72137e2b8a8c3dc88dbd`, blob `dc2b23c11f0bb0039a1dc98846305f6d2f0ee4c2`.
- [`ge19_coupled_frozen_gain_20261112_wsl.log`](../results/ge19_coupled_frozen_gain_20261112_wsl.log) — `GE19_GAIN_SOURCE_LOCKS_PASS 4`, `GE19_REDUCED_FROZEN_GAIN_IDENTITIES_PASS 17`, `GE19_FULL_PHYSICS_GO False`; SHA-256 `bc2ab9700a617690a483f40a84ae6198c0b5de997f0283af32dbfef5538fb6cd`, blob `2314f5ce1ed9456d5fe39334939c0129e45f3027`.
- [Samostalni 17/17](../results/ge19_coupled_frozen_gain_20261112_standalone.json), Git blob `011a482bea1732bda49a812efe9bc13bf79c9095`: isti algebarski sadržaj; osim provenance polja, postoji **beznačajna tekstna razlika** `3H` naspram `3*H` u jednom ljudski čitljivom opisu, bez razlike među 17 simboličkih identiteta.
- Ranije poslani `first_retarded_memory_onset` 14/14 i `radiation_neutrino_delta_source` 9/9, ponovno priloženi pod imenima `(1)`, identični su već zamrznutim WSL dokazima i nisu drugi fizički eksperiment.

## 2. Presudna identiteta komovne gustoće iz Einsteinovih ograničenja

U originalnim fizikalnim konvencijama GE19 LW30 za *AeST-only*:
\[
\mathcal C_H=\frac{k^2}{a^2}\Phi+3H(\dot\Phi+H\Psi)+\frac32D_A=0,\qquad
\mathcal C_M=\dot\Phi+H\Psi-\frac{3a}{2k^2}T_A=0,
\]
gdje \(D_A=\delta\rho_A\), \(T_A=(\rho_A+p_A)\theta_A\), \(R_A=\rho_A+p_A\) i
\[
\Delta_A=\frac{D_A}{R_A}+\frac{3aH}{k^2}\theta_A
=\frac{D_A+3aH T_A/k^2}{R_A}.
\]
Eliminiranjem \(\dot\Phi+H\Psi\) dobivamo **točno**:
\[
\boxed{R_A\Delta_A=-\frac{2k^2}{3a^2}\Phi.}\tag{C1}
\]

Za *puni* standardni višekomponentni FLRW sa zasebno minimalno vezanim vrstama materije, pod već dokumentiranom pretpostavkom da se njihovi stresovi zbrajaju u istim normalizacijama, analogno slijedi
\[
\boxed{R_A\Delta_A+\sum_{s\ne A}R_s\Delta_s
=-\frac{2k^2}{3a^2}\Phi,}\tag{C2}
\]
pri čemu je \(R_s\Delta_s=D_s+3aH T_s/k^2\). Fotonima, barionima, neutrinima i ostalim komponentama **ne dodaje se zasebni CDM slot** uz AeST kad je taj slot prenamijenjen za AeST.

(C2) je fizički **operator ograničenja**: u punom modelu \(\Delta_A\) nije slobodno zadana nezavisna vanjska funkcija, nego je povezana s \(\Phi\) i perturbacijama drugih komponenti. U superhorizontskoj adijabatskoj granici ukupna komovna gustoća je \(O(k^2)\), ali pojedinačne komovne gustoće mogu imati kompenzirane međukomponentne perturbacije, pa se \(\Delta_A=0\) ne smije zaključiti samo iz \(\Delta_{\rm total}=O(k^2)\).

## 3. Poseban egzaktan AeST-only test koji eliminira hipotetski rastući korijen

**Pretpostavke koje ograničavaju ovaj zaključak:** \(k>0\) je konačan, samo AeST gravitira, \(R_A\ne0\), \(K_Q\ne0\), nema drugih vrsta materije ili dodatnog anizotropnog naprezanja, \(0<K_B<2\), \(Q>0\), \(H\ge0\), \(c_a^2\ge0\), a hipotetski homogenizirani mode **zahtijeva \(\Delta_A(t)=0\)**.

1. Iz (C1) i \(\Delta_A=0\) proizlazi \(\Phi=0\).
2. Iz AeST-only beztragno-prostorne Einsteinove jednadžbe \(\Phi-\Psi=0\) proizlazi \(\Psi=0\).
3. Iz impulsnog ograničenja proizlazi \(T_A=0\). Budući da je \(T_A=K_Qk^2\varphi/(3a)\), za \(k>0\) dobivamo \(\varphi=0\).
4. Iz \(R_A\Delta_A=D_A+3aHT_A/k^2=0\) sada je \(D_A=0\). Fiksna action density dictionary daje
   \[
   D_A=\frac13\bigg[
   QK_{QQ}(\dot\varphi-Q\Psi)
   -\frac{k^2}{a^2}\big(K_BE_A+C\chi\big)\bigg]=0,
   \]
   pa \(K_BE_A+C\chi=0\), \(C=2-K_B>0\).
5. Iz \(\chi=\varphi+Q\alpha_A=Q\alpha_A\), \(E_A=\dot\alpha_A+\Psi=\dot\alpha_A\), \(\dot Q/Q=-3Hc_a^2\), slijedi
   \[
   \boxed{\dot\chi=-\left(\frac{CQ}{K_B}+3Hc_a^2\right)\chi.}\tag{C3}
   \]
   Ako je \(0<K_B<2,Q>0,H\ge0,c_a^2\ge0\), koeficijent je strogo negativan. Stoga **pretpostavljeni \(\Delta_A=0\) AeST-only fizički mod ne može imati rastući \(\chi\)**; on ili opada ili je dodatnim jednadžbama potpuno eliminiran.

Ovo je **nužan zaključak samih ograničenja**, ne nova pretpostavka da aeter ima prigušenje. Nisu korišteni nikakvi rezultati DES podataka. Ne tvrdi se da je \(\chi\ne0\) koji bi formalno zadovoljavao (C3) automatski rješenje svih AeST Eulerovih jednadžbi i kupelji.

**Razlika prema prethodnom lokalnom teoremu:** tamo se za račun karakterističnog polinoma u \((\chi,E,q_j,p_j)\) postavilo \(\Delta_A=0\) **bez** istodobnog nametanja (C1), AeST \(D_A\) action dictionary i Einsteinove shear jednadžbe. Dobiveni pozitivni \(\lambda\) je valjano svojstvo *tako izdvojenog* ODE sustava, ali se u prethodno definiranom AeST-only testu **ne može smatrati fizički dopuštenim rastućim rješenjem**.

## 4. Što time još NIJE riješeno

Stvarni zamrznuti CLASS benchmark uključuje radijaciju, barione, neutrinsku anizotropiju i AeST kao efektivnu tamnu komponentu. Tamo je \(\Phi-\Psi\) pogonjen neutrinskim stresom, a (C2) određuje tek **zbroj** komovnih gustoća; dopušteni kompenzirani modovi ostaju otvoreni.

Zato (C3) **ne** dokazuje stabilnost punog Einstein–AeST–NL0B sustava, ne isključuje sve rastuće modove s \(\Delta_A\ne0\), ne ograničava vremenski neautonomni gain do \(z=0.5\) i ne certificira \(\partial_\eta P_{gW}\). Nije dokazano ni da je prethodno opažena mala, nazubljena razlika iz CLASS-a izravni posljedak nekog od ovih modova.

**Fizikalna odluka:** ne smije se podizati alarm zbog fizičke gravitacijske nestabilnosti samo na osnovi 17/17 frozen eigen-polynomial PASS-a. Jedna preostala ciljna provjera je zajednički **constraint-projected** linearni operator s \(\Delta_A,\Phi,\Psi\) i svim standardnim vrstama materije te originalnim scalar-charge/no-free-bath uvjetima; zatim samo ako prođe konačno-vremenski odziv. Nema opravdanja za nove CLASS \(\eta\)-sweepove ili DES fit dok ovo nije riješeno.

**Status:** `FROZEN_REDUCED_ROOT_PASS / AEST_ONLY_EXCLUDED_FOR_DELTA_ZERO / FULL_MULTISPECIES_PHYSICS_GO_BLOCK`.

## 5. Izvorni izvodi

- [LW30 — izvorna ADM Hamiltonova i impulsna ograničenja](ge19_lw30_original_gr_aest_adm_scalar_constraints_class_bridge_2026-11-10.md).
- [LW31 — beztragna Einsteinova jednadžba u AeST-only sektoru](ge19_lw31_original_action_spatial_traceless_Einstein_shear_2026-11-10.md).
- [All-species original CLASS izvorna ograničenja](ge19_20261111_all_species_Einstein_operator_and_adiabatic_IC_block.md).
- [Uvjetni zamrznuti rastući korijen](ge19_20261112_frozen_coupled_scalar_bath_gain_conditional_root.md).
- [Originalni 15/15 action-to-fluid map](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md).
