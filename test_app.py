from app import add, safe_float_input

def test_add_basic():
    assert add(2, 3) == 5
    assert add(-5, 10) == 5
    assert add(0.5, 0.5) == 1

def test_safe_input(monkeypatch):
    inputs = iter(["abc", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = safe_float_input("Введите число")
    assert result == 5
