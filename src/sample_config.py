# Go to the settings of the calendar you created,
# scroll down to `Integrate calendar` heading, and copy the calendar ID from there

# this calendar ID is needed along with credentials to make the API call
codechefCalendarId = """<your calendar ID>@group.calendar.google.com"""

# Under access permission, you can also find sharable link of calendar
# use it to share the calendar with your friends

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
