""" Returns the sum of all the even numbers in the Fibonacci sequence up to 4,000,000"""
def fib():
    current = 1
    previous = 0
    evens = []
    while current < 4000000:
        if current % 2 == 0:
            evens.append(current)
        next = current + previous
        current, previous = next, current

    return sum(evens)

print fib()