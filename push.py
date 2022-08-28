import json
import requests

config = json.load(open('config.json'))
data = json.load(open('data.json'))

for x in data:
	print('Uploading data to the server...');

	entry = data[x]

	entry['stationId'] = config['stationId']
	entry['accessToken'] =  config['accessToken']

	try:
		res = requests.post(config['url'] + '/post', data=entry)

		print('Upload completed with status code ' + str(res.status_code) + '!')
		print('Response from server: ' + res.text)
	except requests.ConnectionError:
		print('Error while upload data to the server! Check your internet connection.')