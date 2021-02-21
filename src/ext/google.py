import os
from dateutil.parser import parse as dtparse

from ..util import rootdir

# Google API
import datetime
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Google API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def GetCalendarEvents():
    print('[Calendar API] Get last events')
    creds = None
    tokendir = os.path.join(rootdir, 'token.pickle')
    
    #Check if the user already logged
    if os.path.exists(tokendir):
        with open(tokendir,'rb') as token:
            creds = pickle.load(token)
    
    # If the file doesn't exists, log the user
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(rootdir, 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokendir,'wb') as token:
            pickle.dump(creds,token)
    
    service = build('calendar','v3',credentials=creds,cache_discovery=False)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('[Calendar API] Getting the upcoming 7 events')
    events_result = service.events().list(calendarId=os.getenv('CALENDAR_ID'),timeMin=now,maxResults=7,singleEvents=True,orderBy='startTime').execute()

    events = events_result.get('items',[])

    return_events = []

    if not events:
        print('No upcoming events found')
    
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start_datetime = dtparse(start)
        end_datetime = dtparse(end)

        new_event = {
            "start_date": start_datetime,
            "end_date": end_datetime,
            "title": event["summary"]
        }
        return_events.append(new_event)

    return return_events