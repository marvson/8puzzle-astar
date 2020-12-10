from typing import List, Tuple
from math import floor
from random import shuffle, seed


def swap(original: List[str], orig: int, dest: int) -> str:
    """Swaps the element from position orig to destiny from the puzzle

    Parameters
    ----------
    original : List[str]
        A linear representation of a 8-puzzle board
    orig : int
        Origin position
    dest : int
        Destiny position

    Returns
    -------
    str
        The new board after the swap of the elements
    """
    action = original.copy()
    action[orig], action[dest] = action[dest], action[orig]
    return "".join(action)


def pretty(states: List[str]) -> None:
    """Pretty print of one or more 8-puzzle boards

    Parameters
    ----------
    states : List[str]
        List of linear representations of 8-puzzle boards
    """
    for state in states:
        print(state[:3])
        print(state[3:6])
        print(state[6:])
        print()


def possible_plays(state: str) -> List[int]:
    """Return possible plays from a given state

    Assuming the actions 0 to 3 to be top, right, bottom, left action, where
    the blank piece is moved to the given direction, this function returns the
    possible actions of a given state.

    Parameters
    ----------
    state : str
        A linear representation of a 8-puzzle board

    Returns
    -------
    List[int]
        List of possible actions from the given puzzle state.

    Raises
    ------
    ValueError
        It raises an error if there is no blank piece to move
    """
    states: List[Tuple[str, int]] = []

    pos_1d = state.find(" ")
    if pos_1d == -1:
        raise ValueError("There should be a space block")

    pos = (pos_1d % 3, floor(pos_1d / 3))
    if pos[1] > 0:
        states.append(0)
    if pos[0] < 2:
        states.append(1)
    if pos[1] < 2:
        states.append(2)
    if pos[0] > 0:
        states.append(3)

    return states


def play(state: str, action: int) -> str:
    """It plays the given action with the given state

    The action being one of these: up, right, down, left (0, 1, 2, 3) is applied
    to the puzzle, returning the resulting state, or raising an error if action
    is invalid.

    Parameters
    ----------
    state : str
        A linear representation of a 8-puzzle board
    action : int
        Either up, right, down or left (respectively 0, 1, 2, 3)

    Returns
    -------
    str
        Resulting linear representation of a 8-puzzle board

    Raises
    ------
    ValueError
        [description]
    """
    list_state = list(state)
    pos_1d = state.find(" ")

    if action == 0 and pos_1d >= 3:
        return swap(list_state, pos_1d, pos_1d - 3)
    elif action == 1 and pos_1d <= 7:
        return swap(list_state, pos_1d, pos_1d + 1)
    elif action == 2 and pos_1d <= 6:
        return swap(list_state, pos_1d, pos_1d + 3)
    elif action == 3 and pos_1d >= 1:
        return swap(list_state, pos_1d, pos_1d - 1)

    raise ValueError(f"Unknown or Invalid action {action} on {state}")


def states_from(state: str) -> List[str]:
    """Generates list of possible states from original state for the 8-puzzle
    game.

    Parameters
    ----------
    state : str
        A linear representation of a 8-puzzle board

    Returns
    -------
    List[str]
        List of possible states from actions on the given puzzle state.
    """
    plays = possible_plays(state)
    return [play(state, action) for action in plays]


def action_of(origin: str, destination: str) -> int:
    """Finds which action was taken from origin to destination.

    If the states origin and destination are separated by one action, it returns
    the numeric value of the action taken (0 = up, 1 = right, 2 = down, 3 = left).
    It returns -1 if they are separated by more than one action.

    Parameters
    ----------
    origin : str
        A linear representation of a 8-puzzle board, original state
    destination : str
        A linear representation of a 8-puzzle board, the resulting state

    Returns
    -------
    int
        Action taken from origin to destination, or -1 if there isn't a single
        action between the states
    """
    if sum([i == j for (i, j) in zip(list(origin), list(destination))]) == 7:
        pos_orig = origin.find(" ")
        pos_dest = destination.find(" ")

        diff = pos_dest - pos_orig

        if diff == 3:
            return 2
        elif diff == -3:
            return 0
        elif diff == 1:
            return 1
        elif diff == -1:
            return 3
    return -1


def is_solvable(state: str) -> bool:
    """Returns whether the puzzle is solvable

    The 8-puzzle game is solvable if and only if the parity of the inversion
    count is even, where one inversion is counted for each pair of elements
    in the linear representation of a 8-puzzle board where the leftmost has
    a bigger value than the rightmost being compared.

    Parameters
    ----------
    state : str
        A linear representation of a 8-puzzle board

    Returns
    -------
    bool
        Whether it's solvable or not
    """
    list_state = list(state)
    inversions = 0
    for i in range(9):
        for j in range(i + 1, 9):
            if (
                list_state[i] != " "
                and list_state[j] != " "
                and list_state[i] > list_state[j]
            ):
                inversions = inversions + 1
    return inversions % 2 == 0


def generate_solvable_state() -> str:
    """It generates a solvable 8-puzzle state

    Returns
    -------
    str
        A solvable linear representation of a 8-puzzle board
    """
    seed()

    puzzle = ["1", "2", "3", "4", "5", "6", "7", "8", " "]
    solvable = False

    while not solvable:
        shuffle(puzzle)
        solvable = is_solvable("".join(puzzle))

    return "".join(puzzle)
