#!/usr/bin/python3

import json
import re


# function to write in json file
def write_in_json(json_file, pprz_file, flight_id):

	data = {flight_id: pprz_file}

	with open(json_file, "r") as file:

		file_data = json.load(file)

	# INVESTIGATE : does not work without the print (or the second one)
	# when adding flights, can erase completely the json file 
	print(file_data)
	
	file_data["flights"][flight_id] = pprz_file

	print(file_data)

	with open(json_file, "w") as file:

		file.write(json.dumps(file_data, indent = 4, sort_keys = True))

	return


# function to erase in json
def erase_in_json(json_file, pprz_file = None, flight_id = None):

	if pprz_file is None and flight_id is None:

		print("Error in erase_in_json, pprz file and flight id are None")
		return

	# probably won't be used this way but just in case
	elif pprz_file is not None and flight_id is None:

		with open(json_file, "r") as file:

			file_data = json.load(file)

		for key, value in file_data.items():

			if value == pprz_file:

				file_data["flights"].pop(key)

		with open(json_file, "w") as file:

				file.write(json.dumps(file_data, indent = 4, sort_keys = True))

	# most probable case
	elif flight_id is not None:

		with open(json_file, "r") as file:

			file_data = json.load(file)

		try:
			file_data["flights"].pop(flight_id)
		except KeyError:
			print("flight id not found in airmap.flights.json")
			return

		with open(json_file, "w") as file:

				file.write(json.dumps(file_data, indent = 4, sort_keys = True))

	return



def to_deg(coord):

	# coord format accepted : 19 54 34.9 E // 19 54 34.9 // 19.90969

	# case 19 54 34.9 E
	if re.match(r"[0-9][0-9] [0-9][0-9] [0-9][0-9]\.[0-9]* [NSEW]", coord):

		splitted = re.split(r' ', coord)
		d = float(splitted[0])
		m = float(splitted[1])
		s = float(splitted[2])
		hem = splitted[3]

		dms = d + (m/60) + (s/3600)

		if hem == 'W' or hem == "S":

			dms *= -1

		return dms

	# case 19 54 34.9
	if re.match(r"[0-9][0-9] [0-9][0-9] [0-9][0-9]\.[0-9]*", coord):

		splitted = re.split(r' ', coord)
		d = float(splitted[0])
		m = float(splitted[1])
		s = float(splitted[2])

		dms = d + (m/60) + (s/3600)

		return dms

	# case 19.90969
	if re.match(r"\-?[0-9]*\.[0-9]*", coord):

		return coord


if __name__ == '__main__':
	print(to_deg("19 54 34.9 E"))
	print(to_deg("19 54 34.9"))
	print(to_deg("19.90969"))
