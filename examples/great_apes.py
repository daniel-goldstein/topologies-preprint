import sys
import msprime
from tqdm import tqdm
import time
import math

from util import area_plot, plot_speed


def great_apes(sample_size):
    spec = msprime.parse_species_tree(
        "(((human:5.6,chimp:5.6):3.0,gorilla:8.6):9.4,orangutan:18.0)",
        Ne=20000,
        branch_length_units="myr",
        generation_time=28,
    )

    species_ts = msprime.simulate(
        length=1e6,
        samples=spec.sample(
            human=sample_size,
            chimp=sample_size,
            gorilla=sample_size,
            orangutan=sample_size,
        ),
        recombination_rate=1e-8,
        random_seed=1,
        demography=spec,
    )

    print(
        species_ts.num_samples / 1e3,
        "thousand genomes, ",
        round(species_ts.num_trees / 1e3),
        "thousand trees",
    )

    return species_ts


def run(sample_size):
    ts = great_apes(sample_size)
    species_topologies = []
    rates = []
    iters_per_sec = 0
    start = time.time()
    stop = start
    for top in tqdm(ts.count_topologies(), total=ts.num_trees):
        stop = time.time()
        iters_per_sec += 1
        interval = stop - start
        if interval >= 1:
            for _ in range(math.floor(interval)):
                rates.append(iters_per_sec / math.floor(interval))
            iters_per_sec = 0
            start = time.time()

        species_topologies.append(top[0, 1, 2, 3])

    area_plot(
        species_topologies,
        ts.breakpoints(as_array=True)[:-1],
        {0: "human", 1: "chimp", 2: "gorilla", 3: "orangutan"},
        "great_apes_area_plot",
    )
    plot_speed(rates, "trees_per_sec")


if __name__ == "__main__":
    run(int(sys.argv[1]))
