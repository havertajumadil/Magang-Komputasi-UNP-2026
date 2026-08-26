# btp/

Input dan output untuk perhitungan transport termoelektrik menggunakan BoltzTraP2:

- `nscf.in` / `nscf.out` — perhitungan QE non-self-consistent pada grid k-point sangat
  padat, dasar bagi interpolasi BoltzTraP2
- `ws2.intrans`, `ws2.struct`, `ws2.energy` — berkas input BoltzTraP2 (format
  antarmuka BoltzTraP klasik) atau hasil ekspor via antarmuka BoltzTraP2-QE
- `ws2.condtens` — keluaran utama BoltzTraP2: koefisien Seebeck, konduktivitas listrik,
  dan power factor sebagai fungsi suhu dan potensial kimia

Alur mengikuti tutorial BRIN-Q:
https://github.com/BRIN-Q/tacit-knowledge/blob/main/Tutorials/boltztrap2-thermoelectric.md
