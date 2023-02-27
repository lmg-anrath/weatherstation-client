#!/usr/bin/python

import os
import json
import requests
import time

from sds011 import SDS011
import Adafruit_DHT
import bme280

config = json.load(open('config.json'))
timestamp = str(round(time.time()))

print('Reading data...')
errors = {}

temperature1 = None
humidity1 = None
try:
	humidity1, temperature1 = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
	temperature1 = str(round(temperature, 2))
	humidity1 = str(round(humidity, 0))
except Exception as e:
	print('Error while reading data from DHT22!')
	print(e)
	errors['DHT22'] = str(e);

temperature2 = None
air_pressure = None
humidity2 = None
try:
	temperature2, air_pressure, humidity2 = bme280.readBME280All()
	temperature2 = str(round(temperature2, 2))
	humidity2 = str(round(humidity2, 0))
	air_pressure = str(round(air_pressure, 0))
except Exception as e:
	print('Error while reading data from BME280!')
	print(e)
	errors['BME280'] = str(e);

temperature = temperature1
humidity = humidity1
if temperature1 == None and temperature2 != None:
	temperature = temperature2
if humidity == None and humidity2 != None:
	humidity = humidity2

air_particle_pm25 = None
air_particle_pm10 = None
try:
	air_particle = SDS011("/dev/ttyUSB0", use_query_mode=True).query()
	air_particle_pm25 = str(air_particle[0])
	air_particle_pm10 = str(air_particle[1])
except Exception as e:
	print('Error while reading data from SDS011!')
	print(e)
	errors['SDS011'] = str(e);

print(f'Temp: {temperature} C ({temperature1} C & {temperature2} C), Humidity: {humidity} % ({humidity1} % & {humidity2} %), Air pressure: {air_pressure} hPa, Air particle: {air_particle_pm25} pm25 and {air_particle_pm10} pm10')
print('The data has been collected.')

data = { 'timestamp': timestamp }
if temperature != None: data['temperature'] = temperature
if humidity != None: data['humidity'] = humidity
if air_pressure != None: data['air_pressure'] = air_pressure
if air_particle_pm25 != None: data['air_particle_pm25'] = air_particle_pm25
if air_particle_pm10 != None: data['air_particle_pm10'] = air_particle_pm10

print('Uploading data to the server...');
online = False

try:
	res = requests.post(config['url'] + '/v2/stations/' + str(config['stationId'] - 1), data=data, headers={ 'Authorization': config['accessToken'] })

	print('Upload completed with status code ' + str(res.status_code) + '!')
	print('Response from server: ' + res.text)
	online = True
except requests.ConnectionError:
	print('Error while upload data to the server! Check your internet connection.')

	print('Temporary logging data in \'data.json\'')
	if not os.path.isfile('data.json'):
		json.dump([], open('data.json', 'w'))
	data_list = json.load(open('data.json'))
	data_list.append(data)
	json.dump(data_list, open('data.json', 'w'))
	print('Data has been saved in \'data.json\'')

if len(errors) > 0 and online:
	print('Uploading errors to the server...')
	try:
		res = requests.post(config['url'] + '/v2/stations/' + str(config['stationId'] - 1) + '/error', data=errors, headers={ 'Authorization': config['accessToken'] })
		print('Upload completed with status code ' + str(res.status_code) + '!')
		print('Response from server: ' + res.text)
	except requests.ConnectionError:
		print('Error while upload errors to the server! Check your internet connection.')

if os.path.isfile('data.json') and online:
	print('Uploading previous data to the server...')
	data_list = json.load(open('data.json'))
	if len(data_list) == 0:
		print('No data to upload.')
		os.remove('data.json')
		exit()

	try:
		res = requests.post(config['url'] + '/v2/stations/' + str(config['stationId'] - 1) + '/bulk', data=data_list, headers={ 'Authorization': config['accessToken'] })
		print('Upload completed with status code ' + str(res.status_code) + '!')
		print('Response from server: ' + res.text)
		if (res.status_code == 200):
			os.remove('data.json')
			print('\'data.json\' has been removed.')
	except requests.ConnectionError:
		print('Error while upload previous data to the server! Check your internet connection.')
