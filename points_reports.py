""" Creates an Excel report for each department """

import csv
from datetime import date
import xlsxwriter


def parse_csv(raw_file, delimiter):
	opened_file = open(raw_file)
	csv_data = csv.reader(opened_file, delimiter=delimiter)
	parsed = []
	# Set 'fields' to the headers in the csv
	fields = csv_data.next() 
	
	# Skip irrelevant employees
	for row in csv_data:
		if row[1] == "term'd" or row[5] == "Exempt":
			continue

		# Each employee will be represented as a dictionary with the key being the appropriate header.
		# For example {'Name': 'Jason Majors', 'Title': 'HR Specialist'}

		parsed.append(dict(zip(fields, row)))

	opened_file.close()

	return parsed	
		
def filter_data(parsed_csv, dept, disciplines):
	# Returns a list containing lists of employee dictionaries grouped by the discipline value
	data = []
	for discipline in disciplines:
		group = []
		for i in parsed_csv:
			if i['Dept'] in dept and i['Discipline'] == discipline:
				group.append(i)

		data.append(group)

	return data	
	

def create_excel(data, filename):
	for d in data:
		for i in d:
			# Don't need these in the report.
			del i['Status']
			del i['FLSA Status']

	workbook = xlsxwriter.Workbook('{0}.xlsx'.format(filename))
	worksheet = workbook.add_worksheet()
	# Set column sizes.
	worksheet.set_column(1, 3, 25)
	worksheet.set_column(5, 5, 25)

	bold = workbook.add_format({'bold': True})
	fields = ['ID', 'Last, First', 'Dept', 'Title', 'Points', 'Discipline']
	
	row = 0

	for group in data:
		if len(group) > 0:
			col = 0
			for header in fields:
				worksheet.write(row, col, header, bold)
				col += 1
			row +=1

			for i in group:
				col = 0
				idnum = int(i['ID'])
				name = i['Last, First']
				dept = i['Dept']
				title = i['Title']
				points = int(i['Points'])
				discipline = i['Discipline']

				worksheet.write_number(row, col, idnum)
				worksheet.write(row, col + 1, name)
				worksheet.write(row, col + 2, dept)
				worksheet.write(row, col + 3, title)
				worksheet.write_number(row, col + 4, points)
				worksheet.write(row, col + 5, discipline)
				# New row for each employee.
				row +=1
			# Create empty row after each disciplinary group.
			row+=1
				
	workbook.close()


def main():
	FILE = "Points Report Master.csv"
	disciplines = ["Coach and Counselling", 
					"Written Warning Due", 
					"Final Warning Due", 
					"Discharge Due",
					]

	# Each list will get 1 report but for practical reasons some departments need to go together.
	# For example 'Casino Floor' and 'California Game' are separated departments in the HRIS but for reporting purposes
	# they can all be grouped under "Casino Floor".
	departments = [['Food & Beverage', 'Beverage', 'Food'],
					['Concierge'],
					['Cage'],
					['Card Control'],
					['Casino Floor', 'California Game', 'Poker', 'Pai Gow Tiles'],
				]

	parsed = parse_csv(FILE, ",")

	today = date.today().isoformat()

	for dept in departments:
		filename = dept[0] + ' ' + today
		data = filter_data(parsed, dept, disciplines)
		create_excel(data, filename)

main();