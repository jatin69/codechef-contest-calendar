import datetime
import string

# Web scraping imports
import requests
from bs4 import BeautifulSoup

# Google Calendar API imports
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools
from googleapiclient.errors import HttpError

# for user configuration
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

    # Get all contests
    allContestsEver = soup.find_all("table", {"class": "dataTable"})
    activeContests = allContestsEver[0]
    upcomingContests = allContestsEver[1]
    # pastContests = allContestsEver[2]
    ignoredContests = ['INOIPRAC', 'ZCOPRAC']

    # Make a list of active and upcoming contests
    requiredContests = []
    requiredContests.extend(activeContests.find("tbody").find_all("tr"))
    requiredContests.extend(upcomingContests.find("tbody").find_all("tr"))

    events = []
    for contest in requiredContests:
        tds = contest.find_all("td")
        events.append({
            'contestCode': tds[0].text,
            'contestLink': 'https://www.codechef.com{0}'.format(tds[1].next.attrs['href'].split('?')[0]),
            'contestTitle': tds[1].text,
            'contestStartDate': tds[2].attrs['data-starttime'],
            'contestEndDate': tds[3].attrs['data-endtime']
        })
        if tds[0].text in ignoredContests:
            events.pop()

    return events


alphanum = (string.digits+string.ascii_lowercase)[:32]
charMap = {'w': 'ab', 'x': 'cd', 'y': 'ef', 'z': 'gh'}


def tobase32hex(contestCode):
    """converts to base32hex encoding, i.e. lowercase letters a-v and digits 0-9 
    Custom combinations for others
    """
    res = ''
    for s in contestCode.lower():
        if s in alphanum:
            res += s
        elif s in charMap.keys():
            res += charMap[s]
        else:
            pass
    return res


def getUniqueIdForContest(contestCode, startDate, endDate):
    """
    Unique Event id - https://developers.google.com/calendar/v3/reference/events/insert
    - characters allowed in the ID are those used in base32hex encoding, 
    i.e. lowercase letters a-v and digits 0-9
    - the length of the ID must be between 5 and 1024 characters
    - the ID must be unique per calendar
    """
    return 'jatin69codechefcalendarcontestidis' + tobase32hex(contestCode) + tobase32hex(startDate[:19]) + tobase32hex(endDate[:19])


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
            'id': getUniqueIdForContest(e['contestCode'], e['contestStartDate'], e['contestEndDate']),
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }
        try:
            service.events().insert(calendarId=config.codechefCalendarId, body=event).execute()
            print("Added - {0}".format(e['contestTitle']))
        except HttpError:
            print("Duplicate - {0}".format(e['contestTitle']))
            continue


if __name__ == '__main__':
    events = fetchContests()
    # events = config.sampleEvents
    makeEventsonGoogleCalendar(events)
