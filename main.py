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

########### Constants ########

# codechef Contests URL
codechefContestURL = 'https://www.codechef.com/contests'

def fetchContests():
    """
    Objective : Fetches all contests from codechef website
    Returns   : A list of event objects.
                Each event object has necessary data to make a google event.
    """
    # fetch & parse contest page
    r = requests.get(codechefContestURL)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get all contests
    allContestsEver = soup.find_all("table", {"class": "dataTable"})
    activeContests = allContestsEver[0]
    upcomingContests = allContestsEver[1]
    # pastContests = allContestsEver[2]

    # ignoring contest that last more than a year
    ignoredContests = ['INOIPRAC', 'ZCOPRAC', 'IARCSJUD']

    # Make a list of active and upcoming contests
    requiredContests = []
    requiredContests.extend(activeContests.find("tbody").find_all("tr"))
    requiredContests.extend(upcomingContests.find("tbody").find_all("tr"))

    events = []
    for contest in requiredContests:
        tds = contest.find_all("td")
        currentContest = {
            'contestCode': tds[0].text,
            'contestLink': 'https://www.codechef.com{0}'.format(tds[1].next.attrs['href'].split('?')[0]),
            'contestTitle': tds[1].text,
            'contestStartDate': tds[2].attrs['data-starttime'],
            'contestEndDate': tds[3].attrs['data-endtime']
        }

        if currentContest['contestCode'] in ignoredContests:
            continue

        if int(currentContest['contestEndDate'][:4]) - int(currentContest['contestStartDate'][:4]) > 0:
            continue
        
        events.append(currentContest)

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


def getUniqueIdForContest(contestCode):
    """
    Unique Event id - https://developers.google.com/calendar/v3/reference/events/insert
    - characters allowed in the ID are those used in base32hex encoding, 
    i.e. lowercase letters a-v and digits 0-9
    - the length of the ID must be between 5 and 1024 characters
    - the ID must be unique per calendar

    Lessons - 
    First i used unique id as - contest code + start date + end date
    Butthis was faulty in a real world case because events get extended.
    To handle updation, we need same event id, so i now just use contest code

    """
    return 'thecodechefcalendarcontestidis' + tobase32hex(contestCode)


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
        uniqueContestId = getUniqueIdForContest(e['contestCode'])
        event = {
            'summary': e['contestTitle'],
            'description': "Contest link - {0}".format(e['contestLink']),
            'start': {
                'dateTime': e['contestStartDate'],
            },
            'end': {
                'dateTime': e['contestEndDate'],
            },
            'id': uniqueContestId,
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }

        currentEvent = ""
        try:
        
            # try to create a new event
            currentEvent = service.events().insert(calendarId=config.codechefCalendarId, body=event).execute()
            print("Added - {0}".format(event['summary']))
        
        except HttpError as err:
        
            # is this a duplicate event?
            if err.resp.status in [409]:
                # print(err)
                # print(err.resp.status)
                
                # already added or modified ?
                currentEvent = service.events().get(calendarId=config.codechefCalendarId, eventId=uniqueContestId).execute()
                # print(currentEvent)

                # assumption - only start and end times change for a contest. ID does not change once decided.
                # event status can be `confirmed` or `cancelled` -> cancelled when deleted by user
                if currentEvent['start']['dateTime'] == event['start']['dateTime'] and \
                    currentEvent['end']['dateTime'] == event['end']['dateTime'] and  \
                    currentEvent['status'] == 'confirmed':
                    print("Already Added - {0}".format(event['summary']))
                else:
                    currentEvent['start']['dateTime'] = event['start']['dateTime']
                    currentEvent['end']['dateTime'] = event['end']['dateTime']
                    currentEvent['status'] = 'confirmed'
                    updated_event = service.events().update(calendarId=config.codechefCalendarId, eventId=uniqueContestId, body=currentEvent).execute()
                    # print(updated_event)
                    print("Updated - {0}".format(event['summary']))

            else:
                print("Unexpected error. Moving forward.")
            
            continue


# sample event structure

sampleEvents = [
        {
            'contestCode': 'TEST', 
            'contestLink': 'https://www.codechef.com/TEST', 
            'contestTitle': 'TESTBRO', 
            'contestStartDate': '2020-01-10T13:00:00+05:30', 
            'contestEndDate': '2020-01-10T15:00:00+05:30'
        }
    ]

# date format is `YYYY-MM-DDTHH:MM:SS+05:30`

if __name__ == '__main__':
    # events = fetchContests() 
    events = sampleEvents
    makeEventsonGoogleCalendar(events)
