def add(a, b):
    return a + b

def safe_float_input(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Ошибка, нужно ввести число")

if __name__ == "__main__":
    x = safe_float_input("Введите первое число: ")
    y = safe_float_input("Введите второе число: ")
    print("Результат:", add(x, y))
