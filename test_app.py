from app import add

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-5, -3) == -8

def test_add_mixed():
    assert add(-5, 10) == 5

def test_add_zero_left():
    assert add(0, 7) == 7

def test_add_zero_right():
    assert add(9, 0) == 9

def test_add_float():
    assert add(2.5, 3.1) == 5.6

def test_add_big_numbers():
    assert add(1_000_000, 2_000_000) == 3_000_000

def test_add_precision():
    result = add(0.1, 0.2)
    assert round(result, 1) == 0.3