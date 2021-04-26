#!/usr/bin/python3

class TelemetryMessage():

	def __init__(self, lat, lon, alt, time):
		self.object = {
			"type": "TelemetryReport",
			"attributes": [
				{
					"name": "lat",
					"type": "float",
					"value": str(lat)
				},
				{
					"name": "lon",
					"type": "float",
					"value": str(lon)
				},
				{
					"name": "alt",
					"type": "float",
					"value": str(alt)
				},
				{
					"name": "time",
					"type": "float",
					"value": str(time)
				}
			]
		}