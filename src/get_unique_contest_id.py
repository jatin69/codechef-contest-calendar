import string 
alphanum = (string.digits+string.ascii_lowercase)[:32]
charMap = {'w' : 'ab', 'x' : 'cd', 'y' : 'ef', 'z' : 'gh'}

def tobase32hex(contestCode):
    res = ''
    for s in contestCode.lower():
        if s in alphanum:
            res += s
        elif s in charMap.keys() :
            res += charMap[s]
        else:
            pass
    return res

def getUniqueIdForContest(contestCode):
    """
    Unique Event id - https://developers.google.com/calendar/v3/reference/events/insert
    
    Opaque identifier of the event. 
    When creating new single or recurring events, you can specify their IDs. 

    - characters allowed in the ID are those used in base32hex encoding, 
    i.e. lowercase letters a-v and digits 0-9
    - the length of the ID must be between 5 and 1024 characters
    - the ID must be unique per calendar

    Lessons - 
    First i used unique id as - contest code + start date + end date
    Butthis was faulty in a real world case because events get extended.
    To handle updation, we need same event id, so i now just use contest code

    """
    return 'thecodechefcalendarcontestidis' + tobase32hex(contestCode)


# Stand-alone script part
if __name__ == '__main__':
    contests = ['jan10','FEB11', 'z1', 'x2']
    for contest_id in contests:
        unique_contest_id = getUniqueIdForContest(contest_id)
        print(unique_contest_id)