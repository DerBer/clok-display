# -*- coding: utf-8 -*-
import sys
sys.path.append('../python-openweathermap-api/package')
from pyowm import OpenWeatherMapApi

# color codes
COL_BLACK  = 0
COL_GREEN  = 1
COL_RED    = 2
COL_ORANGE = 3
COL_TRANSPARENT = 0xff

COL_AUTO   = -1

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
			try:
				weather = self.owm.getcityweaterbyid(self.city)
				temp = weather.getmaintempc()
				print("Current temp: %4.1f°C" % temp)
				if (self.col == COL_AUTO):
					if (temp < 18):
						col = COL_GREEN
					elif (temp < 25):
						col = COL_ORANGE
					else:
						col = COL_RED
				else:
					col = self.col
				putsSpecial(disp, x, y, "%4.1f^" % temp, font, col, 0)
			except:
				print("Error: could not get temperature")
			
class WeatherModuleColored(WeatherModule):
	def __init__(self, cityName, countryCode):
		WeatherModule.__init__(self, cityName, countryCode, COL_AUTO)


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
