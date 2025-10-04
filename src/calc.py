import re
import operator


class CalcError(Exception):
    pass

def tokenize(expr: str) -> list:
    """
        Разбивает строку инфиксного выражения на список токенов
        Обрабатывает числа и операторы

        :param expr: Строка, в которой записано выражение в инфиксной записи
        :return: Возвращает список токенов этой строки
        :raises CalcError: Если выражение пустое, содержит неизвестный токен
        или имеет недопустимое расположение унарных операторов.
    """
    TOKEN_RE = re.compile(r"(\d+(?:\.\d+)?|\*\*|//|/|\*|%|\(|\)|\+|\-)")
    expr = expr.replace(" ", "")
    lst_tokens = re.findall(TOKEN_RE, expr)

    # Проверка на пустую строку
    if len(expr) == 0:
        raise CalcError("Ошибка: Пустое выражение.")

    # Проверка на неизвестный(неправильный) токен
    expr_not_recognize = "".join(lst_tokens)
    if expr_not_recognize != expr:
        wrong_char = re.compile(r"[^\d\.\*\/\%\+\-\(\)]")
        if wrong_char.search(expr):
            raise CalcError("Ошибка: Неизвестный токен.")

    # Проверка на неправильную последовательность идущих подряд знаков
    for i in range(len(lst_tokens) - 2):
        if lst_tokens[i] in ('+', '-') and lst_tokens[i + 1] in ('+', '-') and lst_tokens[i + 2] in ('+', '-'):
            raise CalcError("Ошибка: Недопустимая последовательность идущих подряд унарных/простых операторов.")



    # Работа с унарными знаками
    processed_tokens = []
    i = 0
    while i < len(lst_tokens):
        token = lst_tokens[i]

        # Нахождение унарного символа
        unary_context = (i == 0 or
                         lst_tokens[i - 1] in ['(', '*', '/', '//', '%', '**'])

        if token in ('+', '-'):
            if unary_context:
                if token == '-':
                    processed_tokens.append("~")
                i += 1
                continue

            if i > 0 and lst_tokens[i - 1] in ['+', '-']:
                raise CalcError(
                    f"Ошибка: Унарный оператор '{token}' не " +
                    f"может следовать за '{lst_tokens[i - 1]}'." +
                    " Используйте скобки.")

        processed_tokens.append(token)
        i += 1

    return processed_tokens



def to_rpn(tokens: list) -> list:
    """
    Преобразует список токенов инфиксной записи в обратную польскую запись (ОПЗ)

    :param tokens: Список токенов инфиксного выражения.
    :return: Список токенов в обратной польской записи.
    :raises CalcError: Если обнаружены несбалансированные скобки.
    """
    precedence = {
        "~": 4,
        '**': 3,
        '*': 2, '/': 2, '//': 2, '%': 2,
        '+': 1, '-': 1,
    }

    output = []
    stack_for_RPN = []

    for token in tokens:
        try:
            float(token)
            output.append(token)

        except ValueError:
            if token == '(':
                stack_for_RPN.append(token)
            elif token == ')':
                while stack_for_RPN and stack_for_RPN[-1] != '(':
                    output.append(stack_for_RPN.pop())
                if not stack_for_RPN or stack_for_RPN[-1] != '(':
                    raise CalcError("Ошибка: Несбалансированные скобки.")
                stack_for_RPN.pop()
            elif token in precedence:
                while (stack_for_RPN and stack_for_RPN[-1] != '(' and
                       (precedence[stack_for_RPN[-1]] > precedence[token] or
                        (precedence[stack_for_RPN[-1]] == precedence[token] and stack_for_RPN[-1] != '**'))):
                    output.append(stack_for_RPN.pop())
                stack_for_RPN.append(token)

    while stack_for_RPN:
        op = stack_for_RPN.pop()
        if op == '(':
            raise CalcError("Ошибка: Несбалансированные скобки.")
        output.append(op)

    return output







def shunting_yard(expr: str) -> float|int:
    """
            Вычисляет результат выражения в обратной польской последовательности

            :param expr: Строка, в которой записано выражение в инфиксной записи
            :return: Возвращает результат вычисления(float|int)
            :raises CalcError: При различных ошибках
            :raises ZeroDivisionError: При делении на ноль.
    """

    tokens = tokenize(expr)
    output = to_rpn(tokens)

    operations = {
        '+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv,
        '**': operator.pow, '//': operator.floordiv, '%': operator.mod,
        "~": lambda a: -a
    }
    stack = []

    for data in output:
        try:
            val = float(data)
            stack.append(val)
        except ValueError:
            if data == "~":
                op1 = stack.pop()
                stack.append(operations[data](op1))  # type: ignore
            elif data in operations:
                if len(stack) < 2:
                    raise CalcError("Ошибка: Недостаточно операндов.")
                op2 = stack.pop()
                op1 = stack.pop()

                if data in ('//', '%'):
                    if not (op1 == int(op1) and op2 == int(op2)):
                        raise CalcError(f"Ошибка: Операторы '{data}' требуют целых чисел.")
                    op1, op2 = int(op1), int(op2)

                if data in ('/', '//', '%') and op2 == 0:
                    raise ZeroDivisionError("Ошибка: Деление на ноль!")

                stack.append(operations[data](op1, op2))  # type: ignore

    if len(stack) != 1:
        raise CalcError("Ошибка: Некорректное выражение.")

    result = stack[0]
    if float(result) != int(result):
        return float(result)
    else:
        return int(result)
