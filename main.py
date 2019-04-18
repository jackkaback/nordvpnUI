#!/usr/bin/env python3

# For exicuting terminal commands
import os

# For reading output from the OS/Terminal
import subprocess

# For the user interfaces
from tkinter import *


# parses the data from the console
def parseInput(data):

	# Turns the data from a lot of gibberish into the output
	data = str(data.stdout)

	# List of things to be replaces
	temp = ["\\r", "\\n", "\\t", "\\", ",", " "]

	for i in range(len(temp)):
		data = data.replace(temp[i], "-")

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


# GUI for choosing connect or disconnect
# returns true for connect, false for disconnect, exits for exit
def GUIConDis():
	base = Tk()
	base.title("Nord VPN setup")
	base.geometry("300x150")

	choices = ["Connect", "Disconnect", "Exit"]

	# setup for drop down menu choices
	conDis = StringVar(base)
	conDis.set(choices[0])

	# sets up the drop down menu
	drop_down = OptionMenu(base, conDis, *choices)
	drop_down.pack()

	# runs the GUI
	mainloop()

	# if user sleceted exit, end the program
	if conDis.get() == "Exit":
		exit(0)

	return conDis.get() == "Connect"


# GUI for geting country
def GUICountry(region_list):

	base = Tk()
	base.title("Nord VPN setup")
	base.geometry("300x150")

	region = StringVar(base)
	region.set(region_list[0])  # default value

	text = Label(base, text="Country Select")
	text.pack()

	# sets up the drop down menu
	drop_down = OptionMenu(base, region, *region_list)
	drop_down.pack()

	# if the user wants to city select
	pickCity = IntVar()
	Checkbutton(base, text="Select a City?", variable=pickCity).pack()

	# runs the GUI
	mainloop()

	return [region.get(), pickCity.get()]


# GUI for selecting city
def GUICity(cities):

	base = Tk()
	base.title("Nord VPN setup")
	base.geometry("300x150")

	text = Label(base, text="City Select")
	text.pack()

	region = StringVar(base)
	region.set(cities[0])  # default value

	# sets up the drop down menu
	drop_down = OptionMenu(base, region, *cities)
	drop_down.pack()

	# runs the GUI
	mainloop()

	return region.get()


# connects to the location
def connect(location):
	temp = "nordvpn connect " + location
	os.system(temp)


def disconnect():
	os.system("nordvpn disconnect")


def main():

	disconnect()

	connected = False

	# get list of countries at launch
	country_list = getCountries()

	# runs infinitely until user closes the program
	while(True):

		# if they want to connect
		if GUIConDis():

			temp_arr = GUICountry(country_list)

			# disconnects before reconnecting
			if connected:
				disconnect()

			connected = True

			# picking any makes the VPN decide the location
			if temp_arr[0] == "Any":
				connect("")

			# pick the city GUI for specific city
			elif temp_arr[1] == 1:
				cities_list = getCities(temp_arr[0])
				city_picked = GUICity(cities_list)
				connect(temp_arr[0] + " " + city_picked)

			# connect to whatever server in the target country
			else:
				connect(temp_arr[0])

		# if they want to disconnect
		else:
			if connected:
				disconnect()

			connected = False


if __name__ == '__main__':
	main()
