#!usr/bin/python3

import json
import requests
import os
import re

DEBUG = False

# API_TOKEN = os.environ["API_TOKEN"]
API_URL = "http://127.0.0.1:4567/api/"  # "https://paciak.pl/api/"
API_SLEEP = 1
TOKEN = {"Authorization": "Bearer ciach"}
score_page_url = 'topic/44/punktacja'


# TOKEN = {"Authorization": "Bearer {API_TOKEN}".format(API_TOKEN=API_TOKEN)}

def debug(text):
    """Debug messages"""
    if DEBUG:
        print(text)


def api_url(req):
    return "{0}{1}".format(API_URL, req)


def call_to_api(req):
    response = None
    try:
        debug("In paciak_api: /api/{0}".format(req))
        response = requests.get(api_url(req), headers=TOKEN)
    except requests.status_codes as e:
        print("Oppss, HTTP returned: {0} with: {1}".format(e.code, e.reason))
        print("Check API settings")
        exit(1)
    except requests.status_codes as e:
        print("Oppss, URL error: {0}".format(e.reason))
        exit(2)
    return response


def open_score_page():
    return json.loads(call_to_api(score_page_url).text)


def extract_score_content():
    return open_score_page()["posts"][0]['content']


def get_user_name(data):
    return re.search('(@[^<]+)', data)


def get_user_points(data):
    return re.search('(\ \d+)', data)


def get_challenge_number(data):
    return re.search('(MotoWyzwanie.*\#[^<])', data)


def get_challenge_link(data):
    return re.search('(http[^\"]+)', data)


def divide_by_lines():
    return extract_score_content().split('\n')


points = []


def create_actual_points_list():
    for line in divide_by_lines():
        if line == '</ol>':
            break
        if not get_user_points(line):
            pass
        else:
            points.append([get_user_name(line).group(0), get_user_points(line).group(0).replace(" ", "")])


finished_challenges = []


def create_finished_challenges_list():
    for line in divide_by_lines():
        if not get_challenge_number(line):
            pass
        if 'MotoWyzwanie' not in line:
            pass
        else:
            finished_challenges.append(
                [get_challenge_number(line).group(0), get_challenge_link(line).group(0), get_user_name(line).group(0)])


def main():
    create_actual_points_list()
    create_finished_challenges_list()
    for line in divide_by_lines():
        print(line)
    print(points)
    print(finished_challenges)


if __name__ == "__main__":
    main()
