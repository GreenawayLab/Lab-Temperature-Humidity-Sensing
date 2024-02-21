import bme680
from time import sleep
import datetime
from datetime import datetime
from csv import writer

print("""temperature-humidity.py - Displays date, time, temperature, and humidity.

Press Ctrl+C to exit

""")

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
    
# These oversampling settings can be tweaked to change the balance between accuracy and noise in the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

print('Data sensing')

try:
    while True:
        if  sensor.get_sensor_data():
            output = datetime.now().strftime('%Y-%m-%d,%H:%M:%S,')+'{0:.2f} C,{1:.2f} %RH'.format(
                sensor.data.temperature,
                sensor.data.humidity)
            print(output)

        sleep(30)

except KeyboardInterrupt:
    pass

#To output sensor data to .txt file, in terminal enter 'python3 lab-temp-humidity.py > txt file'
