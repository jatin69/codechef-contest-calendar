# Google Calendar API imports
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools
from googleapiclient.errors import HttpError

def authenticateUser():
    """
    Purpose - obtain credentials by authenticating via browser
    Returns - the credentials object
    side effect - creates a token.json for consecutive authentications
    """

    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/calendar/quickstart/python

    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/calendar'

    store = file.Storage('token.json')
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('credentials_user.json', SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials


if __name__ == '__main__':
    credentials = authenticateUser()
    print(credentials)