from . import calc

def main() -> None:
    """
        Является точкой входа в приложение
        :return: Данная функция ничего не возвращает
    """
    expr = input("Введите выражение: ")
    try:
        print("Результат:", calc.shunting_yard(expr))
    except calc.CalcError as e:
        print(e)
    except ZeroDivisionError:
        print("Ошибка: Деление на ноль!")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()
