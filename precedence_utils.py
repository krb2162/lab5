"""
Functions to check if a schedule is conflict serializable.
"""

from typing import List, Set
from precedence_graph import PrecedenceGraph 


def has_cycles(graph: PrecedenceGraph) -> bool:
    """
    Checks if the given graph has cycles.

    Returns:
        True if the graph has cycles, False otherwise.
    """
    # visited is a set of visited nodes
    visited = set()
    # rec_stack is a set of nodes in the current recursion stack
    rec_stack = set()

    def _has_cycles_util(transaction_id: str) -> bool:
        """
        Utility function to check if the graph has cycles.

        Returns:
            True if the graph has cycles, False otherwise.

        TODO: Implement this helper function to check if the graph has cycles
        by completing the following steps.
        """
        # print("utils:")
        # print(transaction_id)
        # print(rec_stack)
        # print(visited)
        # TODO 1: check if the node is in the recursion stack or
        # has already been visited and return accordingly (4 lines)

        if(transaction_id in rec_stack):
            return True

        if(transaction_id in visited):
            # print("already visited!")
            return False

        # TODO 2: Mark the node as visited and add it to the recursion stack
        # Mark the node as visited and add it to the recursion stack (2 lines)
        visited.add(transaction_id)
        rec_stack.add(transaction_id)

        # TODO 3: Recursively check all neighbours for cycles (~3 lines)
        # print(graph.nodes[transaction_id].edges)
        for neighbor in graph.nodes[transaction_id].edges:
            # print(neighbor)
            # print(type(neighbor))
            # print(neighbor.id)
            if(_has_cycles_util(neighbor.id)):
                return True

        # TODO 4: Remove the node from the recursion stack (1 line)
        rec_stack.remove(transaction_id)

        # TODO 5: Return no cycle found
        return False

    # Check for cycles in all nodes
    for tx_id in graph.nodes:
        if _has_cycles_util(tx_id):
            return True

    return False


def is_conflict_serializable(precedence_graph: PrecedenceGraph) -> bool:
    """
    Check if a schedule is conflict serializable.


    Returns:
        True if the schedule is conflict serializable, False otherwise.
    """
    # TODO: 1 line of code
    # conflict serializable means no cycles?
    # return False  # Change this line
    return not has_cycles(precedence_graph)


def find_all_topological_sorts(pg: PrecedenceGraph) -> List[List[str]]:
    """
    Find all topological sorts of the precedence graph of the schedule
    """
    # Return an empty list if the schedule is not conflict serializable
    if not is_conflict_serializable(pg):
        return []

    # nodes in the graph (Dictionary of transaction id to Node object)
    nodes = pg.nodes

    # Initialize in-degrees for each node
    in_degrees = {node: 0 for node in nodes}
    for node in nodes.values():
        for edge in node.edges:
            in_degrees[edge.id] += 1

    # visited is used to keep track of visited nodes
    visited: Set[str] = set()
    # stack is used to keep track of the current topological sort
    stack: List[str] = []
    # all_orders is a list of all topological sorts
    all_orders: List[List[str]] = []

    def _all_topological_sorts_util(visited: Set[str],
                                    stack: List[str],
                                    all_orders: List[List[str]]) -> None:
        """
        Utility function to find all topological sorts of the graph.

        This function is a recursive backtracking function that explores all
        possible topological sorts of the graph.

        TODO: Implement this function to find all topological sorts of the
        graph by completing the following steps.
        """
        # TODO 1: Check if all nodes are visited; if so, record the current
        # order by adding a COPY of the stack to all_orders and return]
        print(visited)
        not_all_visited = False
        for node in nodes:
            print(node)
            if(node not in visited):
                not_all_visited = True
        if(not not_all_visited):
            all_orders.append(stack.copy())
            return

        print('----')
        # Iterate over all nodes
        for tx, node in nodes.items():
            print(node)
            print(tx)
            # TODO 2: Proceed only if node is unvisited and has no
            # incoming edges from unvisited nodes
            proceed = True
            if(node.id in visited):
                proceed = False
            # FIXME
            # does node.edges show incoming or outgoing edges? set of destination nodes
            # so we want to find nodes that are unvisited and then see if in their edges if this node is in it
            # to find all unvisited nodes we can do nodes - visisted? 
            unvisited = []
            for n in nodes:
                print(n)
                if n not in visited:
                    unvisited.append(n)
            print(unvisited)

            for unvisited_node_id in unvisited:
                for unvisited_node_neighbor in nodes[unvisited_node_id].edges:
                    if(unvisited_node_neighbor == tx):
                        proceed = False

            if (proceed):  # Replace True with the correct condition
                # TODO 3: Visit the node and add it to the topological sort
                # stack (2 lines)
                visited.add(node.id) # actually id
                stack.append(node.id) # actually id

                # TODO 4: Decrement in-degrees of successors
                # (2 lines)

                # TODO 5: Recurse (1 line)

                # TODO 6: Backtrack: un-visit the node and restore in-degrees
                # of successors (4 lines)
                visited.remove(node.id) # actually id
                # restore in-degrees of successors
                pass

    _all_topological_sorts_util(visited, stack, all_orders)

    return all_orders
