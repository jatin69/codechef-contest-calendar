# Web scraping imports
import requests
from bs4 import BeautifulSoup

import pprint

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
    # past contests need not be added to calendar
    # pastContests = allContestsEver[2]

    # ignoring contest that last more than a year
    # new ones will be handled by year subtraction logic below 
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


# Stand-alone script part
if __name__ == '__main__':
    codechef_contests = fetchContests()
    pprint.pprint(codechef_contests)


