from parser.cal.exp import Exp
from operator import mul
from functools import reduce


def calc_apply(operator, args):
    """ 按操作符名称对参数列表进行计算

    >>> calc_apply('+', [1, 2, 3])
    6
    >>> calc_apply('-', [10, 1, 2, 3])
    4
    >>> calc_apply('*', [])
    1
    >>> calc_apply('/', [40, 5])
    8.0

    :param operator: string, 操作符名称
    :param args: list of int or float
    :return: int or float, 计算结果
    """
    if operator in ('add', '+'):
        return sum(args)
    if operator in ('sub', '-'):
        if len(args) == 0:
            raise TypeError(operator + ' requires at least 1 argument')
        if len(args) == 1:
            return -args[0]
        return sum(args[:1] + [-arg for arg in args[1:]])
    if operator in ('mul', '*'):
        return reduce(mul, args, 1)
    if operator in ('div', '/'):
        if len(args) != 2:
            raise TypeError(operator + ' requires exactly 2 arguments')
        numer, denom = args
        return numer / denom


def calc_eval(exp):
    """ 对表达式进行求值

    >>> calc_eval(Exp('add', [1, 2]))
    3
    >>> type(calc_eval(Exp('+', [1, 2])))
    <class 'int'>
    >>> calc_eval(Exp('mul', [2, Exp('sub', [4])]))
    -8
    >>> calc_eval(Exp('mul', [2, Exp('sub', [4, 3])]))
    2
    >>> calc_eval(Exp('div', [2, Exp('sub', [4, 3])]))
    2.0

    :param exp: 表达式, 数值和调用表达式的组合
    :return: int or float, 表达式的值
    """
    if type(exp) in (int, float):
        return exp
    elif type(exp) == Exp:
        arguments = list(map(calc_eval, exp.operands))
        return calc_apply(exp.operator, arguments)


def tokenize(line):
    """词法分析

    >>> tokenize('add(2, mul(4, 6))')
    ['add', '(', '2', ',', 'mul', '(', '4', ',', '6', ')', ')']
    """
    spaced = line.replace('(', ' ( ').replace(')', ' ) ').replace(',', ' , ')
    return spaced.split()


def token_analyze(token):
    """解析单个 token, 转换为数字, 或者原样返回

    >>> token_analyze('1')
    1
    >>> token_analyze('-1.0')
    -1.0
    >>> token_analyze('+1.01')
    1.01
    >>> token_analyze('xxx')
    'xxx'
    """
    try:
        return int(token)
    except (TypeError, ValueError):
        try:
            return float(token)
        except (TypeError, ValueError):
            return token


def assert_non_empty(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected end of line')


def analyze_operands(tokens):
    """递归处理逗号分割的 token 列表

    """
    assert_non_empty(tokens)
    operands = []
    while tokens[0] != ')':
        if operands and tokens.pop(0) != ',':
            # 按递归条件分析，operands 不为空的情况，只有处理 add(1, 2) 中的 ',' 时才会发生
            raise SyntaxError('expected ,')
        operands.append(analyze(tokens))
        assert_non_empty(tokens)
    tokens.pop(0)  # 丢弃最后的 ')'
    return operands


known_operators = ['add', 'sub', 'mul', 'div', '+', '-', '*', '/']


def analyze(tokens):
    """语法分析, 非纯函数, 递归消耗 tokens

    >>> expression = 'add(2, mul(4, 6))'
    >>> analyze(tokenize(expression))
    Exp('add', [2, Exp('mul', [4, 6])])
    >>> str(analyze(tokenize(expression)))
    'add(2, mul(4, 6))'

    :param tokens: list of string, 词法分析产生的词元列表
    :return: tree of Exp
    """
    assert_non_empty(tokens)
    token = token_analyze(tokens.pop(0))
    if type(token) in (int, float):
        return token
    if token in known_operators:
        if len(tokens) == 0 or tokens.pop(0) != '(':  # 丢弃操作符后面的 '('
            raise SyntaxError('expected ( after ' + token)
        return Exp(token, analyze_operands(tokens))
    else:
        raise SyntaxError('unexpected ' + token)


def calc_parse(line):
    """解析表达式文本，返回 AST(此处为表达式树)

    :param line: string, 表达式字符串
    :return: list of Exp
    """
    tokens = tokenize(line)
    expression_tree = analyze(tokens)
    if len(tokens) > 0:
        raise SyntaxError('Extra tokens(s): ' + ' '.join(tokens))
    return expression_tree


def read_eval_print_loop() -> None:
    """ 运行 REPL(read-eval-print loop) 来从命令行获取表达式并计算 """
    while True:
        try:
            expression_tree = calc_parse(input('calc> '))
            print(calc_eval(expression_tree))
        except (SyntaxError, TypeError, ZeroDivisionError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):  # <control>-D, etc.
            print('计算结束')
            return


if __name__ == '__main__':
    from doctest import run_docstring_examples
    run_docstring_examples(calc_apply, globals())
    run_docstring_examples(calc_eval, globals())
    run_docstring_examples(token_analyze, globals())
    run_docstring_examples(tokenize, globals())
    run_docstring_examples(analyze, globals())
    read_eval_print_loop()
