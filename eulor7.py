"""Project Euler Problem #7: Finds the nth prime number"""

from datetime import datetime

## Timing for optimization
start_time = datetime.now()


# Helper function to test if a number is prime
# Could be optimized more
def is_prime(n):
	prime = True
	## Iterate starting at 2 until n-1 checking if n is divisable by i; if n is divisable by i the number is not prime.
	for i in range(2, n):
		if n % i == 0:
			prime = False
			# Found a divisor that's not 1 or n. NOT PRIME!
			break
	# Returns false if not prime.
	return prime

def find_nth_prime(n):
	# Start with 2 as the first prime
	prime_count = 1
	num = 2
	while prime_count < n:
		if (num % 2	 == 0):
			num+=1
			continue

		if is_prime(num):
			prime_count+=1

		if prime_count == n:
			print (num)
			print (datetime.now()- start_time)
			break

		num+=1

find_nth_prime(100)