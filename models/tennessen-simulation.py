import demes
import msprime, tskit
import moments

####
#### Import the demographic model using demes, set up samples
####

graph = demes.load("tennessen.yml")
samples = {"AFR": 20, "EUR": 20}

####
#### Simulate genomic data using msprime
####

msprime_samples = [
    msprime.SampleSet(n, ploidy=1, population=p) for p, n in samples.items()
]
demog = msprime.Demography.from_demes(graph)  # load the demes model as msprime demography
L = 1e7  # sequence length of 10 Mb
r = 2e-8  # with constant recombination rate of 2e-8
u = 2.36e-8  # mutation rate used in Tennessen et al (2012)

ts = msprime.sim_ancestry(
    msprime_samples,
    demography=demog,
    sequence_length=L,
    recombination_rate=r,
    random_seed=1234567,
)

ts = msprime.sim_mutations(ts, rate=u, random_seed=1234567)

# compute the SFS from the msprime simulation using tskit
msprime_afr = ts.allele_frequency_spectrum(
    [range(samples["AFR"])], mode="site", polarised=True, span_normalise=False
)
msprime_eur = ts.allele_frequency_spectrum(
    [range(samples["AFR"], samples["AFR"] + samples["EUR"])],
    mode="site",
    polarised=True,
    span_normalise=False,
)
####
#### Compute expected SFS for sampled populations using moments
####

Ne = graph["ancestral"].epochs[0].start_size
theta = 4 * Ne * u * L

fs = moments.Spectrum.from_demes(graph, samples=samples)
fs *= theta  # rescale to match the total mutation rate in the msprime simulation

moments_afr = fs.marginalize([1])
moments_eur = fs.marginalize([0])
