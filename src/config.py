# event structure
dummy_events = [
    {
        'contestCode': 'TEST',
        'contestLink': 'https://www.codechef.com/TEST',
        'contestTitle': 'TEST EVENT',
        'contestStartDate': '2020-01-10T13:00:00+05:30',
        'contestEndDate': '2020-01-10T15:00:00+05:30'
    }
]

# date format is `YYYY-MM-DDTHH:MM:SS+05:30`

# calendar id secret
def getMyCodechefCalendarID():
    import json
    with open('./../secrets/calendar_secrets.json') as f:
        data = json.load(f)
        codechefCalendarId = data["codechefCalendarId"]
        # shareableLinkOfCalendar = data["shareableLinkOfCalendar"]
    return codechefCalendarId

# choose script_mode
# script_mode = "user"
script_mode = "service_account"

# choose events
# event_mode = "codechef"
event_mode = "dummy_event"
