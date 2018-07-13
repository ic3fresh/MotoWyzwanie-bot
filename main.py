#!usr/bin/python3

import json
import requests
import os
import re

DEBUG = False

# API_TOKEN = os.environ["API_TOKEN"]
API_URL = "http://127.0.0.1:4567/api/"  # "https://paciak.pl/api/"
TOKEN = {"Authorization": "Bearer ciach"}
score_page_url = 'topic/44/punktacja'
category_page_url = 'category/7/motowyzwanie?page={0}'


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


def get_score_page():
    return json.loads(call_to_api(score_page_url).text)["posts"][0]['content'].split('\n')


def get_category_page(current_page_number):
    return json.loads(call_to_api(category_page_url.format(current_page_number)).text)


USERNAME_REGEXP = re.compile('@[^<]+')
USERPOINTS_REGEXP = re.compile('\ \d+')
CHALLENGE_NUMBER_REGEXP = re.compile('MotoWyzwanie.*\#[^<]+')
CHALLENGE_LINK_REGEXP = re.compile('http[^\"]+')
TOPIC_NUMBER_REGEXP = re.compile('\d+')

points = []
finished_challenges = []
topics_list = []
new_challenges_list = topics_list


def create_actual_points_list():
    for line in get_score_page():
        if line == '</ol>':
            break
        if not USERPOINTS_REGEXP.search(line):
            pass
        else:
            points.append(
                [USERNAME_REGEXP.search(line).group(0), USERPOINTS_REGEXP.search(line).group(0).replace(" ", "")])


def create_finished_challenges_list():
    for line in get_score_page():
        if not CHALLENGE_NUMBER_REGEXP.search(line):
            pass
        if 'MotoWyzwanie' not in line:
            pass
        else:
            finished_challenges.append(
                [CHALLENGE_NUMBER_REGEXP.search(line).group(0), CHALLENGE_LINK_REGEXP.search(line).group(0),
                 USERNAME_REGEXP.search(line).group(0)])


def create_topics_list():
    active_page = 1
    page_count = get_category_page(active_page)["pagination"]["pageCount"]
    while active_page <= page_count:
        for topic in get_category_page(active_page)["topics"]:
            if not TOPIC_NUMBER_REGEXP.search(topic["title"]):
                pass
            else:
                topics_list.append(topic["title"])
        active_page += 1


def check_for_new_challenges():
    for element in finished_challenges:
        for topic in topics_list:
            if TOPIC_NUMBER_REGEXP.search(topic):
                topic_number = int(TOPIC_NUMBER_REGEXP.search(topic).group(0))
            else:
                pass
            if topic_number == int(TOPIC_NUMBER_REGEXP.search(element[0]).group(0)):
                new_challenges_list.remove(topic)



def main():
    create_finished_challenges_list()
    create_topics_list()
    check_for_new_challenges()
    print(new_challenges_list)


if __name__ == "__main__":
    main()
