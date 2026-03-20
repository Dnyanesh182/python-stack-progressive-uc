# UC3 - Build Stack Using Linked List

from typing import Generic, TypeVar, Optional, Any

T = TypeVar("T")


class StackError(Exception):
    """Base exception for stack-related errors."""
    pass


class StackUnderflowError(StackError):
    """Raised when pop or peek is performed on an empty stack."""
    pass


class StackOverflowError(StackError):
    """Raised when stack exceeds the maximum allowed capacity."""
    pass


class StackValidationError(StackError):
    """Raised when invalid data is pushed into the stack."""
    pass


class Node(Generic[T]):
    def __init__(self, data: T) -> None:
        self.data: T = data
        self.next: Optional["Node[T]"] = None


class Stack(Generic[T]):
    """
    Dynamic Stack using Linked List with:
    - encapsulation
    - validation
    - optional maximum capacity
    - automatic growth behavior
    """

    def __init__(self, initial_capacity: int = 2, max_capacity: Optional[int] = None, allow_none: bool = False) -> None:
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be greater than 0.")
        if max_capacity is not None and max_capacity < initial_capacity:
            raise ValueError("Max capacity cannot be less than initial capacity.")

        self.__top: Optional[Node[T]] = None
        self.__size: int = 0
        self.__capacity: int = initial_capacity
        self.__max_capacity: Optional[int] = max_capacity
        self.__allow_none: bool = allow_none

    def push(self, item: T) -> None:
        self.__validate(item)

        if self.__size >= self.__capacity:
            self.__grow()

        new_node = Node(item)
        new_node.next = self.__top
        self.__top = new_node
        self.__size += 1

    def pop(self) -> T:
        if self.is_empty():
            raise StackUnderflowError("Cannot pop from an empty stack.")

        assert self.__top is not None
        popped_data = self.__top.data
        self.__top = self.__top.next
        self.__size -= 1
        return popped_data

    def peek(self) -> T:
        if self.is_empty():
            raise StackUnderflowError("Cannot peek into an empty stack.")

        assert self.__top is not None
        return self.__top.data

    def is_empty(self) -> bool:
        return self.__size == 0

    def size(self) -> int:
        return self.__size

    def capacity(self) -> int:
        return self.__capacity

    def max_capacity(self) -> Optional[int]:
        return self.__max_capacity

    def display(self) -> list[T]:
        elements: list[T] = []
        current = self.__top

        while current is not None:
            elements.append(current.data)
            current = current.next

        return elements

    def __grow(self) -> None:
        new_capacity = self.__capacity * 2

        if self.__max_capacity is not None:
            if self.__capacity >= self.__max_capacity:
                raise StackOverflowError("Stack has reached maximum capacity.")
            new_capacity = min(new_capacity, self.__max_capacity)

        self.__capacity = new_capacity

    def __validate(self, item: Any) -> None:
        if item is None and not self.__allow_none:
            raise StackValidationError("None value is not allowed in this stack.")

    def __repr__(self) -> str:
        return (
            f"Stack(top_to_bottom={self.display()}, size={self.__size}, "
            f"capacity={self.__capacity}, max_capacity={self.__max_capacity})"
        )


def main() -> None:
    try:
        initial_capacity = int(input("Enter initial stack capacity: "))
        max_limit_input = input("Enter maximum stack capacity (press Enter for no limit): ").strip()
        max_capacity = int(max_limit_input) if max_limit_input else None

        stack = Stack[str](initial_capacity=initial_capacity, max_capacity=max_capacity)

        n = int(input("Enter number of elements to push into stack: "))

        for i in range(n):
            value = input(f"Enter element {i + 1}: ")
            stack.push(value)
            print(f"Element '{value}' pushed successfully. Current capacity: {stack.capacity()}")

        print("\nStack Elements (Top to Bottom):", stack.display())
        print("Current Stack Size:", stack.size())
        print("Current Stack Capacity:", stack.capacity())

        print("\nTop Element:", stack.peek())
        print("Popped Element:", stack.pop())
        print("Stack After Pop (Top to Bottom):", stack.display())

    except ValueError as error:
        print("Input Error:", error)
    except StackError as error:
        print("Stack Error:", error)


if __name__ == "__main__":
    main()