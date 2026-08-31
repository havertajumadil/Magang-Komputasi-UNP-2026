#!/usr/bin/env python3

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('../matplotlib/sci.mplstyle')

CONDTENS_FILE = Path("../btp/ws2.condtens")

FERMI_ENERGY_EV = 0.3528

TEMPERATURES_K = [300.0, 500.0, 700.0, 900.0]
LINESTYLES = [":", "--", "-.", "-"]
MU_WINDOW_EV = (-1.5, 1.5)

TAU_SECONDS = None

APPLY_2D_RESCALE = False
LZ_ANGSTROM = 20.0
D_EFFECTIVE_ANGSTROM = 3.153

OUTPUT_PNG = Path("../figures/ws2_thermoelectric_vs_mu.png")
OUTPUT_PDF = Path("../figures/ws2_thermoelectric_vs_mu.pdf")

RY_TO_EV = 13.605693122994


def read_condtens(filename):
    data = np.loadtxt(filename, comments="#")
    if data.ndim == 1:
        data = data.reshape(1, -1)
    if data.shape[1] < 30:
        raise RuntimeError(f"{filename} hanya memiliki {data.shape[1]} kolom.")
    return data


def in_plane_average(data, col_xx, col_yy):
    return 0.5 * (data[:, col_xx] + data[:, col_yy])


def best_scale(values):
    peak = np.nanmax(np.abs(values))
    if peak == 0 or not np.isfinite(peak):
        return 0
    return int(np.floor(np.log10(peak)))


def main():
    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)

    data = read_condtens(CONDTENS_FILE)

    mu_abs_ev = data[:, 0] * RY_TO_EV
    mu_rel_ev = mu_abs_ev - FERMI_ENERGY_EV
    temperature = data[:, 1]

    sigma_over_tau = in_plane_average(data, 3, 7)
    seebeck_v_per_k = in_plane_average(data, 12, 16)
    kappa_over_tau = in_plane_average(data, 21, 25)

    if APPLY_2D_RESCALE:
        factor = LZ_ANGSTROM / D_EFFECTIVE_ANGSTROM
        sigma_over_tau = sigma_over_tau * factor
        kappa_over_tau = kappa_over_tau * factor
        print(f"2D rescale diterapkan, faktor = {factor:.4f}")

    pf_over_tau = seebeck_v_per_k**2 * sigma_over_tau
    seebeck_uv_per_k = seebeck_v_per_k * 1.0e6

    if TAU_SECONDS is None:
        sigma_plot, kappa_plot, pf_plot = sigma_over_tau, kappa_over_tau, pf_over_tau
        sigma_unit = r"(\Omega\,m\,s)^{-1}"
        kappa_unit = r"W\,m^{-1}\,K^{-1}\,s^{-1}"
        pf_unit = r"W\,m^{-1}\,K^{-2}\,s^{-1}"
    else:
        sigma_plot = sigma_over_tau * TAU_SECONDS
        kappa_plot = kappa_over_tau * TAU_SECONDS
        pf_plot = pf_over_tau * TAU_SECONDS
        sigma_unit = r"S\,m^{-1}"
        kappa_unit = r"W\,m^{-1}\,K^{-1}"
        pf_unit = r"W\,m^{-1}\,K^{-2}"

    window_mask = (mu_rel_ev >= MU_WINDOW_EV[0]) & (mu_rel_ev <= MU_WINDOW_EV[1])

    exp_sigma = best_scale(sigma_plot[window_mask])
    exp_kappa = best_scale(kappa_plot[window_mask])
    exp_pf = best_scale(pf_plot[window_mask])

    sigma_scaled = sigma_plot / 10.0**exp_sigma
    kappa_scaled = kappa_plot / 10.0**exp_kappa
    pf_scaled = pf_plot / 10.0**exp_pf

    fig, axes = plt.subplots(
        2, 2, figsize=(9.5, 6.5), sharex=True, constrained_layout=True
    )
    fig.set_constrained_layout_pads(w_pad=0.05, h_pad=0.05, hspace=0.03, wspace=0.03)

    ax_s, ax_sigma, ax_kappa, ax_pf = axes.ravel()

    lines_for_legend = []
    labels_for_legend = []

    for i, target_T in enumerate(TEMPERATURES_K):
        mask = np.isclose(temperature, target_T, rtol=0.0, atol=1.0e-8)
        if not np.any(mask):
            print(f"T = {target_T:g} K tidak ditemukan.")
            continue

        x = mu_rel_ev[mask]
        s = seebeck_uv_per_k[mask] / 1000.0
        sig = sigma_scaled[mask]
        kap = kappa_scaled[mask]
        pf = pf_scaled[mask]

        order = np.argsort(x)
        x, s, sig, kap, pf = x[order], s[order], sig[order], kap[order], pf[order]

        w = (x >= MU_WINDOW_EV[0]) & (x <= MU_WINDOW_EV[1])
        x, s, sig, kap, pf = x[w], s[w], sig[w], kap[w], pf[w]

        ls = LINESTYLES[i % len(LINESTYLES)]
        label = f"{target_T:g} K"

        (line,) = ax_s.plot(x, s, linestyle=ls, linewidth=1.4)
        ax_sigma.plot(x, sig, linestyle=ls, linewidth=1.4)
        ax_kappa.plot(x, kap, linestyle=ls, linewidth=1.4)
        ax_pf.plot(x, pf, linestyle=ls, linewidth=1.4)

        lines_for_legend.append(line)
        labels_for_legend.append(label)

    for ax in axes.ravel():
        ax.axvline(0.0, linewidth=0.7, color="gray", zorder=0)
        ax.axhline(0.0, linewidth=0.7, color="gray", zorder=0)
        ax.set_xlim(*MU_WINDOW_EV)
        ax.tick_params(labelsize=9)

    ax_s.set_ylabel(r"$S_{\parallel}$ (mV/K)", fontsize=10)
    ax_s.set_title("(a) Koefisien Seebeck", loc="left", fontsize=10)

    ax_sigma.set_ylabel(
        rf"$\sigma_{{\parallel}}/\tau$ ($10^{{{exp_sigma}}}\,{sigma_unit}$)", fontsize=10
    )
    ax_sigma.set_title("(b) Konduktivitas listrik", loc="left", fontsize=10)

    ax_kappa.set_ylabel(
        rf"$\kappa_{{e,\parallel}}/\tau$ ($10^{{{exp_kappa}}}\,{kappa_unit}$)", fontsize=10
    )
    ax_kappa.set_title("(c) Konduktivitas termal elektronik", loc="left", fontsize=10)
    ax_kappa.set_xlabel(r"$\mu-E_F$ (eV)", fontsize=10)

    ax_pf.set_ylabel(
        rf"$PF_{{\parallel}}/\tau$ ($10^{{{exp_pf}}}\,{pf_unit}$)", fontsize=10
    )
    ax_pf.set_title("(d) Power factor", loc="left", fontsize=10)
    ax_pf.set_xlabel(r"$\mu-E_F$ (eV)", fontsize=10)

    fig.legend(
        lines_for_legend,
        labels_for_legend,
        loc="outside upper center",
        ncol=len(labels_for_legend),
        frameon=False,
        fontsize=10,
    )

    fig.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
    fig.savefig(OUTPUT_PDF, bbox_inches="tight")

    print(f"Skala sigma: 10^{exp_sigma}, kappa: 10^{exp_kappa}, PF: 10^{exp_pf}")
    print(f"Tersimpan: {OUTPUT_PNG}")
    print(f"Tersimpan: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()