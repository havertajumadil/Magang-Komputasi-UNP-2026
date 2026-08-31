#!/usr/bin/env python3

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('../matplotlib/sci.mplstyle')

EPSR_FILE = Path("../optic/epsr_ws2.dat")
EPSI_FILE = Path("../optic/epsi_ws2.dat")

# Koreksi normalisasi 2D -- lihat catatan sebelum mengaktifkan
APPLY_2D_RESCALE = False
LZ_ANGSTROM = 20.0
D_EFFECTIVE_ANGSTROM = 6.15  # konvensi sama seperti BoltzTraP2 nanti; ganti kalau ada dasar lain

ENERGY_WINDOW_EV = (0.0, 6.0)

OUT_EPS_PNG = Path("../figures/ws2_eps_real_imag.png")
OUT_EPS_PDF = Path("../figures/ws2_eps_real_imag.pdf")
OUT_ALPHA_PNG = Path("../figures/ws2_absorption.png")
OUT_ALPHA_PDF = Path("../figures/ws2_absorption.pdf")


def load_4col(path):
    data = np.loadtxt(path, comments="#")
    energy = data[:, 0]
    x, y, z = data[:, 1], data[:, 2], data[:, 3]
    in_plane = 0.5 * (x + y)
    return energy, in_plane, z


def absorption_coefficient(energy_ev, eps1, eps2):
    hbar_c_eVA = 1973.269804  # eV * Angstrom
    w_over_c = energy_ev / hbar_c_eVA  # 1/Angstrom
    modulus = np.sqrt(eps1**2 + eps2**2)
    inner = np.clip(modulus - eps1, 0, None)
    alpha = np.sqrt(2.0) * w_over_c * np.sqrt(inner)  # 1/Angstrom
    return alpha * 1.0e8  # -> 1/cm


OUT_EPS_PNG.parent.mkdir(parents=True, exist_ok=True)

E_r, eps1_ip, _ = load_4col(EPSR_FILE)
E_i, eps2_ip, _ = load_4col(EPSI_FILE)

if APPLY_2D_RESCALE:
    factor = LZ_ANGSTROM / D_EFFECTIVE_ANGSTROM
    eps2_ip_plot = eps2_ip * factor
    print(f"2D rescale diterapkan, faktor = {factor:.4f}")
else:
    eps2_ip_plot = eps2_ip

alpha_ip = absorption_coefficient(E_r, eps1_ip, eps2_ip_plot)

# --- Figure 1: Re(eps) dan Im(eps), dual-axis, tanpa legend ---
fig1, ax_re = plt.subplots(figsize=(5.5, 4.5))
ax_im = ax_re.twinx()

ax_re.plot(E_r, eps1_ip, color="blue", linewidth=1.8)
ax_im.plot(E_i, eps2_ip_plot, color="red", linestyle="--", linewidth=1.8)

ax_re.set_xlabel("Energi foton (eV)")
ax_re.set_ylabel(r"Re($\epsilon_{\parallel}$)", color="blue")
ax_im.set_ylabel(r"Im($\epsilon_{\parallel}$)", color="red")
ax_re.tick_params(axis="y", labelcolor="blue")
ax_im.tick_params(axis="y", labelcolor="red")
ax_re.set_xlim(*ENERGY_WINDOW_EV)

fig1.tight_layout()
fig1.savefig(OUT_EPS_PNG, dpi=300, bbox_inches="tight")
fig1.savefig(OUT_EPS_PDF, bbox_inches="tight")

# --- Figure 2: koefisien absorpsi, single panel, tanpa legend ---
fig2, ax_alpha = plt.subplots(figsize=(5.5, 4.5))
ax_alpha.plot(E_r, alpha_ip, color="black", linewidth=1.8)
ax_alpha.set_xlabel("Energi foton (eV)")
ax_alpha.set_ylabel(r"$\alpha_{\parallel}(\omega)$ (cm$^{-1}$)")
ax_alpha.set_xlim(*ENERGY_WINDOW_EV)

fig2.tight_layout()
fig2.savefig(OUT_ALPHA_PNG, dpi=300, bbox_inches="tight")
fig2.savefig(OUT_ALPHA_PDF, bbox_inches="tight")

print(f"Tersimpan: {OUT_EPS_PNG}")
print(f"Tersimpan: {OUT_EPS_PDF}")
print(f"Tersimpan: {OUT_ALPHA_PNG}")
print(f"Tersimpan: {OUT_ALPHA_PDF}")