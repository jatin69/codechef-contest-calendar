# Google Calendar API imports
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials

import pprint
import sys

def authenticateServiceAccount():
    """
    Purpose - obtain credentials by authenticating via service account (programmatically)    
    Returns - the credentials object
    """

    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/calendar/quickstart/python

    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials_service_account.json', scopes=SCOPES)
    return credentials


if __name__ == '__main__':
    credentials = authenticateServiceAccount()
    print(credentials)