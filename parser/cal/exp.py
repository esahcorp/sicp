class Exp(object):
    """ Calculator 的调用表达式

    >>> Exp('add', [1, 2])
    Exp('add', [1, 2])
    >>> str(Exp('add', [1, 2]))
    'add(1, 2)'
    >>> Exp('add', [1, Exp('mul', [2, 3, 4])])
    Exp('add', [1, Exp('mul', [2, 3, 4])])
    >>> str(Exp('add', [1, Exp('mul', [2, 3, 4])]))
    'add(1, mul(2, 3, 4))'
    """

    def __init__(self, operator, operands) -> None:
        self.operator = operator
        self.operands = operands

    def __repr__(self) -> str:
        return 'Exp({0}, {1})'.format(repr(self.operator), repr(self.operands))

    def __str__(self) -> str:
        operand_str = ', '.join(map(str, self.operands))
        return '{0}({1})'.format(self.operator, operand_str)


if __name__ == '__main__':
    from doctest import run_docstring_examples
    run_docstring_examples(Exp, globals())
