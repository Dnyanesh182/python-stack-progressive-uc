# UC2 - Implement Dynamic Stack with Capacity Control

from typing import Generic, TypeVar, List, Any, Optional

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


class Stack(Generic[T]):
    """
    Dynamic Stack ADT with encapsulation, validation,
    optional maximum capacity, and automatic growth.
    """

    def __init__(self, initial_capacity: int = 2, max_capacity: Optional[int] = None, allow_none: bool = False) -> None:
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be greater than 0.")
        if max_capacity is not None and max_capacity < initial_capacity:
            raise ValueError("Max capacity cannot be less than initial capacity.")

        self.__items: List[T] = []
        self.__capacity = initial_capacity
        self.__max_capacity = max_capacity
        self.__allow_none = allow_none

    def push(self, item: T) -> None:
        self.__validate(item)

        if self.size() >= self.__capacity:
            self.__grow()

        self.__items.append(item)

    def pop(self) -> T:
        if self.is_empty():
            raise StackUnderflowError("Cannot pop from an empty stack.")
        return self.__items.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise StackUnderflowError("Cannot peek into an empty stack.")
        return self.__items[-1]

    def is_empty(self) -> bool:
        return len(self.__items) == 0

    def size(self) -> int:
        return len(self.__items)

    def capacity(self) -> int:
        return self.__capacity

    def max_capacity(self) -> Optional[int]:
        return self.__max_capacity

    def display(self) -> List[T]:
        return self.__items.copy()

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
            f"Stack(items={self.__items}, size={self.size()}, "
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

        print("\nStack Elements:", stack.display())
        print("Current Stack Size:", stack.size())
        print("Current Stack Capacity:", stack.capacity())

        print("\nTop Element:", stack.peek())
        print("Popped Element:", stack.pop())
        print("Stack After Pop:", stack.display())

    except ValueError as error:
        print("Input Error:", error)
    except StackError as error:
        print("Stack Error:", error)


if __name__ == "__main__":
    main()