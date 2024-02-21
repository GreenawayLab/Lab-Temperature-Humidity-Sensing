# Lab-Temperature-Humidity-Sensing
----------------
Code for continuous temperature and humidity sensing with a BME688 sensor

## Hardware
----------------
- BME688 sensor, with trace on back of board marked ADDR cut
- Pi400

## Guide for monitoring temperature and humidty at set time points
----------------
1) copy forked link from Github and git clone https://github.com/pimoroni/bme680-python.git
2) link to directory in terminal - 'cd bme680-python'
3) Install using 'sudo python3 setup.py install'
4) Enable I2C 'sudo raspi-config' (Interface options > I2C to Yes)
5) Check sensor being detected 'i2cdetect -y 1' - BME688 should be in 77, if in 76 (which we found did not work with 'bme680-python' can cut the trace on the back of the board marked ADDR)
6) Run `lab-temp-humidity.py`
