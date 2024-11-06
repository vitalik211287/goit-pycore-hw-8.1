def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)  # Повертаємо текст помилки користувачеві
        except IndexError:
            return "Give me name and phone, please."
        except KeyError:
            return "This contact does not exist."
    return inner