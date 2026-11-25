from app.core.config import get_bool_env


def test_boolean_true(monkeypatch):

    monkeypatch.setenv("TEST_DEBUG", "true")

    assert get_bool_env("TEST_DEBUG") is True


def test_boolean_false(monkeypatch):

    monkeypatch.setenv("TEST_DEBUG", "false")

    assert get_bool_env("TEST_DEBUG") is False


def test_boolean_default(monkeypatch):

    monkeypatch.delenv("TEST_DEBUG", raising=False)

    assert get_bool_env("TEST_DEBUG", True) is True