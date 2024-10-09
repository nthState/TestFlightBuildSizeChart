import os
import sys
import time
import requests
import datetime
import jwt
import numpy as np
import matplotlib.pyplot as plt

class TestFlightBuildSizeChart:

	def generateToken(self, issuer_id, key_id, private_key):
		
		current_time = datetime.datetime.now(datetime.timezone.utc)
		unix_timestamp = current_time.timestamp()
		
		exp = unix_timestamp_plus_5_min = unix_timestamp + (10 * 60)  # 10 min * 60 seconds (tokens over 20 minutes are not allowed)
		iss = unix_timestamp_plus_5_min = unix_timestamp + (-1 * 60)  # -1 min * 60 seconds
		
		data = {'aud': 'appstoreconnect-v1',
				'iss': issuer_id,
				'exp': exp,
				'iat': iss}
				
		headers = {'kid': key_id}
		
		encoded_token = jwt.encode(data, private_key, algorithm='ES256', headers=headers)
		
		return encoded_token

	def createChart(self, APP_ID, TOKEN, DEVICES, EXPORT_AS, MAX_VERSIONS):
	
		print("Starting")
			 
		## No need to edit below this line
		
		# Create Header
		HEAD = {
		   'Authorization': 'Bearer ' + TOKEN
		}
		
		DEVICES = DEVICES.split()
		
		# URLS
		BASE_URL = 'https://api.appstoreconnect.apple.com/v1/'
		
		# Find builds
		buildBundleIds = {}
		
		print("---Find Build---")
		
		URL = BASE_URL + 'builds?filter[app]=' + APP_ID + '&include=buildBundles'
		r = requests.get(URL, params={}, headers=HEAD)
		
		counter = 0
		try:
			data = r.json()['data']
			for item in data:
				if counter >= MAX_VERSIONS:
					break
				counter += 1
		
				version = item['attributes']['version']
				buildBundleId = item['relationships']['buildBundles']['data'][0]['id']
				
				print("Found: {}".format(version))
		
				URL = BASE_URL + 'buildBundles/{}/buildBundleFileSizes'.format(buildBundleId)
				r = requests.get(URL, params={}, headers=HEAD)
				dic = {}
				try:
					data = r.json()['data']
					for item in data:
						if item['attributes']['deviceModel'] in DEVICES:
							dic[item['attributes']['deviceModel']] = item['attributes']['downloadBytes']
				except:
					pass
					
				buildBundleIds[version] = dic
				
		except:
			print("error")
			time.sleep(60) #wait for 60 seconds
			
		
		# Generate Chart
		
		n_groups = len(buildBundleIds)
		
		# create plot
		fig, ax = plt.subplots()
		index = np.arange(n_groups)
		bar_width = 0.35
		opacity = 0.8
		
		color = 'g'
		
		for device in DEVICES:
		
			values = []
			for key, value in buildBundleIds.items():
				values.append(value[device] / 1000000)
			tups = tuple(values)
			rects1 = plt.bar(index, tups, bar_width,
				alpha=opacity,
				color=color,
				label=device)
				
			index = index + bar_width
			color = 'b'
		
		
		plt.xlabel('Versions')
		plt.ylabel('Megabytes')
		plt.title('MB per build verson')
		plt.xticks(index - bar_width,tuple(buildBundleIds.keys()))
		plt.legend()
		
		plt.tight_layout()
		#plt.show()
		plt.savefig(EXPORT_AS)


def main():

	issuer_id = os.getenv('ISSUER_ID')
	key_id = os.getenv('KEY_ID')
	private_key = os.getenv('PRIVATE_KEY')
	
	APP_ID = os.getenv('APP_ID')
	DEVICES = os.getenv('DEVICES')
	MAX_VERSIONS = int(os.getenv('MAX_VERSIONS'))
	EXPORT_AS = os.getenv('EXPORT_AS')
	
	service = TestFlightBuildSizeChart()
	token = service.generateToken(issuer_id, key_id, private_key)
	reason = service.createChart(APP_ID, token, DEVICES, EXPORT_AS, MAX_VERSIONS)
	
	print(reason)

if __name__ == "__main__":
	main()

