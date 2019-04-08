#!/usr/bin/env python3
import os
import subprocess
from tkinter import *


# parses the data from the console
def parseInput(data):

	# Turns the data from a lot of giberish into the output
	data = str(data.stdout)
	data = data.replace("\\r", "-")
	data = data.replace("\\n", "-")
	data = data.replace("\\t", "-")
	data = data.replace("\\", "-")
	data = data.split("-")

	ret_val = []

	# removes assorted trash data
	for i in range(len(data)):
		if len(data[i]) >= 3:
			ret_val.append(data[i])

	ret_val = sorted(ret_val)

	return ret_val


# gets the countries in the list
def getCountries():

	country_list = subprocess.run(['nordvpn', 'countries'], stdout=subprocess.PIPE)

	country_list = parseInput(country_list)

	# added any to support connecting to random server
	country_list.append("Any")
	return country_list


# gets cities from a country
def getCities(country):
	city_list = subprocess.run(['nordvpn', 'cities', country], stdout=subprocess.PIPE)

	return parseInput(city_list)


# gui for choosing connect or disconnect
# returns true for connect, false for disconnect
def guiConDis():
	base = Tk()
	base.title("Nord VPN setup")
	base.geometry("300x150")

	choices = ["Connect", "Disconnect", "Exit"]

	conDis = StringVar(base)
	conDis.set(choices[0])

	# sets up the drop down menu
	w = OptionMenu(base, conDis, *choices)
	w.pack()

	mainloop()

	if conDis.get() == "Exit":
		exit(0)

	return conDis.get() == "Connect"

# GUI for geting country
def guiCountry():

	base = Tk()
	base.title("Nord VPN setup")
	base.geometry("300x150")

	# list of currently supported countries
	region_list = getCountries()

	region = StringVar(base)
	region.set(region_list[0])  # default value

	# sets up the drop down menu
	w = OptionMenu(base, region, *region_list)
	w.pack()

	# if the user wants to city select
	pickCity = IntVar()
	Checkbutton(base, text="city select", variable=pickCity).pack()

	mainloop()

	return [region.get(), pickCity.get()]


# GUI for selecting city
def guiCity(cities):

	base = Tk()
	base.title("Nord VPN setup")
	base.geometry("300x150")

	region = StringVar(base)
	region.set(cities[0])  # default value

	# sets up the drop down menu
	w = OptionMenu(base, region, *cities)
	w.pack()

	mainloop()

	return region.get()


# connects to the location
def connect(location):
	temp = "nordvpn connect " + location
	os.system(temp)


def disconnect():
	os.system("nordvpn disconnect")


def main():

	while(True):

		if guiConDis():

			tempArr = guiCountry()

			# picking any makes the VPN decide the location
			if tempArr[0] == "Any":
				connect("")

			# pick the city GUI for specific city
			elif tempArr[1] == 1:
				cities = getCities(tempArr[0])
				city = guiCity(cities)
				connect(tempArr[0] + " " + city)

			# connect to whatever server in the target country
			else:
				connect(tempArr[0])

		else:
			disconnect()


if __name__ == '__main__':
	main()
