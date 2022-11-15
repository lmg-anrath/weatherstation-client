import json
import requests
import time

from sds011 import SDS011
import Adafruit_DHT
import bme280

config = json.load(open('config.json'))
# log = json.load(open('data.json'))
timestamp = str(round(time.time()))

print('Reading data...')

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
temperature = str(round(temperature, 2))
humidity = str(round(humidity, 0))

temperature2, air_pressure, humidity2 = bme280.readBME280All()
air_pressure = str(round(air_pressure,0))

air_particle = SDS011("/dev/ttyUSB0", use_query_mode=True).query()
air_particle_pm25 = str(air_particle[0])
air_particle_pm10 = str(air_particle[1])

print(f'Temp: {temperature} °C, Humidity: {humidity} %, Air pressure: {air_pressure} mbar, Air particle: {air_particle_pm25} pm25 and {air_particle_pm10} pm10')
print('The data has been collected.')

data = {
	'timestamp': timestamp,
	'temperature': temperature,
	'humidity': humidity,
	'air_pressure': air_pressure,
	'air_particle_pm25': air_particle_pm25,
	'air_particle_pm10': air_particle_pm10
}

# print('Logging data in \'data.json\'')
# log.append(data)
# json.dump(log, open('data.json', 'w'), indent = 4, separators = (',',': '))
# print('Data successfully saved!')


print('Uploading data to the server...');

data['stationId'] = config['stationId']
data['accessToken'] =  config['accessToken']

try:
	res = requests.post(config['url'] + '/post', data=data)

	print('Upload completed with status code ' + str(res.status_code) + '!')
	print('Response from server: ' + res.text)
except requests.ConnectionError:
	print('Error while upload data to the server! Check your internet connection.')
