import os
import collections
import matplotlib.pyplot as plt
# import seaborn as sns

import tskit


def plot_speed(times, outfile):
    plt.plot(range(len(times)), times)
    plt.savefig(f"plots/{outfile}.png")
    plt.close()


def area_plot(counters, breakpoints, leaf_labels, outfile):
    percents = []
    for c in counters:
        total = sum(c.values())
        percents.append(collections.Counter({k: (v / total) * 100 for k, v in c.items()}))
    ranks = list(sorted(set().union(*(c.keys() for c in percents))))
    data = [[c[rank] for c in percents] for rank in ranks]

    pal = ["#9b59b6", "#e74c3c", "#1e90ff", "#2ecc71"]
    # pal = sns.color_palette("Set1")
    plt.stackplot(breakpoints, data, labels=ranks, colors=pal, alpha=0.4)

    if not os.path.exists("plots"):
        os.mkdir("plots")

    plt.savefig(f"plots/{outfile}.png")
    plt.close()

    # Save svgs of the topologies with the corresponding color to the plot
    windows = zip(breakpoints, breakpoints[1:])
    total = collections.Counter()
    for c, (left, right) in zip(counters, windows):
        for rank, count in c.items():
            total[rank] += count * (right - left)

    percents = collections.Counter()
    total_count = sum(total.values())
    for rank, count in total.items():
        percents[rank] = (count / total_count) * 100

    for i, rank in enumerate(ranks):
        print("Topology", rank, "seen", total[rank], "times.", f"({percents[rank]:.2f}% weighted)")
        t = tskit.Tree.unrank(rank, len(leaf_labels))
        t.draw_svg(
            path=f"plots/tree_{i}.svg",
            node_labels=leaf_labels,
            style=f".tree .node .edge {{ stroke: {pal[i]} }}",
            size=(350, 250),
            order="tree")
