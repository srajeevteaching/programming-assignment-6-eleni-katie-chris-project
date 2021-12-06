# Team Members: Chris, Eleni, Katie
# Course: CS151, Dr. Rajeev
# Programming Assignment: 6
# Date: 12/5/21

import csv
import datetime
import matplotlib.pyplot as plt


CSV_START_YYYYMM = 0         # The year and month in the format YYYYMM in which the storm started
CSV_START_DD = 1             # The day of the month in which the storm started
CSV_START_HHMM = 2           # The time at which the storm started
CSV_END_YYYYMM = 3           # The year and month in the format YYYYMM in which the storm ended
CSV_END_DD = 4               # The day of the month in which the storm ended
CSV_END_HHMM = 5             # The time at which the storm ended
CSV_STATE = 6                # The name of the state where storm occurred
CSV_TYPE = 7                 # The type of storm
CSV_INJURIES_DIRECT = 8      # The number of injuries directly caused by the storm
CSV_INJURIES_INDIRECT = 9    # The number of injuries indirectly caused by the storm
CSV_DEATHS_DIRECT = 10       # The number of deaths directly caused by the storm
CSV_DEATHS_INDIRECT = 11     # The number of deaths indirectly caused by the storm
CSV_DAMAGE_PROPERTY = 12     # The amount of damage to property
CSV_DAMAGE_CROPS = 13        # The amount of damage to crops

# A function that, given a filename, loads the data and returns it as a list of lists.
def load_data(filename):
	try:
		f = open(filename, "r")
	except FileNotFoundError:
		print("Exception: \"{}\" not found!".format(filename))
		return []

	# https://nam04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwww.kite.com%2Fpython%2Fanswers%2Fhow-to-read-a-%2560csv%2560-file-into-a-list-in-python&amp;data=04%7C01%7Ccmplowman%40loyola.edu%7Cd5e4dbb90267456d42b508d9ac4a7a1d%7C30ae0a8f3cdf44fdaf34278bf639b85d%7C0%7C0%7C637730258156949158%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000&amp;sdata=haazojHrXIQOJTYWQbs8HamwAmLwgPZZKIFuGV6XV7A%3D&amp;reserved=0
	data = []
	csv_reader = csv.reader(f)
	for row in csv_reader:
		data.append(row)
	f.close()
	return data


# What is the difference in deaths and injuries directly caused by each storm?
# Were there significant fewer, fewer, the same, more, or significantly more injuries than deaths?
# You should consider a change of +/- 1 to be no change. Changes for +/- 5 are significant.
# This information should be output for each storm to a file that the user chooses.
def deaths_and_injuries(data):
	line = []

	outfile = open(input("enter the file to receive the data: "), "w")
	for row in data:
		sub = (int(row[CSV_DEATHS_DIRECT]) - int(row[CSV_INJURIES_DIRECT]))
		absolute = abs(sub)
		if sub < 0 and absolute >= 5:
			difference = "significantly more direct injuries than deaths"
		elif sub < 0 and absolute < 5:
			difference = "no significant difference in direct deaths and injuries"
		elif sub > 0 and absolute >= 5:
			difference = "significantly more direct deaths than injuries"
		elif sub > 0 and absolute < 5:
			difference = "no significant difference in direct deaths and injuries"
		else:
			difference = "same amount of direct deaths and injuries"

		outfile.write(str(sub) + " " + difference + "\n")


# Create a graph that shows the number of storms with no, low, moderate, and high damage to property.
# Low damage is less than 1000 and high damage is greater than 10000.
def property_damage(data):
	dict = {'none':0, 'low':0, 'moderate':0, 'high':0}
	for row in data:
		damage = float(row[CSV_DAMAGE_PROPERTY])
		if damage < 1000:
			dict['none'] += 1
		elif damage < 4000:
			dict['low'] += 1
		elif damage < 7000:
			dict['moderate'] += 1
		else:
			dict['high'] += 1

	keys = list(dict.keys())
	values = list(dict.values())

	plt.figure(figsize = (10, 5))
	plt.bar(keys, values, color = "red", width = 0.4)
	plt.xlabel("Property Damaged")
	plt.ylabel("No. of storms")
	plt.title("Property Damaged Graph")
	plt.show()


# You can ignore the time of day and only look at the date. But be careful - if it starts and ends on the same
# day, it counts as lasting for 1 day, not zero.
def storm_duration_in_days(start_yyyy, start_mm, start_dd, end_yyyy, end_mm, end_dd):
	return (datetime.date(end_yyyy, end_mm, end_dd) - datetime.date(start_yyyy, start_mm, start_dd)).days + 1


# What was the average number of days that each type of storm lasted? You can ignore the time of day and only look
# at the date. But be careful - if it starts and ends on the same day, it counts as lasting for 1 day, not zero.
def average_days_per_storm(data):
	dict = {}

	for row in data:
		storm_type = row[CSV_TYPE]
		storm_duration = storm_duration_in_days(int(row[CSV_START_YYYYMM][:4]), int(row[CSV_START_YYYYMM][-2:]), int(row[CSV_START_DD]), int(row[CSV_END_YYYYMM][:4]), int(row[CSV_END_YYYYMM][-2:]), int(row[CSV_END_DD]))
		if storm_type not in dict:
			dict[storm_type] = [int(storm_duration)]
		else:
			dict[storm_type].extend([int(storm_duration)])

	for key in dict:
		print(key + ": {:.1f} days".format(sum(dict[key])/len(dict[key])))


# How many storms per state?
def storms_per_state(data):
	dict = {}

	for row in data:
		storm_state = row[CSV_STATE]
		if storm_state not in dict:
			dict[storm_state] = 1
		else:
			dict[storm_state] += 1

	for key in dict:
		print(key + ": {} storms".format(dict[key]))


# Write a program that reads in the data from the file "storm2000.csv", stores it in a list of lists, and then answers
# the following questions about that data. The program should give a menu with all options and should only end when the
# user chooses the option to end from the menu.
def main():
	data = load_data("storm2000.csv")
	if len(data):
		while True:
			print("1) deaths and injuries")
			print("2) property damage")
			print("3) storm duration")
			print("4) storms per state")
			print("5) quit")
			choice = input("choice: ")
			if choice == "1":
				deaths_and_injuries(data)
			elif choice == "2":
				property_damage(data)
			elif choice == "3":
				average_days_per_storm(data)
			elif choice == "4":
				storms_per_state(data)
			elif choice == "5":
				break
			else:
				continue


main()
