import json
import requests
import os
import time
from datetime import datetime

from sds011 import SDS011
import Adafruit_DHT
import bme280

config = json.load(open('config.json'))
log = json.load(open('data.json'))
timestamp = str(datetime.now())

print('Reading data...')

Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
time.sleep(2)
humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
temperature = str(int(round(temperature*10,0)))
humidity = str(int(round(humidity,0)))

temperature2, air_pressure, humidity2 = bme280.readBME280All()
air_pressure = str(int(round(air_pressure,0)))

air_particle = SDS011("/dev/ttyUSB0", use_query_mode=True).query()
air_particle_pm25 = str(air_pressure[0])
air_particle_pm10 = str(air_pressure[1])

print(f'Temp: {temperature} °C, Humidity: {humidity} %, Air pressure: {air_pressure} mbar, Air particle: {air_particle_pm25} pm25 and {air_particle_pm10} pm10')
print('The data has been collected.')

print('Logging data in \'data.json\'')

data = {
	'timestamp': timestamp,
	'temperature': temperature,
	'humidity': humidity,
	'air_pressure': air_pressure,
	'air_particle_pm25': air_particle_pm25,
	'air_particle_pm10': air_particle_pm10
}

log.append(data)
json.dump(log, open('data.json', 'w'), indent = 4, separators = (',',': '))
print('Data successfully saved!')


print('Uploading data to the server...');

data['stationId'] = config['stationId']
data['accessToken'] =  config['accessToken']

try:
	res = requests.post(config['url'] + '/post', data=data)

	print('Upload completed with status code ' + str(res.status_code) + '!')
	print('Response from server: ' + res.text)
except requests.ConnectionError:
	print('Error while upload date to the server! Check your internet connection.')