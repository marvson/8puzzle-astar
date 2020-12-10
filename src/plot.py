from typing import List
from math import ceil, floor
from pq import Node

import matplotlib.pyplot as plt

colors = [[0.5, 1, 0.5], [1, 0.5, 1], [0.5, 1, 0.5]]  # board pattern for tables
direction = ["↑", "→", "↓", "←", " "]  # directions of movements for actions


def puzzle_step(puzzles: List[List[Node]]) -> None:
    """Plots a list of puzzles with their costs and the actions

    For each puzzle in the list, it plots the puzzle, the g score, the f score
    and the action taken to get to that configuration. It does nothing if there
    is nothing to plot.

    Parameters
    ----------
    puzzles : List[Node]
        List of linear representations of 8-puzzle boards
    """
    length = len(puzzles)

    if length == 0:
        return

    ncols = min(length, 6)  # always 6 columns, or less if there are less than 6
    nrows = ceil(length / 6)

    figsize = (9, nrows * 2)  # width fixed and height variable
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

    for ax, puzzle in zip(axs.flat, puzzles):
        list_puzzle = list(puzzle.value)  # transform in list of strings

        img = ax.imshow(colors, interpolation="nearest")
        img.set_cmap("PuOr")  # Bilateral color, best that I found

        for i in range(3):
            for j in range(3):
                ax.text(
                    i,
                    j,
                    list_puzzle[i + j * 3],  # since it's linear
                    ha="center",
                    va="center",
                    color="w",
                )

        ax.text(0, 3, f"F {puzzle.p}", ha="center", va="center", color="red")
        ax.text(1, 3, f"G {puzzle.data['g']}", ha="center", va="center", color="green")
        ax.text(
            2,
            3,
            direction[puzzle.data["action"]],
            ha="center",
            va="center",
            color="purple",
        )

    # We need this part because of the zip in the last loop that limits the iteration
    for ax in axs.flat:
        ax.axis("off")  # We don't want to show axis

    fig.show()


def puzzle_solution(puzzles: List[List[Node]]) -> None:
    """Plots the solution of a 8-puzle game

    It does nothing if there is nothing to plot.

    Parameters
    ----------
    puzzles : List[Node]
        List of linear representations of 8-puzzle boards of the solution
    """
    length = len(puzzles)

    if length == 0:
        return

    ncols = min(length, 6)  # always 6 columns, or less if there are less than 6
    nrows = ceil(length / 6)

    figsize = (9, nrows * 2)  # width fixed and height variable
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

    index = 0
    for ax, puzzle in zip(axs.flat, puzzles):
        list_puzzle = list(puzzle.value)  # transform in list of strings

        img = ax.imshow(colors, interpolation="nearest")
        img.set_cmap("PuOr")  # Bilateral color, best that I found

        for i in range(3):
            for j in range(3):
                ax.text(
                    i,
                    j,
                    list_puzzle[i + j * 3],  # since it's linear
                    ha="center",
                    va="center",
                    color="w",
                )

        ax.text(0, 3, index, ha="center", va="center", color="red")
        ax.text(1, 3, f"C {puzzle.data['g']}", ha="center", va="center", color="green")
        ax.text(
            2,
            3,
            direction[puzzle.data["action"]],
            ha="center",
            va="center",
            color="purple",
        )
        index += 1

    # We need this part because of the zip in the last loop that limits the iteration
    for ax in axs.flat:
        ax.axis("off")  # We don't want to show axis

    fig.show()


def puzzle_simple(puzzle: str) -> None:
    """Plots a 8-puzzle board

    Parameters
    ----------
    puzzle : str
        Linear representation of a 8-puzzle board
    """
    list_puzzle = list(puzzle)  # transform in list of strings

    plt.figure(figsize=(1.5, 1.5))
    img = plt.imshow(colors, interpolation="nearest")
    img.set_cmap("PuOr")  # Bilateral color, best that I found

    for i in range(3):
        for j in range(3):
            plt.text(
                i,
                j,
                list_puzzle[i + j * 3],  # since it's linear
                ha="center",
                va="center",
                color="w",
            )
    plt.axis("off")  # We don't want to show axis
