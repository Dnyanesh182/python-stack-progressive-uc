# UC10 - Solve Advanced Stack Problems with Testing and Performance Analysis

from typing import Generic, TypeVar, Optional, Any
import time

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

    def __init__(self, initial_capacity: int = 10, max_capacity: Optional[int] = None, allow_none: bool = False) -> None:
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


class StackAlgorithms:
    """
    Advanced stack problems:
    - Next Greater Element
    - Stock Span
    - Largest Rectangle in Histogram
    """

    def next_greater_element(self, numbers: list[int]) -> list[int]:
        result = [-1] * len(numbers)
        stack = MultiStack[int](initial_capacity=max(10, len(numbers)))

        for index in range(len(numbers) - 1, -1, -1):
            while not stack.is_empty(1) and stack.peek(1) <= numbers[index]:
                stack.pop(1)

            if not stack.is_empty(1):
                result[index] = stack.peek(1)

            stack.push(1, numbers[index])

        return result

    def stock_span(self, prices: list[int]) -> list[int]:
        span = [0] * len(prices)
        stack = MultiStack[int](initial_capacity=max(10, len(prices)))

        for index in range(len(prices)):
            while not stack.is_empty(1) and prices[stack.peek(1)] <= prices[index]:
                stack.pop(1)

            span[index] = index + 1 if stack.is_empty(1) else index - stack.peek(1)
            stack.push(1, index)

        return span

    def largest_rectangle_area(self, heights: list[int]) -> int:
        max_area = 0
        stack = MultiStack[int](initial_capacity=max(10, len(heights)))
        index = 0

        while index < len(heights):
            if stack.is_empty(1) or heights[stack.peek(1)] <= heights[index]:
                stack.push(1, index)
                index += 1
            else:
                top_index = stack.pop(1)
                width = index if stack.is_empty(1) else index - stack.peek(1) - 1
                area = heights[top_index] * width
                max_area = max(max_area, area)

        while not stack.is_empty(1):
            top_index = stack.pop(1)
            width = index if stack.is_empty(1) else index - stack.peek(1) - 1
            area = heights[top_index] * width
            max_area = max(max_area, area)

        return max_area


class StackTester:
    """
    Simple unit testing and performance analysis for advanced stack problems.
    """

    def __init__(self) -> None:
        self.algorithms = StackAlgorithms()

    def run_unit_tests(self) -> None:
        print("\n--- Running Unit Tests ---")

        nge_input = [4, 5, 2, 10, 8]
        nge_expected = [5, 10, 10, -1, -1]
        nge_result = self.algorithms.next_greater_element(nge_input)
        print("Next Greater Element Test:", "PASSED" if nge_result == nge_expected else "FAILED")

        span_input = [100, 80, 60, 70, 60, 75, 85]
        span_expected = [1, 1, 1, 2, 1, 4, 6]
        span_result = self.algorithms.stock_span(span_input)
        print("Stock Span Test:", "PASSED" if span_result == span_expected else "FAILED")

        histogram_input = [6, 2, 5, 4, 5, 1, 6]
        histogram_expected = 12
        histogram_result = self.algorithms.largest_rectangle_area(histogram_input)
        print("Largest Rectangle Test:", "PASSED" if histogram_result == histogram_expected else "FAILED")

    def run_performance_analysis(self) -> None:
        print("\n--- Performance Analysis ---")

        large_data = list(range(1, 5001))

        start_time = time.perf_counter()
        self.algorithms.next_greater_element(large_data)
        end_time = time.perf_counter()
        print(f"Next Greater Element Execution Time: {end_time - start_time:.6f} seconds | Time Complexity: O(n)")

        start_time = time.perf_counter()
        self.algorithms.stock_span(large_data)
        end_time = time.perf_counter()
        print(f"Stock Span Execution Time: {end_time - start_time:.6f} seconds | Time Complexity: O(n)")

        start_time = time.perf_counter()
        self.algorithms.largest_rectangle_area(large_data)
        end_time = time.perf_counter()
        print(f"Largest Rectangle Execution Time: {end_time - start_time:.6f} seconds | Time Complexity: O(n)")


def parse_integer_list(user_input: str) -> list[int]:
    cleaned = user_input.strip()
    if not cleaned:
        raise ValueError("Input cannot be empty.")

    return [int(value) for value in cleaned.split()]


def main() -> None:
    algorithms = StackAlgorithms()
    tester = StackTester()

    while True:
        try:
            print("\n--- Advanced Stack Problems ---")
            print("1. Next Greater Element")
            print("2. Stock Span Problem")
            print("3. Largest Rectangle in Histogram")
            print("4. Run Unit Tests")
            print("5. Run Performance Analysis")
            print("6. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                numbers = parse_integer_list(input("Enter integers separated by space: "))
                result = algorithms.next_greater_element(numbers)
                print("Input:", numbers)
                print("Next Greater Elements:", result)

            elif choice == "2":
                prices = parse_integer_list(input("Enter stock prices separated by space: "))
                result = algorithms.stock_span(prices)
                print("Input:", prices)
                print("Stock Span:", result)

            elif choice == "3":
                heights = parse_integer_list(input("Enter histogram heights separated by space: "))
                result = algorithms.largest_rectangle_area(heights)
                print("Input:", heights)
                print("Largest Rectangle Area:", result)

            elif choice == "4":
                tester.run_unit_tests()

            elif choice == "5":
                tester.run_performance_analysis()

            elif choice == "6":
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