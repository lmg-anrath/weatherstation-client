import json
import requests
from datetime import datetime

config = json.load(open('config.json'))
time = datetime.now()

print('Reading data...')

# For testing purposes static values
temperature = 24.6
humidity = 0.57
air_pressure = 1010

print(f'Temp: {temperature}, Humidity: {humidity}, Air pressure: {air_pressure}')
print('The data has been collected.')

print('Uploading data to the server...');

data = {
	'stationId': config['stationId'],
	'accessToken': config['accessToken'],
	'temperature': temperature,
	'humidity': humidity,
	'air_pressure': air_pressure
}

res = requests.post(config['url'] + '/post', data=data)

print('Upload completed with status code ' + str(res.status_code))
print('Response from server: ' + res.text)