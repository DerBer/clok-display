#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import signal
import heapq
from time import sleep
from datetime import datetime
from datetime import timedelta

sys.path.append('../ht1632clib/python')
from ht1632c import HT1632C
from rotenc import RotEnc

sys.path.append('modules')
sys.path.append('../python-openweathermap-api/package') # TODO why doesn't install work?
from mod_time import TimeModule
from mod_weather import WeatherModule

# Feature TODOs
# - programs
# - regions/widgets
# - color/brightness schemes
# - weather source

# display rotation (multiples of 90° clockwise)
DISPLAY_ROTATION = 0

# rotary encoder pins
PIN_ROTENC_1   = 3
PIN_ROTENC_2   = 4
PIN_ROTENC_BTN = 2

if __name__ == "__main__":
	# init display
	disp = HT1632C(DISPLAY_ROTATION)
	disp.pwmValue = 7
	disp.pwm(disp.pwmValue)
	
	# init rotary encoder
	def rotencInput(value):
		disp.pwmValue += value
		if disp.pwmValue < 0: disp.pwmValue = 0
		if disp.pwmValue > 15: disp.pwmValue = 15
		disp.pwm(disp.pwmValue)
	rotenc = RotEnc(PIN_ROTENC_1, PIN_ROTENC_2, PIN_ROTENC_BTN, rotencInput)
	
	# termination functions
	def stop(signal, stack):
		raise SystemExit('Exiting')
	signal.signal(signal.SIGTERM, stop)
	signal.signal(signal.SIGINT, stop)
	
	screen = [
		{ 'module': TimeModule(), 'x': 0, 'y': 0 },
		{ 'module': WeatherModule('Darmstadt'), 'x': 48, 'y': 11 }
	]
	
	# main loop, process module updates
	try:
		def update(moduleCfg, now):
			# update module
			module = moduleCfg['module']
			x = moduleCfg['x']
			y = moduleCfg['y']
			module.update(disp, x, y)
			
			# schedule next
			d = timedelta(seconds = module.interval)
			heapq.heappush(events, (now + d, moduleCfg))
		
		events = []
		now = datetime.now().replace(microsecond = 0) # (update at start of second)
		for moduleCfg in screen:
			update(moduleCfg, now)
		
		while True:
			# next event
			(nextTime, nextEvent) = heapq.heappop(events)
			# wait
			now = datetime.now()
			if (nextTime > now):
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
