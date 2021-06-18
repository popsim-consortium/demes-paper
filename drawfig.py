#!/usr/bin/env python3
import demes
import demesdraw

def size_max(graph):
    return max(
        max(epoch.start_size, epoch.end_size)
        for deme in graph.demes
        for epoch in deme.epochs
    )

graph = demes.load("models/IM.yaml")
w = 0.8 * size_max(graph)
positions = dict(A=0, X=-w, Y=w)
ax = demesdraw.utils.get_axes(aspect=1)
ax = demesdraw.tubes(graph, ax=ax, positions=positions, seed=1, inf_ratio=0.4)
ax.figure.savefig(
    "fig/IM.pdf",
    # Save with a transparent background.
    transparent=True,
)
