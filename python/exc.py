import sys

try:
    x = int(input("X: "))
    y= int(input("Y: "))
except ValueError:
    print("Invalid Input")
    sys.exit(1)

try:
    result = x / y
except ZeroDivisionError:
    print("Can't divide by 0")
    sys.exit(1)

print(f"{x} / {y} = {result}")
