#!/usr/bin/env python
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START calendar_quickstart]
from __future__ import print_function
import datetime
import json
import pickle
import os.path
import iso8601
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def creds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def colorMapping(colorId):
    if colorId == None:
        return "Unspecified"
    return {
        1: "11",
        2: "#PeopleMgmt",
        3: "33",
        4: "Meta/Organizing",
        5: "Nicktime",
        6: "66",
        7: "77",
        8: "AWAY"
    }[int(colorId)]

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    service = build('calendar', 'v3', credentials=creds())

    # Call the Calendar API
    now = datetime.datetime.utcnow()
    start = now - datetime.timedelta(days=now.weekday())
    end = start + datetime.timedelta(days=6)
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', 
                                        timeMin=start.isoformat() + 'Z',
                                        timeMax=end.isoformat() + 'Z',
                                        maxResults=100, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    check_projects(events)

def header():
    print("\n#####################\n\n\n")

def duration(event):
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['start'].get('date'))
    total = (iso8601.parse_date(end)-iso8601.parse_date(start)).total_seconds()
    if total == 1500:
        return 1800
    if total == 3000:
        return 3600
    #print(total)
    return total

def check_projects(events):
    header()

    times_by_proj = {}
    for event in events:
        if event['status'] == "confirmed" or event['status'] == 'tentative':
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['start'].get('date'))
       
            proj = colorMapping(event.get('colorId'))
            if not times_by_proj.get(proj):
                times_by_proj[proj] = 0
            times_by_proj[proj] = times_by_proj[proj]+duration(event)
            print(start, event['summary'], proj, duration(event))
            #print(json.dumps(event, indent=True))

    for proj, total in times_by_proj.items():
        print(proj, total/60.0/60.0)


if __name__ == '__main__':
    main()
# [END calendar_quickstart]
