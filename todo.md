# TODO

pipenv run pip freeze > requirements.txt

to make requirements.txt

- [X] detect contest extension time. now more difficult because id exists, so duplicate. 
  - Extension detection logic
    - if duplicate identifier, fetch its details. 
    - if everything is exactly same, do nothing
    - else update the event and reflect the new changes
- It turned out that so-called "delete" operation in fact doesn't delete events, but just hides them and changes their status to "cancelled". So the events continue to exist in Google Calendar.
As workaround I retrieve deleted entries using "showDeleted" = true option and then update them

- [ ] make event date time format more user friendly
- [ ] Write readme for advance devs and setup service account and cron job. do this is mca id

## what i did

- first i made unique event id as - event name + start time + end time
- but this was faulty in a real world case
- because events get extended
- to handle updation, we need same event id
- so i now just use - event name


### Notable things

- The site's contest page changes very very often. Can't rely for dates. Cron job needs to be run daily atleast.
- Because the date time is unreliable, change the `constant calendar ID` to use only `contest code` and not date and time.

### todo List

- [ ] detect if contests are extended. GOOD FEATURE.
- [ ] find a way to `insert` events without google authentication everytime. Possibly with a service account.
- [X] Make a basic readme file to tell users how to add this calendar to their own
- [-] Make a good detailed readme file for devs.
- [x] ADD A way to stop duplicate event addition. Use custom ID while adding events. Then read events & skip id's.
- [x] custom ids need a specific format
- [x] clean code file
- [x] remove useless contests
- [X] Implement a delete all function as well, just in case
- [X] provide a simplied `ADD TO CALENDAR` button
- [x] Dont upload credentials and token on github. make gitignore
- [-] `cron jobs` work can be done either in AWS Lambda + cloudwatch events or GCP.
      Both are managed services. Both have a decent free tier.
      AWS has ease of use.
      GCP has inbuilt handling of service account. Might be handy.
      Both AWS & GCP is safe. But be careful be confidential data.

### Some reference links

- [Cloud console](https://console.cloud.google.com/appengine?folder=true&organizationId=true&project=codechef-calenda-1539932234083&serviceId=default&duration=PT1H) and [Cloud SDK](https://cloud.google.com/sdk/docs/quickstart-linux)
- [cron jobs](https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml)
- [Oauth2](https://developers.google.com/calendar/auth#perform-google-apps-domain-wide-delegation-of-authority) and [oauth2 2L](https://developers.google.com/identity/protocols/OAuth2ServiceAccount)
- [AWS cron jobs docs](https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html) and [tutorial](https://medium.com/blogfoster-engineering/running-cron-jobs-on-aws-lambda-with-scheduled-events-e8fe38686e20)
