import datetime

# Website scraping imports
import requests
from bs4 import BeautifulSoup

# Google Calendar API imports
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools

import config


def fetchContests():
    """
    Objective : Fetches all contests from codechef website
    Returns   : A list of event objects.
                Each event object has necessary data to make a google event.
    """
    # fetch & parse contest page
    r = requests.get(config.codechefContestURL)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get all contest tables
    allTables = soup.find_all("table", {"class": "dataTable"})
    # Drop past contests - IMPORTANT - otherwise calendar will be cluttered upto 2009
    allTables.pop()

    # Make a list of active and upcoming contests
    activeAndUpcomingContests = []
    for table in allTables:
        for row in table.find("tbody").find_all("tr"):
            activeAndUpcomingContests.append(row)

    events = []
    for contest in activeAndUpcomingContests:
        tds = contest.find_all("td")
        events.append({
            'contestCode': tds[0].text,
            'contestLink': 'https://www.codechef.com{0}'.format(tds[1].next.attrs['href'].split('?')[0]),
            'contestTitle': tds[1].text,
            'contestStartDate': tds[2].attrs['data-starttime'],
            'contestEndDate': tds[3].attrs['data-endtime']
        })

    return events


def makeEventsonGoogleCalendar(events):
    """
    Objective       : Add events to the google calendar
    Pre-requisite   : Require oauth2 with Google Calendar
    Returns         : Nothing as of now
    """
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/calendar'

    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/calendar/quickstart/python

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    for e in events:
        event = {
            'summary': e['contestTitle'],
            'description': "Contest link - {0}".format(e['contestLink']),
            'start': {
                'dateTime': e['contestStartDate'],
            },
            'end': {
                'dateTime': e['contestEndDate'],
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }

        service.events().insert(calendarId=config.codechefCalendarId, body=event).execute()


if __name__ == '__main__':
    # events = fetchContests()
    events = config.sampleEvents
    makeEventsonGoogleCalendar(events)
