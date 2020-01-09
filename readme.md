# Codechef Contest Calendar

A Google Calendar for upcoming codechef contests. Checkout the demo [here](https://jatin69.github.io/codechef-contest-calendar/).

## How to Use

### Add to Google Calendar

- The Calendar is publically available [here](https://calendar.google.com/calendar?cid=N2RxbWZuNm12cmVpcWIyNmpkbjVydWs1amtAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ). Simply click this link and tap `yes` on the popup for `Add to Calendar`.
- Alternatively, you can also add the calendar by visiting [the demo](https://jatin69.github.io/codechef-contest-calendar/) and then using the `+` sign at the bottom right of calendar to add to your calendar.

Once added, it will sync all contests periodically. You are done.

If you still can't see the events, or the calendar in your google calendar android app, this is because, new Calendars are sometimes hidden by default in the Calendar App. To make it visible, go to `settings` in the calendar app. You'll see a `show more` button under your id which you used to add the calendar. Tap it, select `Codechef Contest Calendar` and turn the `sync` on.

Calendar will now show in your main calendar. If you want to hide it at any point of time, open the side menu and simply unset the checkbox in front of the calendar.

## Dev corner

These steps guide you in detail on how to create a custom calendar, and making a exact replica of this project.

- Make sure you have python 3.7
- Install [pipenv](https://github.com/pypa/pipenv) and get familiar
- Clone this repo [https://github.com/jatin69/codechef-contest-calendar.git](https://github.com/jatin69/codechef-contest-calendar.git)
- Run `pipenv shell` in project root
- Run `pipenv install` in project root
- This will setup all the required dependencies in a virtual env in python

### Basic setup

- step 1 - setting up calendar and configuration
  - You need a calendar to write the events to
  - Go to [Create calendar](https://calendar.google.com/calendar/r/settings/createcalendar) with the same google account you used in the quickstart steps
  - Then go to calendar settings, find the calendar id, and paste it in `sample_config.py` file.
  - Use `mv sameple_config.py config.py` to rename it to `config.py` which will then be used in code. 
- Step 2 - quickstart guide
  - Go to [Python quickstart guide for google calendar](https://developers.google.com/calendar/quickstart/python) 
  - The step 1 of the quickstart guide needs a google account, so make sure you are logged in. 
  - Execute step 1 and download the `credentials.json` and save to project root.
  - This has been [gitignored](./.gitignore) in the project. You need one with your own google account.
  - `sauce` - This step 1 your just executed creates a project names `quickstart` in your google console, enables the google calendar API, and sets up a oauth client id and secret, and downloads it as `credentials.json`
  - If you like, you can follow all the steps in the quickstart, and make sure the basics work
- Step 3 - Setting up authentication
  - Download the `credentials.json` from step 1 and save in project root
  - Run `python components/authenticate.py` in project root
  - Authenticate via the link provided.
  - This will authenticate the first time, then saves a `token.json` to project root to be reused for consecutive authentications.
- step 4 - getting started with project
  - Until now, we have setup a calendar, and obtained API keys to work with it, and authenticated.
  - We also have 3 files ready - `config.py`, `credentials.json` and `token.json`
  - Run `python main.py` to fetch events and save to your google calendar.
- Step 5 - Understanding accounts and apps
  - We first download credentials aka create an app. This is the dev account and basically the app.
  - When we create a calendar, we may or may not use the same dev account, but because our purpose is calendar sharing, we create a calendar in same dev account as the app itself.
  - Now when we execute the script, the authentication has to be provided to the account where the calendar was created. Basically, we allow a dev app to access our calendar and we authenticate to give that app access to our calendar.
  - Because the edits from the script is also done by the dev, we use dev account for everything.
  - Conclusion - use the same google account to create the app, calendar, and the authentication.


This is up and running. 

If you manually run this command once a day, this will fetch new contests, and add them to calendar. This is still cumbersome, because we still have to manually run step 4. We would like to setup this as a cron job, so it runs once a day and automatically updates our calendar.

### Advance Setup

We need to setup a cron job. For this we need a service account from google to interact with our API.

- Step 1 - create a project
  - Every API in google console is accessed on per project basis.
  - First create a project by going to [Google developer's console](https://console.developers.google.com/projectcreate)
  - create a new project with any name. We'll use this project to obtain google calendar API credentials.
  - we'll name the project `codechef-contest-calendar` for now
- Step 2 - Enable the google calendar API
  - Enable the [google calendar API](https://console.developers.google.com/apis/library/calendar-json.googleapis.com) in this project.
  - This API provides 1 million queries per day for free, so we don't need to worry about billing for now.
  - You can manage this newly enabled google calendar API by going [here](https://console.developers.google.com/apis/api/calendar-json.googleapis.com/overview)
- Step 3 - Obtain credentials
  - You might be prompted to create credentials on [this screen](https://console.developers.google.com/apis/api/calendar-json.googleapis.com/overview)
  - Go to [API and Services section](https://console.developers.google.com/apis/credentials)

- in google calendar, add id of service account

# credentials.json : This file is manually downloaded after creating API credentials
# token.json       : automatically created short lived access token after oauth2 


# Public Calendar Link : open to public to add to their calendar
# Just below the calendar id, you'll find public URL of the calendar, copy and paste it here
calendarShareableLink = """https://calendar.google.com/calendar?cid=N2RxbWZuNm12cmVpcWIyNmpkbjVydWs1amtAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ"""
