from abstract import Stack

def base_convert(num, base):
	digits = '0123456789ABCDEF'

	s = Stack()
	
	while num > 0:
		rem = num % base
		s.push(rem)
		num = num // base

	binary_num_str = ''	
	while not s.isEmpty():
		binary_num_str += digits[s.pop()]

	return binary_num_str

print (base_convert(26, 26))