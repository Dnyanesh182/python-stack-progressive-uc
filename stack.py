# UC1 - Design Generic Stack ADT

from typing import Generic, TypeVar, List, Any

T = TypeVar("T")


class StackEmptyError(Exception):
    """Raised when an operation is performed on an empty stack."""
    pass


class StackValidationError(Exception):
    """Raised when invalid data is pushed into the stack."""
    pass


class Stack(Generic[T]):
    """
    Generic Stack ADT with encapsulation, validation,
    and support for multiple data types.
    """

    def __init__(self, allow_none: bool = False) -> None:
        self.__items: List[T] = []
        self.__allow_none = allow_none

    def push(self, item: T) -> None:
        self.__validate(item)
        self.__items.append(item)

    def pop(self) -> T:
        if self.is_empty():
            raise StackEmptyError("Cannot pop from an empty stack.")
        return self.__items.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise StackEmptyError("Cannot peek into an empty stack.")
        return self.__items[-1]

    def is_empty(self) -> bool:
        return len(self.__items) == 0

    def size(self) -> int:
        return len(self.__items)

    def display(self) -> List[T]:
        return self.__items.copy()

    def __validate(self, item: Any) -> None:
        if item is None and not self.__allow_none:
            raise StackValidationError("None value is not allowed in this stack.")

    def __repr__(self) -> str:
        return f"Stack({self.__items})"


def main() -> None:
    stack = Stack[str]()

    n = int(input("Enter number of elements to push into stack: "))

    for i in range(n):
        value = input(f"Enter element {i + 1}: ")
        stack.push(value)

    print("\nStack Elements:", stack.display())
    print("Top Element:", stack.peek())
    print("Popped Element:", stack.pop())
    print("Stack After Pop:", stack.display())
    print("Is Stack Empty:", stack.is_empty())
    print("Stack Size:", stack.size())


if __name__ == "__main__":
    main()