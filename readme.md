# Codechef Contest Calendar ![Cron job status](https://github.com/jatin69/codechef-contest-calendar/workflows/Cron%20Job%20Workflow/badge.svg)

A Custom Google Calendar for upcoming codechef contests. Checkout the demo [here](https://jatin69.github.io/codechef-contest-calendar/).

## How to Use

### Add to Google Calendar

- The Calendar is publically available [here](https://calendar.google.com/calendar?cid=N2RxbWZuNm12cmVpcWIyNmpkbjVydWs1amtAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ). Simply click this link and tap `yes` on the popup for `Add to Calendar`.
- Alternatively, you can also add the calendar by visiting [the demo](https://jatin69.github.io/codechef-contest-calendar/) and then using the `+` sign at the bottom right of calendar to add to your calendar.

Once added, it will sync all contests periodically. You are done.

If you still can't see the events, or the calendar in your google calendar android app, this is because, new Calendars are sometimes hidden by default in the Calendar App. To make it visible, go to `settings` in the calendar app. You'll see a `show more` button under your id which you used to add the calendar. Tap it, select `Codechef Contest Calendar` and turn the `sync` on.

Calendar will now show in your main calendar. If you want to hide it at any point of time, open the side menu and simply unset the checkbox in front of the calendar.

## Development

- I first scraped events from codechef website
- Then added them on a newly made google calendar
- Then setup a cron job to periodically auto update the calendar by re-scraping codechef contests once a day
- Then setup slack notifications if a cron build fails
- You can simply add the calendar to your google account and it'll show up in your google calendar app.

### Part 1 - Setting up environment

These steps will guide you in detail on how to create a custom calendar, and making a exact replica of this project.

- Make sure you have python 3.7
- Install [pipenv](https://github.com/pypa/pipenv) and get familiar
- Clone this repo [https://github.com/jatin69/codechef-contest-calendar.git](https://github.com/jatin69/codechef-contest-calendar.git)
- Run `pipenv shell` in project root, then `pipenv install`
- This will setup all the required dependencies in a virtual env in python

### Part 2 - Setting up the app

- Step 1 - Quickstart guide
  - Go to [Python quickstart guide for google calendar](https://developers.google.com/calendar/quickstart/python)
  - The step 1 of the quickstart guide needs a google account, so make sure you are logged in.
  - Execute step 1 and download the client configuration and save to `secrets` with name `credentials_user.json`
  - This step 1 your just executed creates a project names `quickstart` in your google console, enables the google calendar API, and sets up a oauth client id and secret, and downloads it.
  - If you like, you can follow all the steps in the quickstart guide to get familiar with everything. However, it is not necessary.
- step 2 - setting up calendar
  - You need a calendar to write the events to
  - Go to [Create calendar](https://calendar.google.com/calendar/r/settings/createcalendar) with the same google account you used in step 1
  - Rename `sample_calendar_secrets.json` to `calendar_secrets.json`
  - Then go to calendar settings, find the calendar id, and paste it in `calendar_secrets.json` file.
- Step 3 - Setting up authentication
  - go to `src` directory, Run `python authenticate_user.py`
  - Authenticate via the link that comes in the shell.
  - This will authenticate the first time, then saves a `token.json` to `src` to be reused for consecutive authentications.
- step 4 - configuration
  - find the `config.py` file in `src` directory
  - make sure the `script mode` is `user`
  - events you can choose either `dummy` or actual `codechef events`
- step 5 - getting started with project
  - Until now, we have setup a calendar, and obtained API keys to work with it, and authenticated. We also have 2 files ready - `credentials_user.json` and `calendar_secrets.json` in the `secrets` folder
  - Inside `src`, Run `python main.py` to fetch events and save to your google calendar.
- Step 6 - checking the calendar
  - check the calendar in web UI or android app, refresh, it should show the newly added event
- Step 7 - Understanding accounts and apps
  - We first downloaded credentials aka created an app. This is the dev account and basically the app.
  - When we create a calendar, we may or may not use the same dev account, but because our purpose is calendar sharing, we create a calendar in same dev account as the app itself.
  - Now when we execute the script, the authentication has to be provided to the account where the calendar was created. Basically, we allow a dev app to access our calendar and we authenticate to give that app access to our calendar.
  - Because the edits from the script is also done by the dev, we use dev account for everything.
  - Conclusion - To keep it all simple, use the same google account to create the app, calendar, and the authentication.
- Step 8 - Run the script once a day manually
  - This is up and running.
  - If you manually run this command once a day, this will fetch new contests, and add them to calendar.
  - This is still cumbersome, because we still have to manually run the script everyday. We would like to setup this as a cron job, so it runs once a day and automatically updates our calendar.

### Part 3 - Setting up the cron job

We need to setup a cron job. For this we'll need a service account from google to interact with our API aka server to server interaction.

- Step 1 - create a project manually
  - Every API in google console is accessed on per project basis.
  - First create a project by going to [Google developer's console](https://console.developers.google.com/projectcreate). Create a new project with any name. We'll use this project to obtain google calendar API credentials.
  - we'll name the project `codechef-contest-calendar` for now
- Step 2 - Enable the google calendar API
  - Enable the [google calendar API](https://console.developers.google.com/apis/library/calendar-json.googleapis.com) in this project.
  - This API provides 1 million queries per day for free, so we don't need to worry about billing for now.
  - You can manage this newly enabled google calendar API by going [here](https://console.developers.google.com/apis/api/calendar-json.googleapis.com/overview)
- Step 3 - Obtain credentials
  - You might be prompted to create credentials on [this screen](https://console.developers.google.com/apis/api/calendar-json.googleapis.com/overview)
  - Go to [API and Services section](https://console.developers.google.com/apis/credentials)
  - create credentials, choose `create service account key`
  - create a new service account for this project, choose key type JSON and create key
  - service accounts are used to programmatically access APIs and user data
  - download and save this file in `secrets` directory with filename `credentials_service_account.json`
- Step 4 - obtain calendar secrets
  - This is same as done in basic app setup
  - rename `sample_calendar_secrets.json` to `calendar_secrets.json`
  - fill calendar id (can be found in your calendar settings. go to [all calendars](https://calendar.google.com/calendar/b/1/r) and use three dots beside calendar name to go in settings)
- Step 5 - giving calendar permission to service account
  - Go to your calendar settings, go to `share it with specific people` and share it with service account by entering the service account email id
  - You can find the service account email [here](https://console.cloud.google.com/iam-admin/serviceaccounts). Use the same service account we created in basic app setup above
  - in google calendar, add id of service account
- Step 6 - change config
  - find the `config.py` file in `src` directory
  - make sure the `script mode` is `service_account`
  - events you can choose either `dummy` or actual `codechef events`
- Step 7 - Testing
  - everything is setup now
  - going in `src` folder and running `python main.py` should work
  - If it throws a error, debug it first
  - If everything worked correctly, events should be reflected in google calendar
- Step 8 - Setting up cron job
  - we'll use github actions for this, they are simpler to use here instead of gcp cron jobs.
  - But we dont want our keys to be exposed, so we'll encrypt them and upload to github and add our decryption key to the project secrets in github repo settings. [Read more here](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets)
  - First set a key as environment variable in your local machine, use `export LARGE_SECRET_PASSPHRASE=YOUR_SECRET_KEY`
  - Go to github repo settings, add secrets a with key as `LARGE_SECRET_PASSPHRASE` and value as `YOUR_SECRET_KEY`
  - Then go to `secrets` directory on your local machine, run `chmod +x encrypt_secrets.sh`, then `./encrypt_secrets.sh`
  - This will create `*.gpg` files, we can safely commit them to github
  - `Your secret key` should preferably be long, probabaly 30-40 chars
  - After this, we need to create a workflow. Luckily it is already created in this repo, that will work as it is. Find it in `.github/workflows/cron-job.yml`
  - We've configured it to run once a day at 00:00

To share the calendar, simply share the public calendar link (can be found in your calendar settings)

### Part 4 - Setting up slack notifications

Websites usually changes their structure often. Even minor changes like adding newlines can break scrapers. And our scraper runs unmonitored once a day. We would like to setup a slack notification for when the cron run fails, so we know something has gone wrong. In most case, runs will fail when there has been changes to codechef website contest page.

I'll use [this](https://github.com/voxmedia/github-action-slack-notify-build) handy github action to create slack notifications. You might want to skim through its readme.

- step 1 : setting up the slack app
  - To use this GitHub Action, you'll need a [Slack bot token](https://api.slack.com/docs/token-types). A bot token must be associated with a Slack app, so we will need to create a slack app.
  - **Login to slack** Login to slack with a email id. Create a slack workspace if you don't already have one. Create a channel in it with name `codechef-contest-calendar`.
  - **Create an app.** Go to [Slack's developer site](https://api.slack.com/) then click "Create an app". Name the app anything and make sure your just desoired Slack workspace is selected under "Development Slack Workspace".
  - **Add a Bot user.** Browse to the "Bot users" page listed in the sidebar. Name your bot "codechef-calendar-bot" (you can change this later) and leave the other default settings as-is.
  - **Set an icon for your bot.** Browse to the "Basic information" page listed in the sidebar. Scroll down to the section titled "Display information" to set an icon.
  - **Install your app to your workspace.** At the top of the "Basic information" page, you can find a section titled "Install your app to your workspace". Click on it, then use the button to complete the installation.
- step 2 : adding the bot token to github secrets
  - **Obtain the bot token** Browse to "Install apps" in your app setting and you'll find the Bot User OAuth Access Token. Bot user token strings begin with `xoxb-`.
  - Add this token to the github project secrets. Same as we did earlier with decryption key of our secrets. name the key as `SLACK_BOT_TOKEN` and value is the string starting from `xoxb-`
- step 3 : Invite your bot to your slack channel
  - Go to channel details for the channel we just create in step 1
  - Scroll down, go to add people, type the name of your bot ( `codechef-calendar-bot` in our case ) and add it to channel. We've now added the bot to our channel.
- step 4 : That's all
  - This token will be used in the already written workflow yml file.
  - Now you'll immediately receive notification if your cron job run fails anyday.

</details>
