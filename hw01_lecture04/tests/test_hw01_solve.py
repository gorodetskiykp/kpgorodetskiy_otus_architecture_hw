from hw01_lecture04.main import Solver


def test_no_roots():
    # x ** 2 + 1 = 0
    # a = 1
    # b = 0
    # c = 1
    roots = Solver.solve(a=1, b=0, c=1)
    assert isinstance(roots, list)
    assert len(roots) == 0


def test_two_roots():
    # x ** 2 - 1 = 0
    # a = 1
    # b = 0
    # c = -1
    roots = Solver.solve(a=1, b=0, c=-1)
    assert isinstance(roots, list)
    assert roots == [1, -1]


def test_one_roots():
    # x ** 2 + 2 * x + 1 = 0
    # a = 1
    # b = 2
    # c = 1
    roots = Solver.solve(a=1, b=2, c=1)
    assert isinstance(roots, list)
    assert roots == [-1]