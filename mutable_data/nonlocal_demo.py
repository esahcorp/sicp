def make_withdraw(balance):
    """Return a withdraw function that draws down balance with each call."""
    def withdraw(amount):
        # nonlocal 表示 balance 绑定在当前局部帧(withdraw)的上层局部帧(make_withdraw)中
        nonlocal balance
        if amount > balance:
            return 'Insufficient funds'
        # 赋值语句默认将变量绑定在当前环境的局部帧(withdraw)中，但是由于 'nonlocal' 的标记，
        # 赋值运算向上寻找到 'balance' 定义位置的第一帧(make_withdraw)，并在那里重新绑定名称
        balance = balance - amount
        return balance
    return withdraw


if __name__ == '__main__':
    # md 的环境局部帧继承自 make_withdraw
    md = make_withdraw(20)
    print(md(5))
    print(md(100))
    print(md(3))
    amt = 100
    # md2 的局部帧同样继承自 make_withdraw 但与 md 不同
    md2 = make_withdraw(amt)
    # 执行第一次 md2 时，'balance' 重新绑定，已经与 'amt' 不同了
    print(md2(100))
    print(amt)
