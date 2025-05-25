class RegexParser:
    @staticmethod
    def insert(regex: str) -> str:
        result = []
        for i, c in enumerate(regex):
            result.append(c)
            if i < len(regex) - 1:
                next_char = regex[i + 1]

                if (c.isalnum() and next_char.isalnum()) or \
                        (c == ')' and next_char == '(') or \
                        (c in {'*', '+'} and (next_char == '(' or next_char.isalnum())):
                    result.append('.')
        return ''.join(result)

    @staticmethod
    def to_postfix(regex: str) -> str:
        """Convert infix regex to postfix notation"""
        precedence = {'*': 4, '+': 4, '?': 4, '.': 3, '|': 2}
        output = []
        stack = []

        i = 0
        while i < len(regex):
            c = regex[i]

            if c.isalnum():
                output.append(c)
            elif c == '(':
                stack.append(c)
            elif c == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Mismatched parentheses")
                stack.pop()
            elif c in precedence:
                while (stack and stack[-1] != '(' and
                       precedence.get(stack[-1], 0) >= precedence[c]):
                    output.append(stack.pop())
                stack.append(c)
            i += 1

        while stack:
            if stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(stack.pop())

        return ''.join(output)