#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import signal
import os
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
from mod_clock import TimeModule
from mod_clock import DateModule
from mod_clock import SecondBarModule
from mod_weather import WeatherModule

# TODOs
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

SCREENS = [
	[
		{ 'moduleFn': lambda disp: TimeModule(disp.font7x8num, COL_GREEN), 'x': 16, 'y': 0, 'w': 46, 'h': 8  },
		{ 'moduleFn': lambda disp: SecondBarModule(COL_RED, COL_BLACK, 5, COL_ORANGE, 3), 'x': 0, 'y': 9, 'w': 64, 'h': 1  },
		{ 'moduleFn': lambda disp: DateModule(disp.font4x5num, COL_GREEN), 'x': -1, 'y': 11, 'w': 46, 'h': 5  },
		{ 'moduleFn': lambda disp: WeatherModule(CITY, COUNTRY, COL_ORANGE), 'x': 47, 'y': 11, 'w': 17, 'h': 5  }
	],
	[
		{ 'moduleFn': lambda disp: TimeModule(disp.font7x8num, COL_GREEN), 'x': 16, 'y': 0, 'w': 46, 'h': 8  }
	]
]

#class NextProgramException(Exception):
    #pass

CMD_EXIT = 0
CMD_NEXTPROG = 1
CMD_SETPWM = 2

command = CMD_EXIT
pwmValue = 4

def showScreen(screenId):
	# init display
	disp = HT1632C(DISPLAY_ROTATION)
	disp.pwm(pwmValue)
	
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
		
		def close():
			# turn off display
			disp.clear()
			disp.sendframe()
			disp.close()
			# unload modules
			for moduleCfg in SCREENS[screenId]:
				moduleCfg['module'] = None
		
		# init screen
		events = []
		now = datetime.utcnow().replace(microsecond = 0) # (update at start of second)
		for moduleCfg in SCREENS[screenId]:
			moduleCfg['module'] = moduleCfg['moduleFn'](disp)
			update(moduleCfg, now)
		
		# command interrupt signal
		def intr(signal, stack):
			global command
			#print("command: %d" % command)
			# react on command
			if command == CMD_EXIT:
				raise SystemExit(0)
			elif command == CMD_NEXTPROG:
				command = CMD_EXIT
				raise SystemExit(1)
			if command == CMD_SETPWM:
				disp.pwm(pwmValue)
			command = CMD_EXIT
		signal.signal(signal.SIGINT, intr)
		
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
		#print(e.code)
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		close()
		if e.code == 0:
			print("Exiting.")
			return -1
		else:
			nextScreen = (screenId + 1) % len(SCREENS)
			print("Switching to screen %d" % nextScreen)
			#command = CMD_EXIT
			return nextScreen


if __name__ == "__main__":
	# termination functions
	def stop(signal, stack):
		raise SystemExit(0)
	signal.signal(signal.SIGTERM, stop)
	
	# load GPIO
	print("Loading GPIO SPI module")
	os.system("gpio load spi")
		
	# init rotary encoder
	rotenc = RotEnc(PIN_ROTENC_1, PIN_ROTENC_2, PIN_ROTENC_BTN, None)
	def rotencInput(value):
		global command
		if value != 0:
			global pwmValue
			pwmValue += value
			if pwmValue < 0: pwmValue = 0
			if pwmValue > 15: pwmValue = 15
			command = CMD_SETPWM
		else:
			command = CMD_NEXTPROG
		thread.interrupt_main()
	def rotencHandlerThread(re):
		while True:
			rotencInput(re.wait())
	thread.start_new_thread(rotencHandlerThread, (rotenc,))
	
	screenId = 0
	while screenId >= 0:
		screenId = showScreen(screenId)
	
	print("Done.")
	sys.exit(0)
