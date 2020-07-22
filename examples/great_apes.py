import sys
import msprime
from tqdm import tqdm
import time

from util import area_plot, plot_speed


def great_apes(sample_size):
    spec = msprime.parse_species_tree(
        "(((human:5.6,chimp:5.6):3.0,gorilla:8.6):9.4,orangutan:18.0)",
        Ne=20000,
        branch_length_units="myr",
        generation_time=28)

    species_ts = msprime.simulate(
        length=1e6,
        samples=spec.sample(human=sample_size, chimp=sample_size, gorilla=sample_size, orangutan=sample_size),
        recombination_rate=1e-8,
        demography=spec)

    print(
        species_ts.num_samples / 1e3, "thousand genomes, ",
        round(species_ts.num_trees / 1e3), "thousand trees")

    return species_ts


def run(sample_size):
    ts = great_apes(sample_size)
    species_topologies = []
    times = []
    start = time.time()
    for top in tqdm(ts.count_topologies(), total=ts.num_trees):
        stop = time.time()
        times.append(stop - start)
        species_topologies.append(top[0, 1, 2, 3])
        start = time.time()

    area_plot(species_topologies,
              ts.breakpoints(as_array=True)[:-1],
              {0: "human", 1: "chimp", 2: "gorilla", 3: "orangutan"},
              "great_apes_area_plot")
    plot_speed(times, "incremental_times")


if __name__ == '__main__':
    run(int(sys.argv[1]))
