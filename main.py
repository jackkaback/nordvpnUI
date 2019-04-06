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

	regionList = ["Albania", "Greece", "Portugal", "Argentina", "Hong_Kong", "Romania",
				"Australia", "Hungary", "Serbia", "Austria", "Iceland", "Singapore", "Belgium",
				"India", "Slovakia", "Bosnia_And_Herzegovina", "Indonesia", "Slovenia", "Brazil",
				"Ireland", "South_Africa", "Bulgaria", "Israel", "South_Korea", "Canada", "Italy", "Spain",
				"Chile", "Japan", "Sweden", "Costa_Rica", "Latvia", "Switzerland", "Croatia", "Luxembourg",
				"Taiwan", "Cyprus", "Malaysia", "Thailand", "Czech_Republic", "Mexico", "Turkey", "Denmark",
				"Moldova", "Ukraine", "Estonia", "Netherlands", "United_Kingdom", "Finland", "New_Zealand",
				"United_States", "France", "North_Macedonia", "Vietnam", "Georgia", "Norway", "Germany", "Poland"]

	# alphabetizes
	regionList = sorted(regionList)

	
	region = StringVar(base)
	region.set(regionList[0])  # default value

	w = OptionMenu(base, region, *regionList)
	w.pack()

	mainloop()

	connect(region.get())


if __name__ == '__main__':
	disconnect()
	main()
