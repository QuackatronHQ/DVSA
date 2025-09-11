
def sum(a, b):
    if not a > 0:
        raise AssertionError
    if not b > 0:
        raise AssertionError
    return eval("a + b")
