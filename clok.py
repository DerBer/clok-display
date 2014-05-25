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

# import configuration
sys.path.append('modules')
import config

# TODOs
# - color/brightness schemes (ht1632c colormap/palette)
# - logging

# Locales should be set so that weekdays are displayed correctly
locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

# rotary encoder pins
PIN_ROTENC_1   = 3
PIN_ROTENC_2   = 4
PIN_ROTENC_BTN = 2

CMD_EXIT = 0
CMD_NEXTPROG = 1
CMD_SETPWM = 2

command = CMD_EXIT
pwmValue = 4

def showScreen(screenId):
	rotation = config.SCREENS[screenId]['rotation']
	screen = config.SCREENS[screenId]['screen']
	
	# init display
	disp = HT1632C(config.NUM_PANELS, rotation)
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
			nextScreen = (screenId + 1) % len(config.SCREENS)
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
