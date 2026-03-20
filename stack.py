# UC7 - Build Expression Evaluation System

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


class ExpressionEngine:
    """
    Validates infix expressions, converts them to postfix and prefix,
    and evaluates postfix and prefix expressions.
    """

    def __init__(self) -> None:
        self.__operators = {'+', '-', '*', '/', '^'}
        self.__precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '^': 3
        }

    def __is_operator(self, char: str) -> bool:
        return char in self.__operators

    def __is_operand(self, char: str) -> bool:
        return char.isalnum()

    def __is_numeric_operand(self, char: str) -> bool:
        return char.isdigit()

    def __precedence_of(self, operator: str) -> int:
        return self.__precedence.get(operator, 0)

    def __is_right_associative(self, operator: str) -> bool:
        return operator == '^'

    def __has_higher_precedence(self, top_operator: str, current_operator: str) -> bool:
        top_precedence = self.__precedence_of(top_operator)
        current_precedence = self.__precedence_of(current_operator)

        if top_precedence > current_precedence:
            return True

        if top_precedence == current_precedence and not self.__is_right_associative(current_operator):
            return True

        return False

    def __remove_spaces(self, expression: str) -> str:
        return "".join(expression.split())

    def __apply_operator(self, left: float, right: float, operator: str) -> float:
        if operator == '+':
            return left + right
        if operator == '-':
            return left - right
        if operator == '*':
            return left * right
        if operator == '/':
            if right == 0:
                raise ValueError("Division by zero is not allowed.")
            return left / right
        if operator == '^':
            return left ** right
        raise ValueError(f"Unsupported operator: {operator}")

    def validate_symbols(self, expression: str) -> tuple[bool, str]:
        stack = MultiStack[str](initial_capacity=max(4, len(expression)))

        pairs = {
            ')': '(',
            '}': '{',
            ']': '['
        }

        for index, char in enumerate(expression):
            if char in "({[":
                stack.push(1, char)
            elif char in ")}]":
                if stack.is_empty(1):
                    return False, f"Unmatched closing bracket '{char}' at position {index}."

                top_symbol = stack.pop(1)
                if top_symbol != pairs[char]:
                    return False, (
                        f"Mismatched bracket at position {index}: "
                        f"expected matching for '{top_symbol}', found '{char}'."
                    )

        if not stack.is_empty(1):
            return False, "Unmatched opening bracket(s) found in expression."

        return True, "Expression is balanced."

    def infix_to_postfix(self, expression: str) -> str:
        expression = self.__remove_spaces(expression)
        operator_stack = MultiStack[str](initial_capacity=max(4, len(expression)))
        postfix: list[str] = []

        for char in expression:
            if self.__is_operand(char):
                postfix.append(char)

            elif char == '(':
                operator_stack.push(1, char)

            elif char == ')':
                while not operator_stack.is_empty(1) and operator_stack.peek(1) != '(':
                    postfix.append(operator_stack.pop(1))

                if operator_stack.is_empty(1):
                    raise ValueError("Invalid expression: unmatched closing parenthesis.")
                operator_stack.pop(1)

            elif self.__is_operator(char):
                while (
                    not operator_stack.is_empty(1)
                    and operator_stack.peek(1) != '('
                    and self.__has_higher_precedence(operator_stack.peek(1), char)
                ):
                    postfix.append(operator_stack.pop(1))

                operator_stack.push(1, char)

            else:
                raise ValueError(f"Invalid character found in expression: '{char}'")

        while not operator_stack.is_empty(1):
            top = operator_stack.pop(1)
            if top == '(':
                raise ValueError("Invalid expression: unmatched opening parenthesis.")
            postfix.append(top)

        return "".join(postfix)

    def infix_to_prefix(self, expression: str) -> str:
        expression = self.__remove_spaces(expression)

        reversed_expression = ""
        for char in expression[::-1]:
            if char == '(':
                reversed_expression += ')'
            elif char == ')':
                reversed_expression += '('
            else:
                reversed_expression += char

        postfix_of_reversed = self.infix_to_postfix(reversed_expression)
        prefix = postfix_of_reversed[::-1]
        return prefix

    def evaluate_postfix(self, expression: str) -> float:
        expression = self.__remove_spaces(expression)
        value_stack = MultiStack[float](initial_capacity=max(4, len(expression)))

        for char in expression:
            if self.__is_numeric_operand(char):
                value_stack.push(1, float(char))

            elif self.__is_operator(char):
                if value_stack.size(1) < 2:
                    raise ValueError("Invalid postfix expression: insufficient operands.")

                right = value_stack.pop(1)
                left = value_stack.pop(1)
                result = self.__apply_operator(left, right, char)
                value_stack.push(1, result)

            else:
                raise ValueError(f"Invalid character in postfix expression: '{char}'")

        if value_stack.size(1) != 1:
            raise ValueError("Invalid postfix expression: too many operands or operators.")

        return value_stack.pop(1)

    def evaluate_prefix(self, expression: str) -> float:
        expression = self.__remove_spaces(expression)
        value_stack = MultiStack[float](initial_capacity=max(4, len(expression)))

        for char in expression[::-1]:
            if self.__is_numeric_operand(char):
                value_stack.push(1, float(char))

            elif self.__is_operator(char):
                if value_stack.size(1) < 2:
                    raise ValueError("Invalid prefix expression: insufficient operands.")

                left = value_stack.pop(1)
                right = value_stack.pop(1)
                result = self.__apply_operator(left, right, char)
                value_stack.push(1, result)

            else:
                raise ValueError(f"Invalid character in prefix expression: '{char}'")

        if value_stack.size(1) != 1:
            raise ValueError("Invalid prefix expression: too many operands or operators.")

        return value_stack.pop(1)


def main() -> None:
    try:
        expression = input("Enter an infix expression using single-digit numbers: ").strip()

        if not expression:
            print("Input Error: Expression cannot be empty.")
            return

        engine = ExpressionEngine()

        is_valid, message = engine.validate_symbols(expression)
        if not is_valid:
            print("\nExpression:", expression)
            print("Validation Result:", is_valid)
            print("Message:", message)
            return

        postfix = engine.infix_to_postfix(expression)
        prefix = engine.infix_to_prefix(expression)

        postfix_result = engine.evaluate_postfix(postfix)
        prefix_result = engine.evaluate_prefix(prefix)

        print("\nExpression:", expression)
        print("Validation Result:", is_valid)
        print("Message:", message)
        print("Postfix Expression:", postfix)
        print("Prefix Expression:", prefix)
        print("Postfix Evaluation Result:", postfix_result)
        print("Prefix Evaluation Result:", prefix_result)

    except ValueError as error:
        print("Input Error:", error)
    except StackError as error:
        print("Stack Error:", error)


if __name__ == "__main__":
    main()