from app import add

def test_add_negative():
    assert add(-5, -3) == -8

def test_add_zero():
    assert add(0, 10) == 10

def test_add_big_numbers():
    assert add(1000000, 2000000) == 3000000
