#!/usr/bin/python

import httplib2
import sys

from datetime import datetime
from datetime import timedelta

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

client_id = '1067073042023.apps.googleusercontent.com'
client_secret = 'fi41sk2FvNk8Y9Zv9VMiBYlw'

# The scope URL for read/write access to a user's calendar data
scope = 'https://www.googleapis.com/auth/calendar'

# Create a flow object. This object holds the client_id, client_secret, and
# scope. It assists with OAuth 2.0 steps to get user authorization and
# credentials.
flow = OAuth2WebServerFlow(client_id, client_secret, scope)

storage = Storage('mod_anniversary_credentials.dat')
credentials = storage.get()
if credentials is None or credentials.invalid:
  credentials = run(flow, storage)

