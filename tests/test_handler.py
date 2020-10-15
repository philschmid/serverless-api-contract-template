from src import handler


def test_handler():
    res = handler.handler("", "")
    assert isinstance(res, dict)
