class RegexParser:
    @staticmethod
    def insert(regex: str) -> str:
        result = []
        for i, c in enumerate(regex):
            result.append(c)
            if i < len(regex) - 1:
                next_char = regex[i + 1]
                if (c.isalnum() or c in ')*}+') and (next_char.isalnum() or next_char in '({[') and c != '+':
                    result.append('.')
        return ''.join(result)

    @staticmethod
    def to_postfix(regex: str) -> str:
        """Convert infix regex to postfix using Shunting Yard algorithm."""
        precedence = {'*': 4, '+': 4, '?': 4, '.': 3, '|': 2}  # Added + with same precedence as *
        output = []
        stack = []

        for c in regex:
            if c.isalnum() or c in {'+', '-', '/', '[', ']', '{', '}'}:
                output.append(c)
            elif c == '(':
                stack.append(c)
            elif c == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # Remove '(' from stack
            elif c in precedence:
                while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[c]:
                    output.append(stack.pop())
                stack.append(c)

        while stack:
            output.append(stack.pop())

        return ''.join(output)