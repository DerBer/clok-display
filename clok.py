#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import signal
import heapq
import thread
import math
from time import sleep
from datetime import datetime
from datetime import timedelta

sys.path.append('../ht1632clib/python')
from ht1632c import HT1632C
from rotenc import RotEnc

sys.path.append('modules')
sys.path.append('../python-openweathermap-api/package') # TODO why doesn't install work?
from mod_clock import TimeModule
from mod_clock import DateModule
from mod_clock import SecondBarModule
from mod_weather import WeatherModule

# TODOs
# - programs
# - color/brightness schemes (ht1632c colormap/palette)
# - logging

# display rotation (multiples of 90° clockwise)
DISPLAY_ROTATION = 0

# location settings
CITY = 'Münster'
COUNTRY = 'DE'

# rotary encoder pins
PIN_ROTENC_1   = 3
PIN_ROTENC_2   = 4
PIN_ROTENC_BTN = 2

# color codes
COL_BLACK  = 0
COL_GREEN  = 1
COL_RED    = 2
COL_ORANGE = 3

if __name__ == "__main__":
	# init display
	disp = HT1632C(DISPLAY_ROTATION)
	disp.pwmValue = 4
	disp.pwm(disp.pwmValue)
	
	#print urlopen("http://vomber.de").read()
	
	# init rotary encoder
	rotenc = RotEnc(PIN_ROTENC_1, PIN_ROTENC_2, PIN_ROTENC_BTN, None)
	def rotencInput(value):
		#print(value)
		disp.pwmValue += value
		if disp.pwmValue < 0: disp.pwmValue = 0
		if disp.pwmValue > 15: disp.pwmValue = 15
		disp.pwm(disp.pwmValue)
	def rotencHandlerThread(re):
		while True:
			rotencInput(re.wait())
	thread.start_new_thread(rotencHandlerThread, (rotenc,))
	
	# termination functions
	def stop(signal, stack):
		raise SystemExit('Exiting')
	signal.signal(signal.SIGTERM, stop)
	signal.signal(signal.SIGINT, stop)
	
	screen = [
		{ 'module': TimeModule(disp.font7x8num, COL_GREEN), 'x': 16, 'y': 0, 'w': 46, 'h': 8  },
		{ 'module': SecondBarModule(COL_RED, COL_BLACK, 5, COL_ORANGE, 3), 'x': 0, 'y': 9, 'w': 64, 'h': 1  },
		{ 'module': DateModule(disp.font4x5num, COL_GREEN), 'x': -1, 'y': 11, 'w': 46, 'h': 5  },
		{ 'module': WeatherModule(CITY, COUNTRY, COL_ORANGE), 'x': 47, 'y': 11, 'w': 17, 'h': 5  }
	]
	
	# main loop, process module updates
	try:
		def update(moduleCfg, now):
			# update module
			module = moduleCfg['module']
			x = moduleCfg['x']
			y = moduleCfg['y']
			w = moduleCfg['w']
			h = moduleCfg['h']
			disp.clip(x, y, x + w, y + h)
			try:
				module.update(disp, x, y, w, h)
			except Exception as e:
				print("Module update error: " + str(e))
				disp.line(x, y, x + w - 1, y + h - 1, 2)
			
			# schedule next (skip intervals if necessary)
			realNow = datetime.utcnow()
			d = module.interval
			nextTime = now + timedelta(seconds = d * math.ceil((realNow - now).total_seconds() / d))
			heapq.heappush(events, (nextTime, moduleCfg))
		
		events = []
		now = datetime.utcnow().replace(microsecond = 0) # (update at start of second)
		for moduleCfg in screen:
			update(moduleCfg, now)
		
		while True:
			# next event
			(nextTime, nextEvent) = heapq.heappop(events)
			# wait
			now = datetime.utcnow()
			if (nextTime > now):
				# commit frame
				disp.sendframe()
				sleep((nextTime - now).total_seconds())
			# update display
			update(nextEvent, nextTime)
	except SystemExit as e:
		print(e.code)
	
	# turn off display
	disp.clear()
	disp.sendframe()
	
	print("Done.")
	sys.exit(0)
