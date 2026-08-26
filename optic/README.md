# optic/

Input dan output Quantum ESPRESSO untuk perhitungan sifat optik:

- `scf.in` / `scf.out` — self-consistent field
- `epsilon.in` / `epsilon.out` — perhitungan fungsi dielektrik kompleks menggunakan
  `epsilon.x` dengan pendekatan *independent-particle* (IPA)
- `epsilon_re.dat`, `epsilon_im.dat` — bagian real & imajiner fungsi dielektrik vs
  energi foton, digunakan untuk menghitung koefisien absorpsi optik
