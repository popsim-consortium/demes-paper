"""

Requires msprime~1.1, moments, demesdraw
"""
import msprime
import moments
import demes
import demesdraw
import numpy as np

import matplotlib.pylab as plt
import matplotlib.image as mpimg

# set font sizes
import matplotlib

plt.rcParams["legend.title_fontsize"] = "xx-small"
matplotlib.rc("xtick", labelsize=6)
matplotlib.rc("ytick", labelsize=6)
matplotlib.rc("axes", labelsize=7)
matplotlib.rc("axes", titlesize=7)
matplotlib.rc("legend", fontsize=6)


def plot_model(ax, graph):
    demesdraw.tubes(
        graph,
        ax=ax,
        num_lines_per_migration=2,
        log_time=True,
        positions={"ancestral": 0, "AFR": -300000, "EUR": 300000},
        seed=11111,
    )
    ax.set_ylim(top=1e6)


def plot_sfs(ax, fs_moments, fs_msprime, ylabel=True):
    ax.plot(fs_moments, "o", lw=0.5, ms=3, fillstyle="none", label="moments")
    ax.plot(fs_msprime, ".--", ms=2, lw=0.5, label="msprime")
    ax.set_xlabel("Derived allele count")
    if ylabel:
        ax.set_ylabel("Number observed")
    ax.set_yscale("log")
    ax.legend()
    ax.set_xticks(np.arange(0, fs_moments.sample_sizes[0] + 1, 5))


if __name__ == "__main__":
    # load the graph
    graph = demes.load("../models/tennessen.yaml")

    # set up the figure
    fig = plt.figure(54321, figsize=(6.5, 3.0))
    fig.clf()
    grid = (5, 10)

    # draw the graph using demesdraw
    ax1 = plt.subplot2grid(grid, (0, 0), colspan=4, rowspan=5)
    plot_model(ax1, graph)

    # simulate data using msprime
    demog = msprime.Demography.from_demes(graph)
    L = 1e7
    r = 2e-8
    #
    samples = {"AFR": 20, "EUR": 20}
    msprime_samples = [
        msprime.SampleSet(n, ploidy=1, population=p) for p, n in samples.items()
    ]

    seed = 1234567
    ts = msprime.sim_ancestry(
        msprime_samples,
        # {p: s // 2 for p, s in samples.items()},
        demography=demog,
        sequence_length=L,
        recombination_rate=r,
        random_seed=seed,
    )

    u = 2.36e-8
    ts = msprime.sim_mutations(ts, rate=u, random_seed=seed)

    msprime_afr = ts.allele_frequency_spectrum(
        [range(samples["AFR"])], mode="site", polarised=True, span_normalise=False
    )
    msprime_eur = ts.allele_frequency_spectrum(
        [range(samples["AFR"], sum(samples.values()))],
        mode="site",
        polarised=True,
        span_normalise=False,
    )
    msprime_afr = moments.Spectrum(msprime_afr)
    msprime_eur = moments.Spectrum(msprime_eur)

    # compute expected SFS for sampled populations using moments
    Ne = graph["ancestral"].epochs[0].start_size
    theta = 4 * Ne * u * L

    fs = moments.Spectrum.from_demes(graph, samples=samples)
    fs *= theta

    moments_afr = fs.marginalize([1])
    moments_eur = fs.marginalize([0])

    # plot AFR SFS comparison
    ax2 = plt.subplot2grid(grid, (0, 4), colspan=3, rowspan=2)
    plot_sfs(ax2, moments_afr, msprime_afr)
    ax2.set_title("AFR frequency spectrum")

    # plot EUR SFS comparison
    ax3 = plt.subplot2grid(grid, (0, 7), colspan=3, rowspan=2)
    plot_sfs(ax3, moments_eur, msprime_eur, ylabel=False)
    ax3.set_title("EUR frequency spectrum")
    ax3.sharey(ax2)

    ax4 = plt.subplot2grid(grid, (2, 4), colspan=6, rowspan=3)
    img = mpimg.imread("minted-snippet.png")
    yy, xx, _ = img.shape
    ax4.set_xlim(0, xx)
    ax4.set_ylim(yy, 0)
    ax4.imshow(img, interpolation="none")
    ax4.set_frame_on(False)
    ax4.set_xticks([])
    ax4.set_yticks([])

    fig.tight_layout()
    fig.subplots_adjust(wspace=1.0)

    fig.text(0.01, 0.95, "A", fontsize=8)
    fig.text(0.40, 0.95, "B", fontsize=8)
    fig.text(0.71, 0.95, "C", fontsize=8)
    fig.text(0.43, 0.45, "D", fontsize=8)

    plt.savefig("showcase.pdf")
