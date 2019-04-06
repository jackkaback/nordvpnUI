#!/usr/bin/env python3
import os
from tkinter import *


# connects to the location
def connect(location):
	temp = "nordvpn connect " + location
	os.system(temp)


def disconnect():
	os.system("nordvpn disconnect")


def main():
	base = Tk()
	base.title("Nord VPN setup")
	base.geometry("300x150")


	# list of currently supported countries
	region_list = ["Albania", "Argentina", "Australia", "Austria", "Belgium", "Bosnia_And_Herzegovina", "Brazil",
				"Bulgaria", "Canada", "Chile", "Costa_Rica", "Croatia", "Cyprus", "Czech_Republic", "Denmark",
				"Estonia", "Finland", "France", "Georgia", "Germany", "Greece", "Hong_Kong", "Hungary", "Iceland",
				"India", "Indonesia", "Ireland", "Israel", "Italy", "Japan", "Latvia", "Luxembourg", "Malaysia",
				"Mexico", "Moldova", "Netherlands", "New_Zealand", "North_Macedonia", "Norway", "Poland", "Portugal",
				"Romania", "Serbia", "Singapore", "Slovakia", "Slovenia", "South_Africa", "South_Korea", "Spain",
				"Sweden", "Switzerland", "Taiwan", "Thailand", "Turkey", "Ukraine", "United_Kingdom",
				"United_States", "Vietnam"]

	region = StringVar(base)
	region.set(region_list[0])  # default value

	# sets up the drop down menu
	w = OptionMenu(base, region, *region_list)
	w.pack()

	mainloop()

	connect(region.get())


if __name__ == '__main__':
	disconnect()
	main()
