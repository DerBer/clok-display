# -*- coding: utf-8 -*-
import httplib2
import sys

from datetime import datetime
from datetime import date
from datetime import timedelta

from bisect import insort

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
		self.calendars = calendars
		self.updated = date.today() - timedelta(days = 1);
		self.inverse_speed = inverse_speed
		self.textwidth = 0
	
	def update_string(self, disp):
		if self.updated == date.today():
			return
		self.updated = date.today();
		print "mod_anniversary: Updating string"
		self.strlist = list()
		eventlist = list()
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
				today_str = today.strftime('%Y-%m-%d')
				soon_str = (today + timedelta(days = 7)).strftime('%Y-%m-%d')
				for calendar in self.calendars:
					print "mod_anniversary: Calendar "+ calendar['name']
					request = service.events().list(calendarId=calendar['id'], timeMin=today_str + 'T00:00:00Z', timeMax=soon_str + 'T00:00:00Z')
					# Loop until all pages have been processed.
					while request != None:
						response = request.execute()

						for event in response.get('items', []):
							print "mod_anniversary: Entry "+ event.get('summary', '')
							eventstrlist = list()
							when_str = event.get('start', '')['date']
							when = date(int(when_str[0:4]),int(when_str[5:7]), int(when_str[8:10]))
							time_left = when - today

							if (time_left == timedelta(days = 0)):
								color = COL_RED
								weekday = ''
							elif (time_left < timedelta(days = 4)):
								color = COL_ORANGE
								weekday = ', ' + when.strftime('%a')
							else:
								color = COL_GREEN
								weekday = ', ' + when.strftime('%a')

							try:
								year = int(event.get('description', '0'))
							except ValueError:
								year = 0
							if (0 < year and year <= today.year):
								anniversary = ', '+str(today.year - year) + '.'
							else:
								anniversary = ''

							eventstrlist.append([event.get('summary', '') + ' (', self.font, color, COL_BLACK])
							eventstrlist.append([calendar['name'], calendar['font'](disp) , color, COL_BLACK])
							eventstrlist.append([anniversary + weekday + ')', self.font, color, COL_BLACK])
							eventstrlist.append([', ', self.font, color, COL_BLACK])
							insort(eventlist,[when,eventstrlist])
						request = service.events().list_next(request, response)
			except AccessTokenRefreshError:
				print ('mod_anniversary: The credentials have been revoked or expired.')
		for when, eventstrlist in eventlist:
			self.strlist.extend(eventstrlist)
		self.strlist.pop()
		self.textwidth = 0
		sys.stdout.write("mod_anniversary: String is \"")
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

