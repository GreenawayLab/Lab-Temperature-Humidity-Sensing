import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.units as munits
import os
import numpy as np

### Created by Liam Welch for the Greenaway Research Group at Imperial College London ###
### To interface with data files created from software made by Becky Greenaway & Liam Welch ###

### To be placed in the directory with the data files ###
# Example expected data filename
# 2024-10-30 humiditydata.txt 

# Example expected data line
# 2023-11-19,18:40:58,20.49 C,55.17 %RH


abspath = os.path.abspath(__file__) # Finding the local directory
dirname = os.path.dirname(abspath)

os.chdir(dirname) # Changing the directory to the local directory
f = sorted(os.listdir())

datafiles = [] # Setting up the datafiles list
for i, line in enumerate(f):
	if line.split(" ")[-1] == "humiditydata.txt": # Finding the data files and adding them to the datafiles list
		datafiles.append(line)
		
datafiles = sorted(datafiles, key=lambda x: x.split(' ')[0])
first = datafiles[0].split(" ")[0]
last = datafiles[-1].split(" ")[0]
print (f"Found {len(datafiles)} data files, from {first} - {last}\n")
		
def plotshow(x, y1, y2, xformat, xlabel, y1label, y2label, title):
	"""
	Plots temperature (y1) and humidity (y2) over time (x) with dual y-axes.
	The left y-axis represents temperature (y1) in red, and the right y-axis represents 
	humidity (y2) in blue. The x-axis is formatted according to the given `xformat`.

	Parameters:
	-----------
	x : list/array
		Time data for the x-axis.
	y1 : list/array
		Temperature data for the left y-axis.
	y2 : list/array
		Humidity data for the right y-axis.
	xformat : str
		Format string for the x-axis (e.g., "%Y-%m-%d").
	xlabel : str
		Label for the x-axis.
	y1label : str
		Label for the left y-axis (temperature).
	y2label : str
		Label for the right y-axis (humidity).
	title : str
		Title of the plot.
	"""
	fig, ax1 = plt.subplots()
	ax1.plot(x, y1, color = 'tab:red')
	ax1.tick_params(axis = 'y', labelcolor = 'tab:red')
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel(y1label, color = 'tab:red')
	ax1.xaxis.set_major_formatter(mdates.DateFormatter(xformat))
	ax2 = ax1.twinx()
	ax2.set_ylabel(y2label, color = 'tab:blue')
	ax2.plot(x, y2, color = 'tab:blue')
	ax2.tick_params(axis = 'y', labelcolor = 'tab:blue')
	ax1.set_title(title)
	plt.show()

		
		
def plotday(datafile):
	"""
	Reads a text data file containing temperature and humidity data, and plots them over time using the plotshow() function.
	The file is expected to have the format: date,time,temperature,humidity.

	Parameters:
	-----------
	datafile : str
		Path to the text file containing the data.

	This function calls `plotshow` to display the temperature and humidity over time with dual y-axes.
	"""
	title = f"Temperature & Humidity for {datafile.split(" ")[0]}"
	times = [] # Setting up lists
	daytes = []
	temps = []
	humids = []

	with open(datafile, 'r') as datafile:
		for i, line in enumerate(datafile):
			if line[0] == '2': # It is a data line (in the year 2000)
				times.append(line.split(",")[1])
				daytes.append(line.split(",")[0] + " " + line.split(",")[1])
				temps.append(float(line.split(",")[2].split(" ")[0]))
				humids.append(float(line.split(",")[3].split(" ")[0]))

	datetimes = mdates.date2num(daytes) # Converting dates to datetime for better matplotlib performance
	plotshow(datetimes, temps, humids, '%H:00', 'Time', 'Temperature (\u00b0C)', 'Humidity (%RH)', title)		
	
def plotdaily():
	"""
	Reads multiple text data files, calculates daily averages for temperature and humidity,
	and plots them over time. The files are expected to contain temperature and humidity data 
	in the format: date,time,temperature,humidity.

	This function calls `plotshow` to display the daily average temperature and humidity with dual y-axes.

	Assumes `datafiles`, `first`, and `last` are predefined variables representing the file list 
	and the date range for the plot title.
	"""
	title = f"Daily averages {first} - {last}"

	daytes = []
	avgtemps = []
	avghumids = []
	for i, line in enumerate(datafiles):
		with open(line, 'r') as currentfile:
			temps = []
			humids = []
			for j, line2 in enumerate(currentfile):
				if line[0] == '2': # It is a data line (in the year 2000)
					temps.append(float(line2.split(",")[2].split(" ")[0]))
					humids.append(float(line2.split(",")[3].split(" ")[0]))
			daytes.append(line2.split(",")[0] + " 12:00:00")
			avgtemps.append(np.average(temps))
			avghumids.append(np.average(humids))
	datetimes = mdates.date2num(daytes)
	plotshow(datetimes, avgtemps, avghumids, '%d-%b', 'Day', 'Average Temperature (\u00b0C)', 'Average Humidity (%RH)', title)
	
	
def plothourly():
	"""
	Calculates hourly averages for temperature and humidity over multiple days and plots them.
	The data is assumed to be in text files with the format: date,time,temperature,humidity.

	The function groups the data by hour, calculates average temperature and humidity for each hour,
	and displays them in a plot with temperature on the left y-axis (red) and humidity on the right y-axis (blue).

	Assumes `datafiles` is a list of file paths to the data files.
	"""
	title = f"Hourly Averages ({len(datafiles)} Days)"
	hours = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]
	tempdic = {}
	humiddic = {}
	temps = []
	humids = []
	times = []
	x = []
	y1 = []
	y2 = []

	for i, line in enumerate(datafiles): # Loading each data file
		with open(line, 'r') as currentfile:			
			for j, line2 in enumerate(currentfile): # Enumerating through each data entry
				if line[0] == '2': # It is a data line (in the year 2000)
					temps.append(float(line2.split(",")[2].split(" ")[0])) # Appending the data to the lists
					humids.append(float(line2.split(",")[3].split(" ")[0]))
					times.append(line2.split(",")[1])
					
	hourlyavgtemps = []
	hourlyavghumids = []
	
	# Calculating the averages
	for i, line in enumerate(times): 
		m = int(times[i][:2])
		if m not in tempdic.keys():
			tempdic[m] = [temps[i]]
			humiddic[m] = [humids[i]]
		else:
			tempdic[m].append(temps[i])
			humiddic[m].append(humids[i])
	
	tempdic = dict(sorted(tempdic.items())) # Making sure that the dictionaries are in the right order (00->23)
	humiddic = dict(sorted(humiddic.items()))
	keys = [k for k,v in tempdic.items()]

	# Making final lists to plot
	for i, line in enumerate(keys):
		x.append(line)
		y1.append(np.average(tempdic[line]))
		y2.append(np.average(humiddic[line]))
	
		
	fig, ax1 = plt.subplots()
	plt.xticks([0, 3, 6, 9, 12, 15, 18, 21, 24])
	ax1.plot(x, y1, color = 'tab:red')
	ax1.tick_params(axis = 'y', labelcolor = 'tab:red')
	ax1.set_xlabel("Hour")
	ax1.set_ylabel('Average Temperature (\u00b0C)', color = 'tab:red')
	ax1.set_xlim([0, 24])
	
	ax2 = ax1.twinx()
	ax2.set_ylabel('Average Humidity (%RH)', color = 'tab:blue')
	ax2.plot(x, y2, color = 'tab:blue')
	ax2.tick_params(axis = 'y', labelcolor = 'tab:blue')
	ax1.set_title(title)
	plt.show()
	

	#plotshow(x, y1, y2, '%H:%M', 'Hourly average', 'Temperature (\u00b0C)', 'Humidity (%RH)', title)
			
	
	
def plotcontinuous():
	"""
	Reads in temperature and humidity data from all data files contained in datafiles, and plots the data over time.
	The files are expected to be in the format date,time,temperature,humidity.

	This function calls `plotshow` to display the temperature and humidity data with dual y-axes.

	Assumes `datafiles`, `first`, and `last` are predefined variables representing the list of files 
	and the date range for the plot title.
	"""
	title = f"Continuous readings from {first} to {last}"
	daytes = []
	temps = []
	humids = []
	for i, line in enumerate(datafiles):
		with open(line, 'r') as currentfile:
			for j, line2 in enumerate(currentfile):
				if line[0] == '2': # It is a data line (in the year 2000)
					temps.append(float(line2.split(",")[2].split(" ")[0]))
					humids.append(float(line2.split(",")[3].split(" ")[0]))
					daytes.append(line2.split(",")[0] + " " + line2.split(",")[1])
	datetimes = mdates.date2num(daytes)
	plotshow(datetimes, temps, humids, '%d-%b', 'Day', 'Temperature (\u00b0C)', 'Humidity (%RH)', title)
					
				

# Main loop
datafile = datafiles	
while "i" in "Hi":
	datafile = "n"
	print("Enter: \"list\" - to plot a particular day\
	\nLeave blank - to plot the current day\n\
	\"Daily\" - to plot the daily averages\n\
	\"Hourly\" - to plot the hourly averages\n\
	\"Continuous\" - to plot every reading. ")
	while datafile == "n":
		g = input("Plot: ")
		if g == "":
			datafile = datafiles[-1] #The latest datafile
			plotday(datafile)
		elif g == "list" or g == "List":
			for i, line in enumerate(datafiles):
				print(f"{i}: {line}")
			while datafile == "n":
				f = input("Select day number: ")
				try:
					datafile = datafiles[int(f)]
					plotday(datafile)
				except Exception as error:
					print(error)
					pass
		elif g.capitalize() == ("Daily"):
			datafile = datafiles
			plotdaily()
			
		elif g.capitalize() == ("Continuous"):
			datafile = datafiles
			plotcontinuous()
			
		elif g.capitalize() == ("Hourly"):
			datafile = datafiles
			plothourly()
		print("")