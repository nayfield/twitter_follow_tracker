import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

from dotenv import load_dotenv
# The file '.env' contains two variables we care about:
# BEARER_TOKEN=AAjkldjfdlksjfdskljklfds
# TWITTER_UID=12345


def auth():
    return os.environ.get("BEARER_TOKEN")


def create_url():
    user_id = os.environ.get("TWITTER_UID")
    return "https://api.twitter.com/2/users/{}/followers".format(user_id)


def get_params():
    return {"user.fields": "public_metrics,created_at"}


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def connect_paginated(url, headers, params):
    retval = []
    more = 'firstrun'
    while more:
        if more != 'firstrun':
            params['pagination_token'] = more
        got = connect_to_endpoint(url, headers, params)
        retval.extend(got['data'])
        if 'next_token' in got['meta']:
            print('more', got['meta']['next_token'])
            more = got['meta']['next_token']
        else:
            more = False
    return retval

def main():
    load_dotenv()
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    params = get_params()
    json_response = connect_paginated(url, headers, params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
