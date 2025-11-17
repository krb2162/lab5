# import precedence_utils as pu
"""
Author: Rami Pellumbi

This is an implementation of the precedence graph algorithm for conflict
serializability.
"""
from collections import namedtuple
from typing import Dict, List, Set, Union

# An operation is a tuple of three elements:
# - transaction: the transaction id (e.g., T1)
# - type: the operation type (read or write)
# - item: the item being read or written (e.g., A)
Operation = namedtuple("Operation", ["transaction", "type", "item"])

"""
A schedule is a list of steps, where each step is a list of operations.

- Suppose we have m transactions and k steps. We may view the schedule
  as a matrix of size k x m, where each cell contains the operations of a
  transaction in a step (may be None). That is, the (i, j)-th cell contains
  the operation of transaction Tj in step i, 1 <= i <= k, 1 <= j <= m.
- Two operations in the same step, i.e., op_1 and op_2 are both in the i-th
  row, may run in any order.
- Two operations in different steps, i.e., op_1 is in the i-th row and op_2
  is in the j-th row, and i < j, must run in the order op_1 followed by op_2.
"""
Schedule = List[List[Union[Operation, None]]]


class Node:
    """
    Represents a node in the graph, which is a transaction in this context.
    """

    def __init__(self, transaction_id):
        self.id = transaction_id
        # edges is a set of destination nodes from this node
        self.edges: Set["Node"] = set()

    def add_edge(self, destination_node: "Node"):
        """Add an edge from this node to another."""
        self.edges.add(destination_node)

    def __repr__(self):
        """String representation for debugging."""
        return f"Node({self.id})"


class PrecedenceGraph:
    """
    Class to represent a precedence graph given a schedule
    """

    def __init__(self, schedule: Schedule) -> None:
        # maps a transaction id (e.g., T1) to a Node object
        self._nodes: Dict[str, Node] = {}
        # flag to check if the graph has been initialized
        self.is_initialized = False
        # initialize self._nodes and set self.is_initialized to True
        self._initialize_nodes(schedule)
        # build the precedence graph from the schedule
        self._build_graph(schedule)

    def _add_node_if_not_exists(self, transaction_id):
        """Add a node to the graph if it is not already present."""
        if transaction_id not in self._nodes:
            self._nodes[transaction_id] = Node(transaction_id)

    def _initialize_nodes(self, schedule: Schedule):
        """
        Initialize all transactions in the graph
        """
        for step in schedule:
            for operation in step:
                if operation is not None:
                    tx = operation.transaction
                    self._add_node_if_not_exists(tx)
        self.is_initialized = True

    def _has_conflict(self, operation1: Operation, operation2: Operation) -> bool:
        """
        Determine if two operations conflict.

        A conflict occurs if two different transactions are operating
        on the same item and at least one of them is a write operation.

        Returns:
            True if the operations conflict, False otherwise.
        """
        # An operation is a tuple of three elements:
        # - transaction: the transaction id (e.g., T1)
        # - type: the operation type (read or write)
        # - item: the item being read or written (e.g., A))

        # TODO: Implement this function to check if two operations conflict
        # Hint: compute three boolean values and return their conjunction
        if operation1.transaction == operation2.transaction:
            return False

        operation_type_1 = operation1[1]
        item_1 = operation1[2]

        operation_type_2 = operation2[1]
        item_2 = operation2[2]

        return item_1 == item_2 and (operation_type_2 == "write" or operation_type_1 == "write")


    def _build_graph(self, schedule: Schedule):
        """
        Build the precedence graph from the schedule

        TODO: Implement this function to build the precedence graph
        by following the steps below.
        """
        if not self.is_initialized:
            raise ValueError("Nodes have not been initialized")

        # A schedule is a list of steps, where each step is a list of operations.

        # - Suppose we have m transactions and k steps. We may view the schedule
        #   as a matrix of size k x m, where each cell contains the operations of a
        #   transaction in a step (may be None). That is, the (i, j)-th cell contains
        #   the operation of transaction Tj in step i, 1 <= i <= k, 1 <= j <= m.
        # - Two operations in the same step, i.e., op_1 and op_2 are both in the i-th
        #   row, may run in any order.
        # - Two operations in different steps, i.e., op_1 is in the i-th row and op_2
        #   is in the j-th row, and i < j, must run in the order op_1 followed by op_2.
        # """
        # Schedule = List[List[Union[Operation, None]]]        

        # TODO: Step 1: flatten the schedule into a list of operations,
        # maintaining the order of the operations

        # basically turn the matrix into a flat list
        # iterate through the matrix by row, and they can go in any order? 
        operations = []
        for step in schedule:
            for operation in step:
                if (operation != None):
                    operations.append(operation)

        # TODO: Step 2: add edges between nodes that have conflicts
        # An edge from node T1 to node T2 means that T1 must come before T2
        # Hint 1: use the _has_conflict method to check two operations conflict
        # Hint 2: add an edge from the source node to the destination node
        # ~8 lines of code

        for i in range(0, len(operations)-1):
            for j in range(i+1, len(operations)):
                if(self._has_conflict(operation1=operations[i], operation2=operations[j])):
                    source = self._nodes[operations[i].transaction]
                    destination = self._nodes[operations[j].transaction]
                    source.add_edge(destination)

    def __repr__(self) -> str:
        rep = ""
        for src, node in self._nodes.items():
            destinations = node.edges
            if destinations:
                # Format: Source -> [Destination1, Destination2, ...]
                formatted_destinations = ", ".join(dest.id for dest in destinations)
                rep += f"Source {src} -> [{formatted_destinations}]\n"

            else:
                # Explicitly state when there are no outgoing edges
                rep += f"Source {src} has no outgoing edges\n"

        return rep

    @property
    def nodes(self) -> Dict[str, Node]:
        """Return the nodes in the graph."""
        return self._nodes

if __name__ == "__main__":
    operation1ra = Operation(transaction="T1", type="read", item="A")
    operation1wa = Operation(transaction="T1", type="write", item="A")
    operation1rc = Operation(transaction="T1", type="read", item="C")
    operation1wc = Operation(transaction="T1", type="write", item="C")
    operation1rg = Operation(transaction="T1", type="read", item="G")

    operation2wh = Operation(transaction="T2", type="write", item="H")
    operation2rh = Operation(transaction="T2", type="read", item="H")
    operation2rd = Operation(transaction="T2", type="read", item="D")
    operation2wd = Operation(transaction="T2", type="write", item="D")

    operation3rb = Operation(transaction="T3", type="read", item="B")
    operation3wb = Operation(transaction="T3", type="write", item="B")
    operation3ra = Operation(transaction="T3", type="read", item="A")
    operation3re = Operation(transaction="T3", type="read", item="E")
    operation3we = Operation(transaction="T3", type="write", item="E")

    operation4re = Operation(transaction="T4", type="read", item="E")
    operation4we = Operation(transaction="T4", type="write", item="E")
    operation4rg = Operation(transaction="T4", type="read", item="G")
    operation4rh = Operation(transaction="T4", type="read", item="H")
    operation4wh = Operation(transaction="T4", type="write", item="H")
    operation4rf = Operation(transaction="T4", type="read", item="F")

    operation5rf = Operation(transaction="T5", type="read", item="F")
    operation5wf = Operation(transaction="T5", type="write", item="F")
    operation5rc = Operation(transaction="T5", type="read", item="C")
    operation5wc = Operation(transaction="T5", type="write", item="C")

    schedule = [[operation1ra, None, operation3rb, operation4re, operation5rf],
                [operation1wa, operation2rh, operation3wb, operation4we, operation5wf],
                [None, operation2wh, operation3ra, operation4rg, operation5rf],
                [operation1rc, None, operation3ra, operation4rh, operation5wf],
                [operation1wc, operation2rd, operation3ra, operation4rh, None],
                [None, operation2wd, operation3re, operation4wh, operation5rc],
                [None, operation2rd, operation3we, None, operation5wc],
                [operation1rg, operation2wd, None, operation4rf, operation5rc]]
    cycle_schedule = [[operation1wa, None],
                      [None, operation3ra],
                      [operation3wb, operation1wa]]
    no_cycle = [[operation1wa, operation2rd],
                [operation3ra, operation4rf]]
    
#     {Node(T3), Node(T2)}
# {Node(T1)}
# {Node(T3), Node(T1)}

    # graphsched = PrecedenceGraph(schedule)
    graph = PrecedenceGraph(cycle_schedule)
    no_cycle_graph = PrecedenceGraph(no_cycle)
    print('--------')
    # print(graph)
    # print(pu.has_cycles(graph))
    # print(pu.has_cycles(no_cycle_graph))

    
