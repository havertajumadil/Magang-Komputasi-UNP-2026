#!/usr/bin/env python3

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('../matplotlib/sci.mplstyle')

BAND_FILE = Path("../bands/ws2.bands.gnu")
DOS_FILE  = Path("../dos/ws2.dos")

FERMI_ENERGY_EV = 0.40095   # titik tengah gap dari NSCF-DOS: (-0.5464 + 1.3663)/2

N_OCCUPIED_BANDS = 13      # 26 elektron valensi (W=14, S=6x2) -- konfirmasi kalau belum yakin

HIGH_SYMMETRY_INDICES = [0, 40, 80, -1]
HIGH_SYMMETRY_LABELS = [r"$\Gamma$", "M", "K", r"$\Gamma$"]

ENERGY_WINDOW_EV = (-4.0, 4.0)

OUTPUT_PNG = Path("../figures/ws2_band_dos.png")
OUTPUT_PDF = Path("../figures/ws2_band_dos.pdf")


def read_qe_gnu_bands(filename):
    blocks, current = [], []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                if current:
                    blocks.append(np.asarray(current, dtype=float))
                    current = []
                continue
            if s.startswith("#"):
                continue
            fields = s.split()
            if len(fields) >= 2:
                current.append([float(fields[0]), float(fields[1])])
    if current:
        blocks.append(np.asarray(current, dtype=float))
    if not blocks:
        raise RuntimeError(f"Tidak ada data pita dalam {filename}")
    nk = min(len(b) for b in blocks)
    kdist = blocks[0][:nk, 0]
    energies = np.vstack([b[:nk, 1] for b in blocks])
    return kdist, energies


def resolve_indices(indices, nk):
    result = []
    for i in indices:
        j = nk + i if i < 0 else i
        if not 0 <= j < nk:
            raise IndexError(f"Indeks {i} tidak valid untuk nk={nk}")
        result.append(j)
    return result


OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)

# --- baca data ---
kdist, bands_ev = read_qe_gnu_bands(BAND_FILE)
bands_shifted = bands_ev - FERMI_ENERGY_EV

hs_indices = resolve_indices(HIGH_SYMMETRY_INDICES, len(kdist))
hs_positions = [kdist[i] for i in hs_indices]
nbands = bands_ev.shape[0]

print(f"E_F(ref, titik tengah gap) = {FERMI_ENERGY_EV:.5f} eV")
print(f"Jumlah pita = {nbands}, jumlah titik-k = {len(kdist)}")

# --- cek direct gap di K ---
iv, ic = N_OCCUPIED_BANDS - 1, N_OCCUPIED_BANDS
vband, cband = bands_ev[iv], bands_ev[ic]

ivbm, icbm = int(np.argmax(vband)), int(np.argmin(cband))
vbm, cbm = vband[ivbm], cband[icbm]
gap_bandpath = cbm - vbm

k_index = hs_indices[2]  # posisi K di lintasan
direct_gap_k = cband[k_index] - vband[k_index]

print(f"VBM = {vbm:.4f} eV @ indeks k={ivbm}")
print(f"CBM = {cbm:.4f} eV @ indeks k={icbm}  (indeks K={k_index})")
print(f"Gap minimum sepanjang lintasan = {gap_bandpath:.4f} eV")
print(f"Direct gap di K = {direct_gap_k:.4f} eV")
print(f"VBM tepat di K? {ivbm == k_index} | CBM tepat di K? {icbm == k_index}")

# --- baca DOS ---
dos_data = np.loadtxt(DOS_FILE, comments="#")
if dos_data.ndim == 1:
    dos_data = dos_data.reshape(1, -1)

dos_energy = dos_data[:, 0] - FERMI_ENERGY_EV
dos_value = dos_data[:, 1]

# --- plot dua panel, gaya prosedural ---
plt.figure(figsize=(9.0, 6.0))

plt.subplot(1, 2, 1)
for band in bands_shifted:
    plt.plot(kdist, band, linewidth=1.0, color='C0')
for xpos in hs_positions:
    plt.axvline(xpos, linewidth=0.7, linestyle=":", color='gray')
plt.axhline(0.0, linewidth=0.9, linestyle="--", color='k')
plt.xlim(kdist[0], kdist[-1])
plt.ylim(*ENERGY_WINDOW_EV)
plt.xticks(hs_positions, HIGH_SYMMETRY_LABELS)
plt.ylabel(r"$E-E_F$ (eV)")
plt.xlabel("Lintasan titik-k")
plt.title("Struktur pita elektronik")

plt.subplot(1, 2, 2)
plt.plot(dos_value, dos_energy, linewidth=1.2, color='C0')
plt.axhline(0.0, linewidth=0.9, linestyle="--", color='k')
plt.ylim(*ENERGY_WINDOW_EV)
plt.xlabel("DOS (states/eV)")
plt.title("DOS")
plt.gca().tick_params(axis="y", labelleft=False)

plt.suptitle("WS$_2$ Monolayer")
plt.tight_layout()

plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
plt.savefig(OUTPUT_PDF, bbox_inches="tight")