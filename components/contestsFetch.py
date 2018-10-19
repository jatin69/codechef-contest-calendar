# Web scraping imports
import requests
from bs4 import BeautifulSoup

# codechef Contests URL : Replace with config when integrating
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
    # pastContests = allContestsEver[2]
    ignoredContests = ['INOIPRAC', 'ZCOPRAC']

    # Make a list of active and upcoming contests
    requiredContests = []
    requiredContests.extend(activeContests.find("tbody").find_all("tr"))
    requiredContests.extend(upcomingContests.find("tbody").find_all("tr"))

    events = []
    for contest in requiredContests:
        tds = contest.find_all("td")
        events.append({
            'contestCode': tds[0].text,
            'contestLink': 'https://www.codechef.com{0}'.format(tds[1].next.attrs['href'].split('?')[0]),
            'contestTitle': tds[1].text,
            'contestStartDate': tds[2].attrs['data-starttime'],
            'contestEndDate': tds[3].attrs['data-endtime']
        })
        if tds[0].text in ignoredContests:
            events.pop()

    return events


print(fetchContests())
