class RegexParser:
    @staticmethod
    @staticmethod
    def insert(regex: str) -> str:
        result = []
        for i, c in enumerate(regex):
            result.append(c)
            if i < len(regex) - 1:
                next_char = regex[i + 1]
                # حالات إدراج . بين الرموز
                if (c.isalnum() and next_char.isalnum()) or \
                        (c == ')' and next_char == '(') or \
                        (c in {'*', '+'} and next_char == '(') or \
                        (c in {'*', '+'} and next_char.isalnum()):
                    result.append('.')
        return ''.join(result)

    @staticmethod
    def to_postfix(regex: str) -> str:
        precedence = {'*': 4, '+': 4, '?': 4, '.': 3, '|': 2}
        output = []
        stack = []

        for c in regex:
            if c.isalnum():  # الحروف والأرقام فقط
                output.append(c)
            elif c == '(':
                stack.append(c)
            elif c == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # إزالة '('
            elif c in precedence:  # المشغلين (*, +, ., |)
                while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[c]:
                    output.append(stack.pop())
                stack.append(c)

        while stack:
            output.append(stack.pop())

        return ''.join(output)