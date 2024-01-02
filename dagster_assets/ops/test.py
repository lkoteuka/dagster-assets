from os import path, pardir

print(path.join(path.join(path.dirname(__file__), pardir), pardir))
