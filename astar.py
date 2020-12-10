from puzzle import action_of
from typing import Callable, Dict, List, Optional
from pq import Node, insert, poll, update


def path_of(node: Node) -> List[Node]:
    """Given a last node in the solution, it iterates back and returns the path

    Parameters
    ----------
    node : Node
        Last node of a A* solution

    Returns
    -------
    List[Node]
        Solution in order, including the initial state
    """
    path = []

    current = node
    while current.data["parent"] is not None:
        path.append(current)
        current = current.data["parent"]
    path.append(current)
    path.reverse()

    return path


def astar(
    initial: str,
    cost: Callable[[str, str], float],
    neighborhood: Callable[[str], List[str]],
    h: Callable[[str], float],
    terminal: str,
    print_node: Optional[Callable[[List[str]], None]] = None,
    print_fringe: Optional[Callable[[List[List[str]]], None]] = None,
) -> List[str]:
    """A* algorithm for a state in string format

    Parameters
    ----------
    initial : str
        Initial state
    cost : Callable[[str, str], float]
        Cost of edge (x,y) fro two nodes x and y
    neighborhood : Callable[[str], List[str]]
        All possible states that can be reached by an action on given state
    h : Callable[[str], float]
        Heuristic function (must be admissible)
    terminal : str
        Terminal state
    print_node : Optional[Callable[[List[str]], None]]
        Function that prints a single node, defaults to None
    print_fringe : Optional[Callable[[List[List[str]]], None]]
        Function that prints the fringe, defaults to None

    Returns
    -------
    List[str]
        Step-to-step solution found

    Raises
    ------
    RuntimeError
        If there is no solution
    """
    f_score = h(initial)  # since g_score is 0, f_score = h(s)
    initial_state = Node(0, f_score, initial, {"g": 0, "parent": None, "action": -1})

    hashtable: Dict[str, Node] = {}
    fringe: List[Node] = [initial_state]
    while len(fringe) > 0:
        current = poll(fringe)
        if current.value == terminal:
            return path_of(current)

        if print_node:
            print_node(current.value)

        for state in neighborhood(current.value):
            g_score = current.data["g"] + cost(current.value, state)
            try:
                neighbor = hashtable[state]
                if g_score < neighbor.data["g"]:
                    f_score = g_score + h(state)
                    neighbor.data["parent"] = current
                    neighbor.data["g"] = g_score
                    neighbor.data["action"] = action_of(current.value, state)
                    update(fringe, neighbor, f_score)
            except:
                f_score = g_score + h(state)
                neighbor = Node(
                    0,
                    f_score,
                    state,
                    {
                        "g": g_score,
                        "parent": current,
                        "action": action_of(current.value, state),
                    },
                )
                hashtable[state] = neighbor
                insert(neighbor, fringe)

        if print_fringe:
            print_fringe(fringe)
    raise RuntimeError("No terminal state found")
