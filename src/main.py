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

# import user modules
import authenticate_user
import authenticate_service_account
import fetch_codechef_contests
import get_unique_contest_id


def makeEventsonGoogleCalendar(events):
    """
    Objective       : Add events to the google calendar
    Pre-requisite   : Require oauth2 with Google Calendar
    Returns         : Nothing as of now
    """

    # authenticate with google and create a service

    credentials = None
    if config.script_mode == "user":
        credentials = authenticate_user.authenticateUser()
    else:
        credentials = authenticate_service_account.authenticateServiceAccount()

    service = build('calendar', 'v3', http=credentials.authorize(Http()))

    # iterate through events and add to calendar

    for e in events:
        uniqueContestId = get_unique_contest_id.getUniqueIdForContest(
            e['contestCode'])
        currentEventBody = {
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
            currentEvent = service.events().insert(calendarId=config.codechefCalendarId,
                                                   body=currentEventBody).execute()
            print("Added - {0}".format(currentEvent['summary']))

        except HttpError as err:

            # is this a duplicate event?
            if err.resp.status in [409]:
                # print(err)
                # print(err.resp.status)

                # already added or modified ?
                currentEvent = service.events().get(calendarId=config.codechefCalendarId,
                                                    eventId=uniqueContestId).execute()
                # print(currentEvent)

                # assumption - only start and end times change for a contest. ID does not change once decided.
                # event status can be `confirmed` or `cancelled` -> cancelled when deleted by user
                if currentEvent['start']['dateTime'] == currentEventBody['start']['dateTime'] and \
                        currentEvent['end']['dateTime'] == currentEventBody['end']['dateTime'] and  \
                        currentEvent['status'] == 'confirmed':
                    print(
                        "Already Added - {0}".format(currentEvent['summary']))
                else:
                    currentEvent['start']['dateTime'] = currentEventBody['start']['dateTime']
                    currentEvent['end']['dateTime'] = currentEventBody['end']['dateTime']
                    currentEvent['status'] = 'confirmed'
                    updated_event = service.events().update(calendarId=config.codechefCalendarId,
                                                            eventId=uniqueContestId, body=currentEvent).execute()
                    # print(updated_event)
                    print("Updated - {0}".format(updated_event['summary']))

            else:
                print("Unexpected error. Moving forward.")

            continue


if __name__ == '__main__':

    events = config.dummy_events

    if config.event_mode == "codechef":
        events = fetch_codechef_contests.fetchContests()

    makeEventsonGoogleCalendar(events)
