
import csv
import re
""" Quick script to read a csv and break up the address into a more desirable formnat with the street adress separated from the city, state, zip cell"""

FILE = "addresses.csv"

def parse_csv(raw_file, delimiter):
	opened_file = open(raw_file)
	csv_data = csv.reader(opened_file, delimiter=delimiter)
	address_book = []

	# Skip the first line (fields).
	csv_data.next() 
	for row in csv_data:
		desired_format = {}
		desired_format['name'] = row[0]
		current_address = row[1]

		# For each city in the list, search through and see if employee's City is there.
		# If so, split the item before City and add the elements to our address book.
		for c in get_city_list():
			city = re.compile(c)
			city_in_address = city.search(current_address)
			if city_in_address is not None:
				i = city_in_address.start()
				desired_format['address'] = current_address[0:i]
				desired_format['city_state_zip'] = current_address[i:]
		
		address_book.append(desired_format)

	opened_file.close()

	return address_book

def create_csv(address_book):
	with open('newfile.csv', 'wb') as csvfile:
		fields = ['name', 'address', 'city_state_zip']
		fieldwriter = csv.writer(csvfile, dialect='excel')
		spamwriter = csv.DictWriter(csvfile, fieldnames=fields)
		
		fieldwriter.writerow(fields)

		for employee in address_book:
			spamwriter.writerow(employee)


def get_city_list():
	"""Quick function to generate a list of the CA cities."""
	cities = []
	opened_file = open("cities.csv")
	csv_data = csv.reader(opened_file, delimiter=",")

	for row in csv_data:
		# Add on ", CA" to the city so there won't be false matches when an employee
		# has a street name that is also a city name
		cities.append(row[0] + ", CA")

	return cities				

def main():
	address_book = parse_csv(FILE, ",")

	return create_csv(address_book)

if __name__ == "__main__":
	main()	





