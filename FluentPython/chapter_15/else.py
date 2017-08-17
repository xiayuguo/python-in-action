def test_for_else():
    """只有for循环完整执行完成之后, 才会执行else中的内容

    [output]: No element is 5
    """
    for ele in range(5):
        if ele == 5:
            break
    else:
        raise ValueError('No element is 5')


def test_try_else():
    """
    [output]: ok
    [output]: over
    """
    try:
        print("ok")
    except Exception as e:
        print("error")
    else:
        print("over")


def test_try_except_else():
    """只有try块不抛出异常才会执行else中的内容, 此时else相当于then的含义

    [output]: error
    """
    try:
        value = [][0]
        print("ok")
    except IndexError as e:
        print("error")
    else:
        print("over")


if __name__ == "__main__":
    print(test_try_else.__doc__)
    test_try_else()
    print(test_try_except_else.__doc__)
    test_try_except_else()
    print(test_for_else.__doc__)
    test_for_else()
