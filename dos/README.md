# dos/

Input dan output Quantum ESPRESSO untuk perhitungan Density of States (DOS):

- `scf.in` / `scf.out` — self-consistent field
- `nscf.in` / `nscf.out` — non-self-consistent field pada grid k-point padat (diperlukan
  untuk DOS yang akurat)
- `dos.in` / `dos.out` — perhitungan total DOS (`dos.x`)
- `pdos.in` / `pdos.out` — projected DOS per orbital/atom (`projwfc.x`), opsional
- `*.dos`, `*pdos*` — berkas keluaran numerik siap diplot
