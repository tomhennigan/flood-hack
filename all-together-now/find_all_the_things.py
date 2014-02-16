from twitterClient import Client
from urllib import urlencode
import argparse
import json
import requests
from volunteers import get_volunteers, points_within_distance, Point
import os.path


class Severity:
    SEVERE_WARNING = 1
    WARNING = 2
    ALERT = 3
    WARNING_NO_LONGER_IN_FORCE = 4
    MONITORED_LOCATION = 5

parser = argparse.ArgumentParser()
parser.add_argument('--donut-inner-distance', type=int, default=8)
parser.add_argument('--donut-outer-distance', type=int, default=10)
parser.add_argument('--flood-warning-severity', type=int, default=Severity.SEVERE_WARNING)

parser.add_argument('--twitter-query', type=str, default='')
parser.add_argument('--twitter-consumer-key', type=str, required=True)
parser.add_argument('--twitter-consumer-secret', type=str, required=True)

cli_args = parser.parse_args()


def _shoothill_api_floods():
    """Nasty hacks to access the shoothill API.

    :returns: a list of areas affected by flooding.
    """

    r = requests.get(
        'http://dbec32afb59243e0a83d0216b56eccce.cloudapp.net/api/Floods',
    )

    return r.json()


def get_flood_warning_locations(severity=None):
    """Returns a generator that yields [lat, lng] pairs for affected areas.

    :param shoothill_file: the shoothill update file to use.
    :param severity: an optional value to filter results by severity.
    :returns: a generator of [lat, lng] points.
    """

    # with open('shoothill_floods.json', 'r') as fp:
    #     areas = json.load(fp)

    areas = _shoothill_api_floods()

    for area in areas:
        if severity is None or area['Severity'] == severity:
            yield (area['Center']['Latitude'], area['Center']['Longitude'])




#location = Location(consumer_key, consumer_secret)

def get_user_name_near_lat_long(lat, lon, radius):
    client = Client(
        cli_args.twitter_consumer_key,
        cli_args.twitter_consumer_secret
    )

    seen_screen_names = set()

    lat = '%.10f' % lat
    lon = '%.10f' % lon
    # radius = '%.10f' % radius

    params = {
        'count': '10000',
        'q': cli_args.twitter_query,
        'geocode': ','.join([lat, lon, radius])
    }

    url = 'https://api.twitter.com/1.1/search/tweets.json?' + urlencode(params.items())

    data = client.request(url)

    for status in data['statuses']:
        if status['geo'] is None:
            continue

        if status['geo']['type'] != 'Point':
            continue

        screen_name = status['user']['screen_name']

        if screen_name in seen_screen_names:
            continue
        seen_screen_names.add(screen_name)

        lat = status['geo']['coordinates'][0]
        lon = status['geo']['coordinates'][1]
        yield screen_name, (lat, lon)

def get_twitter_users(locations):

    if os.path.exists('twitter_users.json'):
        with open('twitter_users.json', 'r') as fp:
            for line in fp:
                yield json.loads(line)
        return

    seen_usernames = set()

    for search_lat, search_lng in locations:
        distance = '%dmi' % (cli_args.donut_outer_distance)

        for username, (lat, lng) in get_user_name_near_lat_long(search_lat, search_lng, distance):
            if username in seen_usernames:
                continue

            seen_usernames.add(username)
            yield username, (lat, lng)


volunteers = get_volunteers()
locations = get_flood_warning_locations(severity=cli_args.flood_warning_severity)

for twitter_user, (twitter_user_lat, twitter_user_lng) in get_twitter_users(locations):
    print twitter_user, (twitter_user_lat, twitter_user_lng)

