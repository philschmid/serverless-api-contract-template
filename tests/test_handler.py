from src import handler

test_event = {"body": "test"}


def test_handler():
    res = handler.handler("", "")
    assert isinstance(res, dict)
    res = handler.handler(test_event, "")
    assert res == test_event["body"]
