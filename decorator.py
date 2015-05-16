def p_decorate(func):
	def wrapper(name):
		return "WRAPPED!!! {0}".format(func(name))
	return wrapper

@p_decorate
def get_text(name):
	return "Hello {0}".format(name)

## p_decorate returns the wrapper() function for us to use
## t = p_decorate(get_text)

print (get_text("Jason"))
