# UC9 - Design Special Stack with O(1) Min and Max Retrieval

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
    Two stacks in a single shared array with:
    - memory-efficient storage
    - dynamic growth
    - optional maximum capacity
    - validation
    """

    def __init__(self, initial_capacity: int = 6, max_capacity: Optional[int] = None, allow_none: bool = False) -> None:
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


class MinMaxStack:
    """
    Special stack with:
    - primary stack in Stack 1
    - min tracking in Stack 2
    - max tracking using separate internal stack
    - O(1) min retrieval
    - O(1) max retrieval
    """

    def __init__(self) -> None:
        self.__main_stack = MultiStack[int](initial_capacity=10)
        self.__max_stack: list[int] = []

    def push(self, value: int) -> None:
        self.__main_stack.push(1, value)

        if self.__main_stack.is_empty(2) or value <= self.__main_stack.peek(2):
            self.__main_stack.push(2, value)

        if not self.__max_stack or value >= self.__max_stack[-1]:
            self.__max_stack.append(value)

    def pop(self) -> int:
        if self.is_empty():
            raise StackUnderflowError("Cannot pop from an empty stack.")

        removed_value = self.__main_stack.pop(1)

        if removed_value == self.__main_stack.peek(2):
            self.__main_stack.pop(2)

        if removed_value == self.__max_stack[-1]:
            self.__max_stack.pop()

        return removed_value

    def peek(self) -> int:
        if self.is_empty():
            raise StackUnderflowError("Cannot peek into an empty stack.")
        return self.__main_stack.peek(1)

    def get_min(self) -> int:
        if self.is_empty():
            raise StackUnderflowError("Cannot get minimum from an empty stack.")
        return self.__main_stack.peek(2)

    def get_max(self) -> int:
        if self.is_empty():
            raise StackUnderflowError("Cannot get maximum from an empty stack.")
        return self.__max_stack[-1]

    def is_empty(self) -> bool:
        return self.__main_stack.is_empty(1)

    def size(self) -> int:
        return self.__main_stack.size(1)

    def display(self) -> list[int]:
        return self.__main_stack.display(1)


def main() -> None:
    stack = MinMaxStack()

    while True:
        try:
            print("\n--- Special Stack with O(1) Min and Max Retrieval ---")
            print("1. Push")
            print("2. Pop")
            print("3. Peek")
            print("4. Get Minimum")
            print("5. Get Maximum")
            print("6. Display Stack")
            print("7. Get Size")
            print("8. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                value = int(input("Enter integer value to push: "))
                stack.push(value)
                print(f"Value {value} pushed successfully.")
                print("Current Stack:", stack.display())

            elif choice == "2":
                removed = stack.pop()
                print(f"Popped Value: {removed}")
                print("Current Stack:", stack.display())

            elif choice == "3":
                print("Top Element:", stack.peek())

            elif choice == "4":
                print("Minimum Element:", stack.get_min())

            elif choice == "5":
                print("Maximum Element:", stack.get_max())

            elif choice == "6":
                print("Stack Elements (Top to Bottom):", stack.display())

            elif choice == "7":
                print("Stack Size:", stack.size())

            elif choice == "8":
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Please select a valid option.")

        except ValueError as error:
            print("Input Error:", error)
        except StackError as error:
            print("Stack Error:", error)


if __name__ == "__main__":
    main()