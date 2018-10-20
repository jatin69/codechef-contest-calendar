# TODO

### Notable things

- The site's contest page changes very very often. Can't rely for dates. Cron job needs to be run daily atleast.
- Because the date time is unreliable, change the `constant calendar ID` to use only `contest code` and not date and time.

### todo List

- [X] Make a basic readme file to tell users how to add this calendar to their own
- [ ] Make a good detailed readme file for devs.
- [x] ADD A way to stop duplicate event addition. Use custom ID while adding events. Then read events & skip id's.
- [x] custom ids need a specific format
- [x] clean code file
- [x] remove useless contests
- [X] Implement a delete all function as well, just in case
- [ ] detect if contests are extended. GOOD FEATURE.
- [X] provide a simplied `ADD TO CALENDAR` button
- [ ] find a way to `insert` events without google authentication everytime. Possibly with a service account.
- [x] Dont upload credentials and token on github. make gitignore
- [ ] `cron jobs` work can be done either in AWS Lambda + cloudwatch events or GCP.
      Both are managed services. Both have a decent free tier.
      AWS has ease of use.
      GCP has inbuilt handling of service account. Might be handy.
      Both AWS & GCP is safe. But be careful be confidential data.

### Some links

- [Cloud console](https://console.cloud.google.com/appengine?folder=true&organizationId=true&project=codechef-calenda-1539932234083&serviceId=default&duration=PT1H) and [Cloud SDK](https://cloud.google.com/sdk/docs/quickstart-linux)
- [cron jobs](https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml)
- [Oauth2](https://developers.google.com/calendar/auth#perform-google-apps-domain-wide-delegation-of-authority) and [oauth2 2L](https://developers.google.com/identity/protocols/OAuth2ServiceAccount)
- [AWS cron jobs docs](https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html) and [tutorial](https://medium.com/blogfoster-engineering/running-cron-jobs-on-aws-lambda-with-scheduled-events-e8fe38686e20)
