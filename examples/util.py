import os
import collections
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def area_plot(counters, breakpoints, outfile):
    percents = []
    for c in counters:
        total = sum(c.values())
        percents.append(collections.Counter({k: (v / total) * 100 for k, v in c.items()}))
    ranks = set().union(*(c.keys() for c in percents))
    data = [[c[rank] for c in percents] for rank in ranks]

    # pal = ["#9b59b6", "#e74c3c", "#34495e", "#2ecc71"]
    pal = sns.color_palette("Set1")
    plt.stackplot(range(1, 100), data, labels=ranks, colors=pal, alpha=0.4 )
    plt.show()

    if not os.path.exists("plots"):
        os.mkdir("plots")

    plt.savefig(f"plots/{outfile}.png")
