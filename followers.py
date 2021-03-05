import requests
import os
import json
import pickle
from datetime import datetime


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

from dotenv import load_dotenv

def savestate(mys, varn, scrl):
    #TODO write out to a tmp file then move into place
    # in order to transact atomically
    with open(mys.format(varn, 'pickle'), 'wb') as output:
        pickle.dump(scrl, output, 4)

def loadstate(mys, varn):
    retval={}
    if os.path.isfile(mys.format(varn, 'pickle')):
        with open(mys.format(varn, 'pickle'), 'rb') as readin:
            retval=pickle.load(readin)
    return retval


def create_url(user_id, ctype):
    ''' user_id = twitter (numeric) user ID
        ctype = 'followers' or 'following'
        '''
    return "https://api.twitter.com/2/users/{}/{}".format(user_id, ctype)

def get_params():
    return {"user.fields": "public_metrics,created_at", "max_results": 1000}

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_paginated(url, headers, params):
    retval = []
    more = 'firstrun'
    while more:
        if more != 'firstrun':
            params['pagination_token'] = more
        response = requests.request("GET", url, headers=headers, params=params)
        if response.status_code != 200:
            # TODO staus code 429 need to look at x-rate-limit-reset header for waiting
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )

        got = response.json()
        retval.extend(got['data'])
        if 'next_token' in got['meta']:
            more = got['meta']['next_token']
        else:
            more = False
    return retval

def response_to_dict(json_data):
    '''
    Convert the json list into a dict keyed by uid
    :param json_response: list of json response data items
    :return: dict keyed by id
    '''
    retval = {}
    for u in json_data:
        retval[u['id']] = u

    return retval


def logcompare(mys, varn, oldd, newd):
    '''
    Compare previous and current user dicts
    :param mys: storage location format spec
    :param varn: which variant (followers/following)
    :param oldd: old dict
    :param newd: new dict
    :return: list of changes
    '''
    retval = []

    if varn == 'followers':
        fgone = 'Unfollowed by @{} [ID:{} Name:{}]'
        fnew  = 'Newly followed by @{} [ID:{} Name:{}]'
    else:
        fgone = 'Stopped Following @{} [ID:{} Name:{}]'
        fnew = 'Started Following @{} [ID:{} Name:{}]'

    # walk old list
    for uid in oldd.keys():
        if uid not in newd:
            #unfollowed
            retval.append(fgone.format(oldd[uid]['username'], uid, oldd[uid]['name']))

    # walk new list
    for uid in newd.keys():
        if uid not in oldd:
            retval.append(fnew.format(newd[uid]['username'], uid, newd[uid]['name']))
        # TODO could track name changes here

    now = datetime.now()
    tst = now.strftime("%Y-%m-%d %H:%M:%S")

    if retval:
        with open(mys.format(varn, 'log'), 'a') as output:
           for msg in retval:
               output.write('{} {}\n'.format(tst, msg))


    return retval


def main():

    # Load .env file.
    # This does not override existing env vars
    load_dotenv()

    # TB_STORAGE lets you move the storage format
    saveat = os.environ.get("TB_STORAGE", "tb.{}.{}")

    # env BEARER_TOKEN must be set.
    # TODO ensure that os.environ.get tracebacks if unset
    bearer_token = os.environ.get("BEARER_TOKEN")
    headers = create_headers(bearer_token)

    # TWITTER_UID probably should be set.  But we will use @jack if you don't set it.
    uid = os.environ.get("TWITTER_UID", "12")

    params = get_params()




    for ltype in ('following', 'followers'):

        url = create_url(uid, ltype)
        json_data = connect_paginated(url, headers, params)
        new_ud = response_to_dict(json_data)

        old_ud = loadstate(saveat, ltype)

    #   Do stuff
        changelog = logcompare(saveat, ltype, old_ud, new_ud)


        print('foo')

        savestate(saveat, ltype, new_ud)

    print('bar')

if __name__ == "__main__":
    main()
