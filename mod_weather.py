# -*- coding: utf-8 -*-
from pyowm import OpenWeatherMapApi

class WeatherModule:
	# update interval (seconds)
	interval = 60.0
	
	def __init__(self, cityName):
		self.owm = OpenWeatherMapApi()
		try:
			cities = self.owm.getcitybycitycountrycode(cityName, None, None)
			self.city = cities[0].identifier if cities else None
			print("OWM city ID for \"%s\": %d" % (cityName, self.city))
		except:
			print("Error: could not get city \"%s\"" % cityName)
			self.city = None
	
	def update(self, disp, x, y):
		font = disp.font4x6
		weather = self.owm.getcityweaterbyid(self.city)
		print "%02.1f" % weather.getmaintempc()
		#y = 2
		#x = 5
		x = disp.putstr(x, y, "%02.1f" % weather.getmaintempc(), font, 1, 0) + 4
		#x = disp.putstr(x, y, t.strftime("%M"), font, 1, 0) + 4
		#x = disp.putstr(x, y, t.strftime("%S"), font, 1, 0)
		#disp.sendframe()
