# -*- coding: utf-8 -*-
from pyowm import OpenWeatherMapApi

class WeatherModule:
	# update interval (seconds)
	interval = 900.0
	
	def __init__(self, cityName, countryCode):
		self.owm = OpenWeatherMapApi()
		try:
			cities = self.owm.getcitybycitycountrycode(cityName, None, countryCode)
			self.city = cities[0].identifier if cities else None
			print("OWM city ID for \"%s\" (%s): %d" % (cityName, countryCode, self.city))
		except:
			print("Error: could not get city \"%s\" (%s)" % (cityName, countryCode))
			self.city = None
	
	def update(self, disp, x, y, w, h):
		if self.city != None:
			font = disp.font4x6
			weather = self.owm.getcityweaterbyid(self.city)
			print("Current temp: %02.1f°C" % weather.getmaintempc())
			x = disp.putstr(x, y, "%02.1f" % weather.getmaintempc(), font, 1, 0) + 4
