# UC8 - Implement Undo/Redo State Management System

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

    def clear(self, stack_number: int) -> None:
        if stack_number == 1:
            while self.__top1 != -1:
                self.__array[self.__top1] = None
                self.__top1 -= 1
            return

        if stack_number == 2:
            while self.__top2 != self.__capacity:
                self.__array[self.__top2] = None
                self.__top2 += 1
            return

        raise ValueError("Invalid stack number. Use 1 or 2.")

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


class TextEditorStateManager:
    """
    Undo/Redo system using two stacks:
    - Stack 1 for undo history
    - Stack 2 for redo history
    """

    def __init__(self) -> None:
        self.__history = MultiStack[str](initial_capacity=10)
        self.__current_text = ""

    def type_text(self, new_text: str) -> None:
        self.__history.push(1, self.__current_text)
        self.__current_text += new_text
        self.__history.clear(2)

    def undo(self) -> str:
        if self.__history.is_empty(1):
            raise StackUnderflowError("No actions available to undo.")

        self.__history.push(2, self.__current_text)
        self.__current_text = self.__history.pop(1)
        return self.__current_text

    def redo(self) -> str:
        if self.__history.is_empty(2):
            raise StackUnderflowError("No actions available to redo.")

        self.__history.push(1, self.__current_text)
        self.__current_text = self.__history.pop(2)
        return self.__current_text

    def get_current_text(self) -> str:
        return self.__current_text

    def show_undo_history(self) -> list[str]:
        return self.__history.display(1)

    def show_redo_history(self) -> list[str]:
        return self.__history.display(2)


def main() -> None:
    manager = TextEditorStateManager()

    while True:
        try:
            print("\n--- Undo/Redo State Management System ---")
            print("1. Type Text")
            print("2. Undo")
            print("3. Redo")
            print("4. Show Current Text")
            print("5. Show Undo History")
            print("6. Show Redo History")
            print("7. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                text = input("Enter text to append: ")
                manager.type_text(text)
                print("Text added successfully.")
                print("Current Text:", manager.get_current_text())

            elif choice == "2":
                updated_text = manager.undo()
                print("Undo successful.")
                print("Current Text:", updated_text)

            elif choice == "3":
                updated_text = manager.redo()
                print("Redo successful.")
                print("Current Text:", updated_text)

            elif choice == "4":
                print("Current Text:", manager.get_current_text())

            elif choice == "5":
                print("Undo History:", manager.show_undo_history())

            elif choice == "6":
                print("Redo History:", manager.show_redo_history())

            elif choice == "7":
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Please select a valid option.")

        except StackError as error:
            print("Stack Error:", error)
        except ValueError as error:
            print("Input Error:", error)


if __name__ == "__main__":
    main()