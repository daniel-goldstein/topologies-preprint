import sys
import msprime
from tqdm import tqdm
import time
import math
import tskit

from util import area_plot, plot_speed


def great_apes(sample_size, initial_size):
    spec = msprime.species_trees.parse_species_tree(
        "(((human:5.6,chimp:5.6):3.0,gorilla:8.6):9.4,orangutan:18.0)",
        initial_size=initial_size,
        branch_length_units="myr",
        generation_time=28,
    )

    species_ts: tskit.TreeSequence = msprime.sim_ancestry(
        sequence_length=1e6,
        samples={j: sample_size for j in range(4)},
        demography=spec,
        recombination_rate=1e-8,
        random_seed=1,
    )

    print(
        species_ts.num_samples / 1e3,
        "thousand genomes, ",
        round(species_ts.num_trees / 1e3),
        "thousand trees",
    )

    return species_ts


def run(sample_size, initial_size):
    ts = great_apes(sample_size, initial_size)
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
    run(int(sys.argv[1]), int(sys.argv[2]))
