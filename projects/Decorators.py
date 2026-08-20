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


data = {"name": "John", "age": 25, "email": "john@example.com", "password": "1234"}


reserved_keys = {"name", "password"}


extra_kwargs = {}

for k, v in data.items():

    if k not in reserved_keys:
        extra_kwargs[k] = v
print("Extra kwargs:", extra_kwargs)


extra_kwargs_comprehension = {k: v for k, v in data.items() if k not in reserved_keys}
print("Extra kwargs comprehension:", extra_kwargs_comprehension)

k = "city"
v = "dhaka"

city_dict = {k: v}
print("City dict:", city_dict)

numbers = [1, 2, 3, 4, 5, 6]

sqaured_numbers = [a * a for a in numbers]

even_numbers = [a for a in numbers if a % 2 == 0]

print("even numbers", even_numbers)

names = ["john", "alice", "bob", "sarah"]

uppercase_names = [s.upper() for s in names]

print(uppercase_names)

main_names = ["John", "Alexander", "Bob", "Christopher", "Sam"]

long_names = [a for a in main_names if len(a) >= 5]

print(long_names)

new_names = names = ["Alice", "Bob", "Charlie"]

dict_name = {k: len(k) for k in names}

print("dict names", dict_name)


scores = {"Alice": 85, "Bob": 45, "Charlie": 92, "David": 60}

filltered_scores = {k: v for k, v in scores.items() if v >= 70}

print(filltered_scores)

prices = {"apple": 100, "banana": 50, "orange": 80}


def add_percentage(price: float, percentage: float) -> float:
    return price + (price * percentage / 100)


test = add_percentage(100, 10)


after_tax_prices = {k: add_percentage(v, 10) for k, v in prices.items()}

print(after_tax_prices)


array_numbers = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

flattened = [num for row in array_numbers for num in row]


users = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 17},
    {"name": "Charlie", "age": 30},
    {"name": "David", "age": 15},
]

uppercase_users = [user["name"].upper() for user in users if user["age"] >= 18]


print(uppercase_users)
