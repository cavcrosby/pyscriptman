# content of test_indirect_list.py

import pytest


@pytest.fixture(scope="function")
def x(request):
    print(request.param)
    return request.param[0] * 3


@pytest.fixture(scope="function")
def y(request):
    return request.param * 2


@pytest.mark.parametrize("x, y", [((["a", 'c'], "b"))], indirect=["x"])
def test_indirect(x, y):
    assert x == "aaa"
    assert y == "b"