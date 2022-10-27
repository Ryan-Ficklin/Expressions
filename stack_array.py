from typing import Optional, List, Any

# Stack class implemented with array
class Stack:
    """Implements an efficient last-in first-out Abstract Data Type using a Python List"""

    # capacity is max number of Nodes, init_items is optional List parameter for initialization
    # if the length of the init_items List exceeds capacity, raise IndexError
    def __init__(self, capacity: int, init_items: Optional[List] = None):
        """Creates an empty stack with a capacity"""
        self.capacity = capacity        # capacity of stack
        self.items = [None]*capacity    # array for stack
        self.num_items = 0              # number of items in stack
        if init_items is not None:      # if init_items is not None, initialize stack
            if len(init_items) > capacity:
                raise IndexError
            else:
                self.num_items = len(init_items)
                self.items[:self.num_items] = init_items

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Stack):
            return (self.capacity == other.capacity
            and self.items[:self.num_items] == other.items[:other.num_items])
        else:
            return False

    def __repr__(self) -> str:
        return ("Stack({!r}, {!r})".format(self.capacity, self.items[:self.num_items]))

    def is_empty(self) -> bool:
        """Returns True if the stack is empty, and False otherwise
           MUST have O(1) performance"""
        return self.num_items == 0

    def is_full(self) -> bool:
        """Returns True if the stack is full, and False otherwise
           MUST have O(1) performance"""
        return self.num_items == self.capacity

    def push(self, item: Any) -> Any:
        """If stack is not full, pushes item on stack.
           If stack is full when push is attempted, raises IndexError
           MUST have O(1) performance"""
        if self.is_full():
            raise IndexError
        self.items[self.num_items] = item
        self.num_items += 1


    def pop(self) -> Any:
        """If stack is not empty, pops item from stack and returns item.
           If stack is empty when pop is attempted, raises IndexError
           MUST have O(1) performance"""
        if self.is_empty():
            raise IndexError
        self.num_items -= 1
        return self.items[self.num_items]


    def peek(self) -> Any:
        """If stack is not empty, returns next item to be popped (but does not remove the item)
           If stack is empty, raises IndexError
           MUST have O(1) performance"""
        if self.is_empty():
            raise IndexError
        return self.items[self.num_items-1]

    def size(self) -> int:
        """Returns the number of elements currently in the stack, not the capacity
           MUST have O(1) performance"""
        return self.num_items
