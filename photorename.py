"""A quick script to rename files using a CSV where Column 1 is the current filenames 
and Column 2 is the desired names."""

import os
import csv

FILE = 'barcodes.csv'
PATH = "/home/jason/Projects/Pictures/"

def parse_codes(file, delimiter):
	opened_file = open(FILE)
	csv_data = csv.reader(opened_file, delimiter=delimiter)
	codes = {}

	for row in csv_data:
		codes[row[0]] = row[1]

	return codes	


def rename(codes):
	clipped = []
	pictures = os.listdir(PATH)

	for picture in pictures:
		# Take off the .jpg so they can be matched to the Name column in the CSV
		clipped.append(picture[:-4])

	for picture in clipped:
		for name, code in codes.iteritems():
			if picture == name:
				# Match complete. Put the .jpg tag back on
				old_name = os.path.join(PATH, picture) + '.jpg'
				new_name = os.path.join(PATH, code)
				os.rename(old_name, new_name)
				
def main():
	codes = parse_codes(FILE, ',')
	return rename(codes)

if __name__ == '__main__':
	main()	



