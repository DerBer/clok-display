# -*- coding: utf-8 -*-
from pyowm import OpenWeatherMapApi

class WeatherModule:
	# update interval (seconds)
	interval = 900.0
	
	def __init__(self, cityName, countryCode, col):
		self.col = col
		self.owm = OpenWeatherMapApi()
		try:
			cities = self.owm.getcitybycitycountrycode(cityName, None, countryCode)
			self.city = cities[0].identifier if cities else None
			print("OWM city ID for \"%s\" (%s): %d" % (cityName, countryCode, self.city))
		except:
			print("Error: could not get city \"%s\" (%s)" % (cityName, countryCode))
			self.city = None
	
	def update(self, disp, x, y, w, h):
		font = disp.font4x5num
		if self.city != None:
			weather = self.owm.getcityweaterbyid(self.city)
			print("Current temp: %02.1f°C" % weather.getmaintempc())
			putsSpecial(disp, x, y, "%02.1f^" % weather.getmaintempc(), font, self.col, 0)
			

# helper functions

def putsSpecial(disp, x, y, s, font, col, bg):
	for c in s:
		if c == '.':
			disp.plot(x + 1, y + 4, col)
			x += 2
		elif c == '^':
			disp.box(x + 1, y, x + 2, y + 1, col)
			x += 3
		else:
			x = disp.putchar(x, y, c, font, col, bg)
	return x
