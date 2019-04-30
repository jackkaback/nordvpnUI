#!/usr/bin/env python3

# For executing terminal commands
import os

# For reading output from the OS/Terminal
import subprocess

# For the user interfaces
from tkinter import *


def client_exit(self):
	exit()


# parses the data from the console
def parseInput(data):

	# Turns the data from a lot of gibberish into the output
	data = str(data.stdout)

	# List of things to be replaced
	remove_vals = ["\\r", "\\n", "\\t", "\\", ",", " "]

	for ii in range(len(remove_vals)):
		data = data.replace(remove_vals[ii], "-")

	# Splits the data into a useable array
	data = data.split("-")

	ret_val = []

	# removes assorted trash data
	for jj in range(len(data)):
		if len(data[jj]) >= 3:
			ret_val.append(data[jj])

	# sorts for easy reading
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
	base.geometry("300x200")

	choices = ["Connect", "Disconnect", "Exit"]

	# setup for drop down menu choices
	con_dis = StringVar(base)
	con_dis.set(choices[0])

	# sets up the drop down menu
	drop_down = OptionMenu(base, con_dis, *choices)
	drop_down.pack()

	# continue button
	quit_button = Button(base, text="Select", command=lambda: base.destroy())
	quit_button.pack()

	# runs the GUI
	mainloop()

	# if user selected exit, end the program
	if con_dis.get() == "Exit":
		exit(0)

	return con_dis.get() == "Connect"


# GUI for geting country
def GUICountry(region_list):

	base = Tk()
	base.title("Nord VPN setup")
	base.geometry("300x200")

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

	# continue button
	quit_button = Button(base, text="Select", command=lambda: base.destroy())
	quit_button.pack()

	# runs the GUI
	mainloop()

	return [region.get(), pickCity.get()]


# GUI for selecting city
def GUICity(cities):

	base = Tk()
	base.title("Nord VPN setup")
	base.geometry("300x200")

	text = Label(base, text="City Select")
	text.pack()

	region = StringVar(base)
	region.set(cities[0])  # default value

	# sets up the drop down menu
	drop_down = OptionMenu(base, region, *cities)
	drop_down.pack()

	# continue button
	quit_button = Button(base, text="Select", command=lambda: base.destroy())
	quit_button.pack()

	# runs the GUI
	mainloop()

	return region.get()


# connects to the location
def connect(location):
	# connects to VPN
	command = "nordvpn connect " + location
	os.system(command)

	# sends out a systm notification for the user to see where they connected
	location = location.replace(" ", ", ")
	location = location.replace("_", " ")
	subprocess.Popen(['notify-send', "Connected to " + location])


def disconnect():
	os.system("nordvpn disconnect")
	subprocess.Popen(['notify-send', "Disconnected from VPN"])


def main():

	disconnect()

	connected = False

	# get list of countries at launch
	country_list = getCountries()

	# runs infinitely until user closes the program
	while(True):

		# if they want to connect
		if GUIConDis():

			# [0] for country, [1] for connect to city
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


# run if is run as main
if __name__ == '__main__':
	main()
