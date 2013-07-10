#!/usr/bin/env python

import sys
from time import sleep
from datetime import datetime
import signal

sys.path.append('../ht1632clib/python')
from ht1632c import HT1632C
from rotenc import RotEnc

if __name__ == "__main__":
	# init display
	disp = HT1632C()
	disp.pwm(8)
	
	# init rotary encoder
	def cb(value):
		print("cb", value)
	rotenc = RotEnc(3, 4, 2, cb)
	
	# termination functions
	def stop(signal, stack):
		raise SystemExit('Exiting')
	signal.signal(signal.SIGTERM, stop)
	signal.signal(signal.SIGINT, stop)
	
	# display update function
	def update():
		disp.clear()
		t = datetime.now()
		#print t
		font = disp.font8x12
		x = 0
		x = disp.putstr(x, 0, t.strftime("%H"), font, 1) + 3
		x = disp.putstr(x, 0, t.strftime("%M"), font, 1) + 3
		x = disp.putstr(x, 0, t.strftime("%S"), font, 1)
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
