# Lab-Temperature-Humidity-Sensing
Code for continuous temperature and humidity sensing with a BME688 sensor

## Hardware
----------------
- BME688 sensor, with trace on back of board marked ADDR cut
- Pi400

## Setup
- 2-6V connected to 3.3 VDC power (header pin 1)
- SDA connected to GPIO8 (header pin 3)
- SCL connected to GPIO9 (header pin 5)
- GND connected to Ground (header pin 9)


## Guide for monitoring temperature and humidty at set time points
----------------
1) copy forked link from Github and git clone https://github.com/pimoroni/bme680-python.git
2) link to directory in terminal - 'cd bme680-python'
3) Install using 'sudo python3 setup.py install'
4) Enable I2C 'sudo raspi-config' (Interface options > I2C to Yes)
5) Check sensor being detected 'i2cdetect -y 1' - BME688 should be in 77, if in 76 (which we found did not work with 'bme680-python' can cut the trace on the back of the board marked ADDR)
6) Save `lab-temp-humidity.py` to folder and run 'python3 lab-temp-humidity.py' - data can be stored to a .txt using 'python3 lab-temp-humidity.py > txt file' and example of output included as 'sensor_output.txt'

## Script Parameters
----------------
The sleep time can be changed between measurements, and the sensor is also capable of outputing pressure measurements as well.

# BME Sensor Plotter
----------------
## Requirements
- Matplotlib
- Numpy

## Usage
The BME Sensor Plotter.py file can be launched using a text editor or just by double clicking the .py file.\
This script will launch a command line interface, which allows the plotting of humidity data as generated by the lab-temp-humidity.py script.\
2024-03-17 humiditydata.txt included in repository as an example data file

## Modes
The interface will prompt the user to select a plotting mode:
- Day
  - Lists all days for which data was found, and prompt user to select one
- Daily
  - Plots the daily averages (RH & humidity) for each day
- Hourly
  - Plots the average values for each hour from all available data
- Continuous
  - Similar to Daily, but plots each data point instead of an average

Leaving the field blank and pressing enter will plot the last recorded day