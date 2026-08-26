# WS₂ Monolayer — Komputasi First-Principles Sifat Elektronik, Optik, dan Termoelektrik

Repositori ini memuat seluruh alur kerja komputasi, skrip pascapengolahan data, dan draf
laporan akhir untuk investigasi material dua dimensi (2D) **Tungsten Disulfida (WS₂)
Monolayer**, menggunakan pendekatan *Density Functional Theory* (DFT) pada perangkat
lunak **Quantum ESPRESSO**, serta perhitungan transport semiklasik menggunakan
**BoltzTraP2**.

## 📑 Sumber Referensi & Atribusi (BRIN-Q)

Sebagian besar *pipeline* dasar komputasi pada proyek ini diadaptasi dari repositori
*tacit-knowledge* milik Pusat Riset Fisika Kuantum BRIN (**BRIN-Q**):

1. [Tutorial Termoelektrik Dasar](https://github.com/BRIN-Q/tacit-knowledge/blob/main/Tutorials/tutorial-termoelektrik.md)
2. [Panduan Instalasi & Eksekusi BoltzTraP2](https://github.com/BRIN-Q/tacit-knowledge/blob/main/Tutorials/boltztrap2-thermoelectric.md)

## 🗂️ Struktur Repositori

```
ws2-mono/
├── bands/          # Input dan output (scf, nscf, bands) untuk plot pita energi
├── btp/             # Input (nscf.in) dan output transport BoltzTraP2 (ws2.condtens)
├── dos/              # Input dan output (scf, nscf, dos) untuk plot DOS
├── optic/            # Input dan output (scf, epsilon) untuk sifat optik
├── figures/          # Hasil plot grafik final (PNG dan PDF)
├── matplotlib/        # Style sheet plot (sci.mplstyle) untuk standarisasi grafik
├── scripts/           # Skrip Python (plot_band_dos.py, plot_optic.py, dll.)
└── laporan_magang/     # Source code LaTeX beserta gambar dari laporan akhir
```

## 📌 Alur Kerja Komputasi

1. **Struktur:** Optimasi geometri (*vc-relax*) monolayer dengan ruang vakum transversal
   20.0 Å.
2. **Elektronik (`bands/`, `dos/`):** Perhitungan struktur pita energi dan *Density of
   States* untuk mengonfirmasi karakter *direct gap* di titik K.
3. **Optik (`optic/`):** Ekstraksi fungsi dielektrik kompleks dan koefisien absorpsi
   optik menggunakan modul `epsilon.x` (pendekatan *independent-particle*).
4. **Termoelektrik (`btp/`):** Evaluasi koefisien Seebeck, konduktivitas listrik, dan
   *power factor* menggunakan BoltzTraP2 (CRTA).
5. **Analisis (`scripts/`, `figures/`):** Uji konvergensi, validasi silang
   pseudopotensial GBRV vs ONCV, dan visualisasi hasil termasuk fenomena *band gap
   divergence* pada suhu rendah.

## ⚙️ Perangkat Lunak

| Perangkat Lunak | Kegunaan |
|---|---|
| [Quantum ESPRESSO](https://www.quantum-espresso.org/) | DFT: vc-relax, scf, nscf, bands, dos, epsilon.x |
| [BoltzTraP2](https://gitlab.com/sousaw/BoltzTraP2) | Transport semiklasik (Seebeck, konduktivitas, power factor) |
| Python 3 (NumPy, Matplotlib, Pandas) | Pascapengolahan data & visualisasi |

## 👥 Tim

Kelompok Jumadil & Zairil — Magang UNP 2026.

## 📄 Lisensi

Lihat berkas [LICENSE](LICENSE).
