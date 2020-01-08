"""
Event id - 
Opaque identifier of the event. 
When creating new single or recurring events, you can specify their IDs. 
Provided IDs must follow these rules:
- characters allowed in the ID are those used in base32hex encoding, i.e. lowercase letters a-v and digits 0-9, see section 3.1.2 in RFC2938
- the length of the ID must be between 5 and 1024 characters
- the ID must be unique per calendar
"""

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

def getUniqueIdForContest(contestCode, startDate, endDate):
    return 'thecodechefcalendarcontestidis_' + tobase32hex(contestCode)

x = getUniqueIdForContest('OCT18','2018-10-20T11:00:00+05:30','2018-10-20T11:00:00+05:30' )
print(x)
