#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import sleep
from datetime import datetime
import signal

sys.path.append('../ht1632clib/python')
from ht1632c import HT1632C
from rotenc import RotEnc

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
	
	# display update function
	def update():
		disp.clear()
		disp.plot(0, 0, 2); disp.plot(1, 0, 2); disp.plot(0, 1, 2)
		disp.plot(63, 0, 2); disp.plot(62, 0, 2); disp.plot(63, 1, 2)
		disp.plot(0, 15, 2); disp.plot(1, 15, 2); disp.plot(0, 14, 2)
		disp.plot(63, 15, 2); disp.plot(62, 15, 2); disp.plot(63, 14, 2)
		t = datetime.now()
		#print t
		font = disp.font8x12
		y = 2
		x = 5
		x = disp.putstr(x, y, t.strftime("%H"), font, 1) + 4
		x = disp.putstr(x, y, t.strftime("%M"), font, 1) + 4
		x = disp.putstr(x, y, t.strftime("%S"), font, 1)
		disp.sendframe()
	
	# main loop
	try:
		while True:
			# update display
			update()
			# wait for next second
			t = datetime.now()
			sleep(1.0 - (t.microsecond / 1000000.0))
	except SystemExit as e:
		print(e.code)
	
	# turn off display
	disp.clear()
	disp.sendframe()
	
	print("Done.")
	sys.exit(0)
