from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import numpy as np


@dataclass
class Node:
    """Node that holds information such as cost

    P is the priority of the node, and data has the information about the
    game state being held and path. Value is the game state being held.
    """

    index: int
    p: float
    value: str
    data: Dict[str, Any]

    def __repr__(self):
        return f"|{self.value}|"


def get_parent(index: int) -> int:
    """Returns the parent of the heap node

    For a heap array, this function returns the address of the parent node

    Parameters
    ----------
    index : int
        Child node to get the parent of

    Returns
    -------
    int
        Address of the parent node, or the node itself if there is only one node
    """
    if index == 0:
        return 0
    elif index % 2 == 0:
        return int((index - 2) / 2)
    else:
        return int((index - 1) / 2)


def get_children(index: int, limit: int) -> Tuple[int, int]:
    """Returns the two children of the node at the index of the binary heap node

    The node at the index 'index' is retrieved and its children are returned.
    The limit must be the length of the binary heap.

    Parameters
    ----------
    index : int
        The parent node to get the children from
    limit : int
        The length of the binary heap

    Returns
    -------
    Tuple[int, int]
        A Tuple with the index of the two children. If there are only two Nodes
        on the binary heap, where the first is the parent, this function returns
        the only child twice, one in the original position and one in the position
        of the other child.

    Raises
    ------
    IndexError
        If the child index is out of limit, then there is no child actually
    """
    if limit == 2:
        return (1, 1)
    elif 2 * index + 2 < limit:
        return (2 * index + 1, 2 * index + 2)
    raise IndexError("Index out of range")


def get_smallest_child(heap: List[Node], index: int) -> int:
    """Simple comparison between the children of a node."

    It compares the priority of the children of a node and returns the index
    of the child with the smallest priority value (highest priority).

    Parameters
    ----------
    heap : List[Node]
        A binary min heap in the form of a list of Nodes
    index : int
        The index of the parent node to get the children from

    Returns
    -------
    int
        The index of the smallest child
    """
    try:
        left, right = get_children(index, len(heap))
        if heap[left].p <= heap[right].p:
            return left
        return right
    except:
        return -1


def bubble_up(heap: List[Node], index: int) -> None:
    """Fixes the binary heap after an insertion

    When an insertion happens, the binary heap may be violated, with a smaller
    value at the leaves. Bubble up will make the smaller value "surface" on the
    heap and preserve the heap invariant.

    Parameters
    ----------
    heap : List[Node]
        A binary min heap in the form of a list of Nodes
    index : int
        The index to bubble up from, mostly the index of the insertion
    """
    parent = get_parent(index)
    if index != parent and heap[index].p < heap[parent].p:
        heap[index], heap[parent] = heap[parent], heap[index]
        heap[index].index, heap[parent].index = index, parent
        bubble_up(heap, parent)


def bubble_down(heap: List[Node], index: int) -> None:
    """Fixes the binary heap after a deletion

    When a deletion occurs, the binary heap invariant may be violated. This is
    an attempt to fix the heap invariant by returning a node with high value to
    the bottom.

    Parameters
    ----------
    heap : List[Node]
        A binary min heap in the form of a list of Nodes
    index : int
        The index to bubble up from, mostly zero for a polling operation
    """
    chosen = get_smallest_child(heap, index)
    if chosen > 0 and heap[index].p > heap[chosen].p:
        heap[index], heap[chosen] = heap[chosen], heap[index]
        heap[index].index, heap[chosen].index = index, chosen
        bubble_down(heap, chosen)


def insert(value: Node, heap: List[Node]) -> None:
    """Inserts the node into the heap, preserving the heap invariant

    Parameters
    ----------
    value : Node
        Node to be inserted, where its property p is the priority
    heap : List[Node]
        A binary min heap in the form of a list of Nodes
    """
    heap.append(value)
    bubble_up(heap, len(heap) - 1)


def poll(heap: List[Node]) -> Node:
    """Returns the node of highest priority in the heap (smallest value)

    Parameters
    ----------
    heap : List[Node]
        A binary min heap in the form of a list of Nodes

    Returns
    -------
    Node
        The element polled from the heap
    """
    last_child = len(heap) - 1
    heap[last_child], heap[0] = heap[0], heap[last_child]
    removed = heap.pop()

    if len(heap) > 1:
        bubble_down(heap, 0)

    return removed


def update(heap: List[Node], node: Node, new_p: float) -> None:
    """Update the priority value of an element of the heap preserving the invariant

    Parameters
    ----------
    heap : List[Node]
        A binary min heap in the form of a list of Nodes
    new_p : float
        New priority
    """
    old_p = heap[node.index].p
    heap[node.index].p = new_p

    if new_p > old_p:
        bubble_down(heap, node.index)
    elif new_p < old_p:
        bubble_up(heap, node.index)
