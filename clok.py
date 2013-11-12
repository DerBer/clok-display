#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import signal
import os
import heapq
import thread
import math
import locale
from time import sleep
from datetime import datetime
from datetime import timedelta

sys.path.append('../ht1632clib/python')
from ht1632c import HT1632C
from rotenc import RotEnc

sys.path.append('modules')
from mod_clock import TimeModule
from mod_clock import DateModule
from mod_clock import DateModuleVertical
from mod_clock import SecondBarModule
from mod_weather import WeatherModule
from mod_weather import WeatherModuleColored
from mod_anniversary import AnniversaryModule

# TODOs
# - color/brightness schemes (ht1632c colormap/palette)
# - logging

# location settings
CITY = 'Münster'
COUNTRY = 'DE'

# display settings
NUM_PANELS = 2

# calendar settings
# Note: you will need a file 'mod_anniversary_credentials.dat' that
# can be created using an external script by logging into your google
# account and permitting mod_anniversary access to your calendar.
# The module also needs the google calendar api to be installed.
# This can usually be done by running
#
#   easy_install --upgrade google-api-python-client

CALENDARS = [
  {
    'name' : '*',
    'id' : 'someid@group.calendar.google.com',
    'font' : (lambda disp: disp.font4x6)
  },
  {
    'name' : 'Jahrestag',
    'id' : 'someotherid@group.calendar.google.com',
    'font' : (lambda disp: disp.font4x6)
  }
]

# Locales should be set so that weekdays are displayed correctly
locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

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
	{
		# display rotation (multiples of 90° clockwise)
		'rotation': 0,
		# screen configuration
		'screen': [
			{ 'moduleFn': lambda disp: TimeModule(disp.font7x8num, COL_GREEN), 'x': 16, 'y': 0, 'w': 46, 'h': 8  },
			{ 'moduleFn': lambda disp: SecondBarModule(COL_RED, COL_BLACK, 5, COL_ORANGE, 3), 'x': 0, 'y': 9, 'w': 64, 'h': 1  },
			{ 'moduleFn': lambda disp: DateModule(disp.font4x5num, COL_GREEN), 'x': -1, 'y': 11, 'w': 46, 'h': 5  },
			{ 'moduleFn': lambda disp: WeatherModule(CITY, COUNTRY, COL_ORANGE), 'x': 47, 'y': 11, 'w': 17, 'h': 5  },
		]
	},
	{
		'rotation': 0,
		# screen configuration
		'screen': [
			{ 'moduleFn': lambda disp: TimeModule(disp.font7x8num, COL_GREEN), 'x': 16, 'y': 0, 'w': 31, 'h': 8  },
			{ 'moduleFn': lambda disp: DateModuleVertical(disp.font3x4num, COL_GREEN), 'x': 0, 'y': 0, 'w': 16, 'h': 10  },
			{ 'moduleFn': lambda disp: WeatherModuleColored(CITY, COUNTRY), 'x': 47, 'y': 0, 'w': 17, 'h': 5  },
			{ 'moduleFn': lambda disp: AnniversaryModule(disp.font4x6, COL_GREEN, 100, CALENDARS), 'x': 0, 'y': 10, 'w': 64, 'h': 6  },
		]
	},
	{
		'rotation': 0,
		'screen': [
			{ 'moduleFn': lambda disp: TimeModule(disp.font12x16, COL_GREEN), 'x': 5, 'y': 1, 'w': 53, 'h': 15  },
		]
	},
	{
		'rotation': 1,
		'screen': [
			{ 'moduleFn': lambda disp: TimeModule(disp.font8x12, COL_ORANGE, "%H"), 'x': 1, 'y': 0, 'w': 15, 'h': 12  },
			{ 'moduleFn': lambda disp: TimeModule(disp.font8x12, COL_ORANGE, "%M"), 'x': 1, 'y': 12, 'w': 15, 'h': 12  },
			{ 'moduleFn': lambda disp: TimeModule(disp.font8x12, COL_GREEN, "%S"), 'x': 1, 'y': 24, 'w': 15, 'h': 12  },
			{ 'moduleFn': lambda disp: WeatherModule(CITY, COUNTRY, COL_RED), 'x': -1, 'y': 48, 'w': 17, 'h': 5  },
		]
	},
	{
		# display rotation (multiples of 90° clockwise)
		'rotation': 2,
		# screen configuration
		'screen': [
			{ 'moduleFn': lambda disp: TimeModule(disp.font7x8num, COL_GREEN), 'x': 16, 'y': 0, 'w': 46, 'h': 8  },
			{ 'moduleFn': lambda disp: SecondBarModule(COL_RED, COL_BLACK, 5, COL_ORANGE, 3), 'x': 0, 'y': 9, 'w': 64, 'h': 1  },
			{ 'moduleFn': lambda disp: DateModule(disp.font4x5num, COL_GREEN), 'x': -1, 'y': 11, 'w': 46, 'h': 5  },
			{ 'moduleFn': lambda disp: WeatherModule(CITY, COUNTRY, COL_ORANGE), 'x': 47, 'y': 11, 'w': 17, 'h': 5  },
		]
	},
]

CMD_EXIT = 0
CMD_NEXTPROG = 1
CMD_SETPWM = 2

command = CMD_EXIT
pwmValue = 4

def showScreen(screenId):
	rotation = SCREENS[screenId]['rotation']
	screen = SCREENS[screenId]['screen']
	
	# init display
	disp = HT1632C(NUM_PANELS, rotation)
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
			# set clip region
			disp.clip(x, y, x + w, y + h)
			# clear region
			disp.box(x, y, x + w, y + h, 0)
			# module update with failure handling
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
			for moduleCfg in screen:
				moduleCfg['module'] = None
		
		# init screen
		events = []
		now = datetime.utcnow().replace(microsecond = 0) # (update at start of second)
		for moduleCfg in screen:
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
		
		# main loop
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
			sys.stdout.flush()
	
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
