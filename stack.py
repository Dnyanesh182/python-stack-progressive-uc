# UC4 - Implement Multiple Stacks in a Single Array

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


class MultiStack(Generic[T]):
    """
    Multiple stacks in a single shared array with:
    - two independent stacks
    - memory-efficient storage
    - dynamic growth
    - optional maximum capacity
    - validation
    """

    def __init__(self, initial_capacity: int = 4, max_capacity: Optional[int] = None, allow_none: bool = False) -> None:
        if initial_capacity <= 1:
            raise ValueError("Initial capacity must be greater than 1.")
        if max_capacity is not None and max_capacity < initial_capacity:
            raise ValueError("Max capacity cannot be less than initial capacity.")

        self.__array: list[Optional[T]] = [None] * initial_capacity
        self.__capacity = initial_capacity
        self.__max_capacity = max_capacity
        self.__allow_none = allow_none

        self.__top1 = -1
        self.__top2 = initial_capacity

    def push(self, stack_number: int, item: T) -> None:
        self.__validate(item)

        if self.__top1 + 1 == self.__top2:
            self.__grow()

        if stack_number == 1:
            self.__top1 += 1
            self.__array[self.__top1] = item
        elif stack_number == 2:
            self.__top2 -= 1
            self.__array[self.__top2] = item
        else:
            raise ValueError("Invalid stack number. Use 1 or 2.")

    def pop(self, stack_number: int) -> T:
        if stack_number == 1:
            if self.__top1 == -1:
                raise StackUnderflowError("Cannot pop from empty Stack 1.")
            item = self.__array[self.__top1]
            self.__array[self.__top1] = None
            self.__top1 -= 1
            return item  # type: ignore

        if stack_number == 2:
            if self.__top2 == self.__capacity:
                raise StackUnderflowError("Cannot pop from empty Stack 2.")
            item = self.__array[self.__top2]
            self.__array[self.__top2] = None
            self.__top2 += 1
            return item  # type: ignore

        raise ValueError("Invalid stack number. Use 1 or 2.")

    def peek(self, stack_number: int) -> T:
        if stack_number == 1:
            if self.__top1 == -1:
                raise StackUnderflowError("Cannot peek into empty Stack 1.")
            return self.__array[self.__top1]  # type: ignore

        if stack_number == 2:
            if self.__top2 == self.__capacity:
                raise StackUnderflowError("Cannot peek into empty Stack 2.")
            return self.__array[self.__top2]  # type: ignore

        raise ValueError("Invalid stack number. Use 1 or 2.")

    def is_empty(self, stack_number: int) -> bool:
        if stack_number == 1:
            return self.__top1 == -1
        if stack_number == 2:
            return self.__top2 == self.__capacity
        raise ValueError("Invalid stack number. Use 1 or 2.")

    def size(self, stack_number: int) -> int:
        if stack_number == 1:
            return self.__top1 + 1
        if stack_number == 2:
            return self.__capacity - self.__top2
        raise ValueError("Invalid stack number. Use 1 or 2.")

    def total_size(self) -> int:
        return self.size(1) + self.size(2)

    def capacity(self) -> int:
        return self.__capacity

    def display(self, stack_number: int) -> list[T]:
        if stack_number == 1:
            return [self.__array[i] for i in range(self.__top1, -1, -1)]  # type: ignore
        if stack_number == 2:
            return [self.__array[i] for i in range(self.__top2, self.__capacity)]  # type: ignore
        raise ValueError("Invalid stack number. Use 1 or 2.")

    def __grow(self) -> None:
        new_capacity = self.__capacity * 2

        if self.__max_capacity is not None:
            if self.__capacity >= self.__max_capacity:
                raise StackOverflowError("Shared array has reached maximum capacity.")
            new_capacity = min(new_capacity, self.__max_capacity)

        new_array: list[Optional[T]] = [None] * new_capacity

        for i in range(self.__top1 + 1):
            new_array[i] = self.__array[i]

        stack2_size = self.__capacity - self.__top2
        new_top2 = new_capacity - stack2_size

        j = new_top2
        for i in range(self.__top2, self.__capacity):
            new_array[j] = self.__array[i]
            j += 1

        self.__array = new_array
        self.__top2 = new_top2
        self.__capacity = new_capacity

    def __validate(self, item: Any) -> None:
        if item is None and not self.__allow_none:
            raise StackValidationError("None value is not allowed in this stack.")

    def __repr__(self) -> str:
        return (
            f"MultiStack(stack1={self.display(1)}, stack2={self.display(2)}, "
            f"total_size={self.total_size()}, capacity={self.__capacity})"
        )


def main() -> None:
    try:
        initial_capacity = int(input("Enter initial shared array capacity: "))
        max_limit_input = input("Enter maximum shared capacity (press Enter for no limit): ").strip()
        max_capacity = int(max_limit_input) if max_limit_input else None

        stacks = MultiStack[str](initial_capacity=initial_capacity, max_capacity=max_capacity)

        n1 = int(input("Enter number of elements to push into Stack 1: "))
        for i in range(n1):
            value = input(f"Enter element {i + 1} for Stack 1: ")
            stacks.push(1, value)
            print(f"Element '{value}' pushed into Stack 1. Current shared capacity: {stacks.capacity()}")

        n2 = int(input("\nEnter number of elements to push into Stack 2: "))
        for i in range(n2):
            value = input(f"Enter element {i + 1} for Stack 2: ")
            stacks.push(2, value)
            print(f"Element '{value}' pushed into Stack 2. Current shared capacity: {stacks.capacity()}")

        print("\nStack 1 (Top to Bottom):", stacks.display(1))
        print("Stack 2 (Top to Bottom):", stacks.display(2))
        print("Stack 1 Top Element:", stacks.peek(1))
        print("Stack 2 Top Element:", stacks.peek(2))

        print("\nPopped from Stack 1:", stacks.pop(1))
        print("Popped from Stack 2:", stacks.pop(2))

        print("\nStack 1 After Pop:", stacks.display(1))
        print("Stack 2 After Pop:", stacks.display(2))
        print("Total Elements in Shared Array:", stacks.total_size())
        print("Current Shared Capacity:", stacks.capacity())

    except ValueError as error:
        print("Input Error:", error)
    except StackError as error:
        print("Stack Error:", error)


if __name__ == "__main__":
    main()