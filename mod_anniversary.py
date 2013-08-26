# -*- coding: utf-8 -*-
import httplib2
import sys

from datetime import datetime
from datetime import date
from datetime import timedelta

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

# color codes
COL_BLACK  = 0
COL_GREEN  = 1
COL_RED    = 2
COL_ORANGE = 3
COL_TRANSPARENT = 0xff

# The two lines below identify mod_anniversary.
CALENDAR_CLIENT_ID = '1067073042023.apps.googleusercontent.com'
CALENDAR_CLIENT_SECRET = 'fi41sk2FvNk8Y9Zv9VMiBYlw'

class AnniversaryModule:
	# update interval (seconds)
	interval = 0.1
	
	def __init__(self, font, col, inverse_speed, calendars):
		self.font = font
		self.col = col
		self.format = format
		self.client_id = client_id
		self.client_secret = client_secret
		self.calendars = calendars
		self.updated = date.today() - timedelta(days = 1);
		self.inverse_speed = inverse_speed
		self.textwidth = 0
	
	def update_string(self, disp):
		if self.updated == date.today():
			return
		self.updated = date.today();
		print "mod_anniversary: updating string."
		self.strlist = list()
		scope = 'https://www.googleapis.com/auth/calendar'
		flow = OAuth2WebServerFlow(CALENDAR_CLIENT_ID, CALENDAR_CLIENT_SECRET, scope)
		storage = Storage('mod_anniversary_credentials.dat')
		credentials = storage.get()
		if credentials is None or credentials.invalid:
			print "mod_anniversary: No or invalid credentials."
		else:
			print "mod_anniversary: Logging in..."
			http = httplib2.Http()
			http = credentials.authorize(http)
			service = build('calendar', 'v3', http=http)

			print "mod_anniversary: Receiving data..."
# loop over days to sort
			try:
				today = date.today()
				for i in range(8):
					if (i == 0):
						color = COL_RED
					elif (i < 4):
						color = COL_ORANGE
					else:
						color = COL_GREEN
					day_str = (today + timedelta(days = i)).strftime('%Y-%m-%d')
					next_day_str = (today + timedelta(days = i+1)).strftime('%Y-%m-%d')
					for calendar in self.calendars:
						print "mod_anniversary: calendar "+ calendar['name']
						request = service.events().list(calendarId=calendar['id'], timeMin=day_str + 'T00:00:00Z', timeMax=next_day_str + 'T00:00:00Z')
						# Loop until all pages have been processed.
						while request != None:
							# Get the next page.
							response = request.execute()
							# Accessing the response like a dict object with an 'items' key
							# returns a list of item objects (events).
							for event in response.get('items', []):
								# The event object is a dict object with a 'summary' key.
								print "mod_anniversary: entry "+ event.get('summary', '')
								self.strlist.append([event.get('summary', '') + ' (', self.font, color, COL_BLACK])
								self.strlist.append([calendar['name'], calendar['font'](disp) , color, COL_BLACK])
								self.strlist.append([')', self.font, color, COL_BLACK])
								self.strlist.append([', ', self.font, color, COL_BLACK])
#								print repr(event.get('description','')) + '\n'
								# Get the next request object by passing the previous request object to
								# the list_next method.
							request = service.events().list_next(request, response)
			except AccessTokenRefreshError:
				print ('The credentials have been revoked or expired.')
		self.textwidth = 0
		self.strlist.pop()
		sys.stdout.write("mod_anniversary: string is \"")
		for [s,f,c,b] in self.strlist:
			self.textwidth += disp.strwidth(s,f)
			sys.stdout.write(s)
		print "\""
		self.runstrlist = self.strlist[:]
		self.runstrlist.append(['-', self.font, COL_GREEN, COL_BLACK])
		self.runstrlist.extend(self.strlist)

	def update(self, disp, x, y, w, h):
		if self.updated != date.today():
			self.update_string(disp)
		if self.textwidth > w:
			putstrFontColor(disp, x - ((getMillisecondsSince1970() / self.inverse_speed) % (self.textwidth + disp.strwidth('-',self.font))), y, self.runstrlist)
		else:
			putstrFontColor(disp, x, y, self.strlist)


# helper functions

def getMillisecondsSince1970():
	now = datetime.now()
	return int(now.strftime('%s'))*1000+now.microsecond/1000

def putstrFontColor(disp,x,y,l):
	for [s,f,c,b] in l:
		x = disp.putstr_metric(x, y, s, f, c, b)

