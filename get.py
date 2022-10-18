from __future__ import print_function
import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_event():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        events_result = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        result = ""

        if not events:
            return 'No upcoming events found.'

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            result += (start + " " + event['summary'] + '\n')

        return result

    except HttpError as error:
        print('An error occured: %s' % error)
        return "Couldn't list event"

print(get_event())

if event['summary'] != "Wells Fargo : WFT : Campus : NIT Durgapur : Interns":
            #     print(event['summary'] + " deleted.")
            #     service.events().delete(calendarId='primary', eventId=event['id']).execute()
