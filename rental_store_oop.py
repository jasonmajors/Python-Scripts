import datetime

class Rental(object):
	def __init__(self, title, id):
		self.rental_length=5 #how many days you can rent the Rental for
		self.checkout_date=None
		self.due_date=None
		self.title = title
		self.id = id


class Store(object):
	def __init__(self):
		self.inventory = []
		self.checked_out = []

	#Method to add Rentals to the store
	def add_rental(self, rental):
		self.inventory.append(rental)

	#Method to check-out rentals.
	def checkout(self, rental, date=None):
		if rental in self.inventory:
			if date is None:
				rental.checkout_date = datetime.datetime.now()
			else:
				rental.checkout_date = datetime.datetime.strptime(date, "%m/%d/%y")

			self.checked_out.append(rental)
			self.inventory.remove(rental)

			rental.due_date = rental.checkout_date + datetime.timedelta(days=rental.rental_length)

		else:
			print ("We're all out of {0} at the moment.\n").format.rental.title	
	
	#a method to show what Rentals are checked out and when they're due back'
	def status(self):
		for rental in self.checked_out:
			if datetime.datetime.now() < rental.due_date:
				print ("%s (RENTAL_ID: %d) is out and due back %d/%d/%d") % (rental.title, rental.id, rental.due_date.month, 
															rental.due_date.day, rental.due_date.year)
	
			elif datetime.datetime.now() > rental.due_date:
					print ("%s is OVERDUE!!") % rental.title

	
def main():
	r1 = Rental('Top Gun', 1)
	r2 = Rental('Lion King', 2)
	r3 = Rental('American History X', 3)
	r4 = Rental('Top Gun', 4)
	store = Store()

	store.add_rental(r1)
	store.add_rental(r2)
	store.add_rental(r3)
	store.add_rental(r4)

	store.checkout(r1)
	store.checkout(r2)
	store.checkout(r3)
	store.checkout(r2)
	store.checkout(r4, '10/5/13')

	store.status()

if __name__ == '__main__':
	main()

