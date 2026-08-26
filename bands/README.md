# bands/

Input dan output Quantum ESPRESSO untuk perhitungan struktur pita energi (band structure):

- `scf.in` / `scf.out` — perhitungan self-consistent field, hasil kerapatan elektron dasar
- `nscf.in` / `nscf.out` — non-self-consistent field pada grid k-point padat (opsional, jika diperlukan sebelum bands)
- `bands.in` / `bands.out` — perhitungan pita energi sepanjang lintasan titik simetri
  tinggi Brillouin zone heksagonal (Γ–M–K–Γ)
- `bands.dat` / `bands.dat.gnu` — keluaran `bands.x` yang siap diplot

Digunakan untuk mengonfirmasi karakter *direct band gap* WS₂ monolayer di titik K.
