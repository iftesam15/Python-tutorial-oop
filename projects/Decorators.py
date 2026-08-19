def my_decorator(func):
    def wrapper():
        print("something happening in the function before it runs")
        func()
        print("Something is happening after the function runs")

    return wrapper


@my_decorator
def hello():
    print("Hello, World!")


hello()


# Decorators with arguments


def add_greeting(func):
    def wrapper(*args, **kwargs):
        print("Hello!")
        result = func(*args, **kwargs)
        print("Goodbye!")
        return result

    return wrapper


@add_greeting
def greet(name):
    return f"Hello, {name}!"


print(greet("John"))


user = {"name": "John", "age": 30, "email": "john@example.com"}


print(user.get("name"))
print(user.get("address", "Not provided"))


def get_user_info(user):
    return f"Name: {user.get('address','No address found')}, Age: {user['age']}, Email: {user['email']}"


print(get_user_info(user))
