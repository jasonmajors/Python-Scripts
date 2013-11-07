"""A script to parse a CSV of employee clock-in/clock-out/lunch/break data
	and calculate how many regular and OT hours they worked each/on a given day. Users can specify
	what dates they are interested in."""

import csv
import datetime

MY_FILE = "amy.csv"  # TODO: change to ~os/path/to/csvfile.csv


def parse(raw_file, delimiter):
    """Parses a CSV file to two dictionaries (regular and OT hours) of 'Date: Hours Worked' with both Date
    and Hours Worked as datetime objects."""
    regular_hours = {}
    overtime_hours = {}
    opened_file = open(raw_file)
    csv_data = csv.reader(opened_file, delimiter=delimiter)
    shift = []
    fields = csv_data.next()
    time = None

    for row in csv_data:

        next_time = datetime.datetime.strptime(row[1], "%m/%d/%Y %H:%M")

        if time is None:
            time = next_time
        time_difference = next_time - time

        time_difference = float(time_difference.total_seconds()) / 3600

        if time_difference > 12.5:
            date, shift_hours, ot_hours = hours(shift)
            regular_hours[date] = shift_hours
            overtime_hours[date] = ot_hours
            shift = []
            time = None

        shift.append(dict(zip(fields, row)))
        
    # Calculate the last shift in the csv.
    date, shift_hours, ot_hours = hours(shift)
    regular_hours[date] = shift_hours
    overtime_hours[date] = ot_hours

    opened_file.close()

    return (regular_hours, overtime_hours)


def hours(shift):
    """Parses through an employee shift and returns the date, regular hours worked, and OT hours."""
    # Since lists preserve order, the first dict in the shift list is the time the employee clocks in, and
    # the last has when they clockout.
    date = datetime.datetime.strptime(shift[0]['Date'], "%m/%d/%Y")
    clockin = datetime.datetime.strptime(
        shift[0]['Scan Time'],
        "%m/%d/%Y %H:%M")
    clockout = datetime.datetime.strptime(
        shift[-1]['Scan Time'],
        "%m/%d/%Y %H:%M")
    lunchin = datetime.timedelta()
    lunchout = datetime.timedelta()
    ot_hours = datetime.timedelta()

    for i in shift:
        if i['Scan Type'] == 'Lunch-In/Lunch-Out Swipe':
            lunchin = datetime.datetime.strptime(
                i['Scan Time'], "%m/%d/%Y %H:%M")
            # Break the loop so 'lunchin' is the first lunch swipe found.
            break
    for i in shift:
        if i['Scan Type'] == 'Lunch-In/Lunch-Out Swipe':
            lunchout = datetime.datetime.strptime(
                i['Scan Time'], "%m/%d/%Y %H:%M")

    lunch_time = lunchout - lunchin
    shift_hours = clockout - clockin - lunch_time

    # 8 hours is a regular shift before overtime pay begins.
    if shift_hours > datetime.timedelta(hours=8):
        ot_hours = shift_hours - datetime.timedelta(hours=8)

    shift_hours = shift_hours - ot_hours

    return (date, shift_hours, ot_hours)


def desired_hours(hours_dict, start_date, end_date):
    """Takes either the regular_hours or overtime_hours dictionary and sums the hours the
    employee worked between a start date and end date."""
    total = []
    for date, hours_worked in hours_dict.iteritems():
        if date >= start_date and date <= end_date:
            total.append(hours_worked)

    return sum(total, datetime.timedelta()).total_seconds() / 3600


def main():
    regular_hours, overtime_hours = parse(MY_FILE, ",")
    try:
        start_date = datetime.datetime.strptime(
            raw_input('Enter a start date (m/d/yyyy): '),
            "%m/%d/%Y")
    except ValueError:
        print "Not a valid date."
        return main()
    try:
        end_date = datetime.datetime.strptime(
            raw_input('Enter an end date (inclusive): '),
            "%m/%d/%Y")
    except ValueError:
        print "Not a valid date."
        return main()

    cost = desired_hours(regular_hours, start_date, end_date) * 8.00
    ot_cost = desired_hours(overtime_hours, start_date, end_date) * 12.00

    print "Regular hours: %f" % desired_hours(regular_hours, start_date, end_date)
    print "Overtime hours: %f" % desired_hours(overtime_hours, start_date, end_date)
    print 'Pay: $%f' % (cost + ot_cost)

if __name__ == "__main__":
    main()
