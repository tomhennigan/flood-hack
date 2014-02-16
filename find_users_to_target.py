from twitterClient import Client
from urllib import urlencode
import json
import requests
from volunteers import get_volunteers, points_within_distance, Point
import os.path

# Severities.
SEVERE_WARNING = 1
WARNING = 2
ALERT = 3
WARNING_NO_LONGER_IN_FORCE = 4
MONITORED_LOCATION = 5


def get_flood_warning_locations(severity=None):
    """Returns a generator that yields [lat, lng] pairs for affected areas.

    :param shoothill_file: the shoothill update file to use.
    :param severity: an optional value to filter results by severity.
    :returns: a generator of [lat, lng] points.
    """

    # with open('shoothill_floods.json', 'r') as fp:
    #     areas = json.load(fp)

    r = requests.get(
        'http://dbec32afb59243e0a83d0216b56eccce.cloudapp.net/api/Floods',
    )

    areas = r.json()

    for area in areas:
        if severity is None or area['Severity'] == severity:
            yield (area['Center']['Latitude'], area['Center']['Longitude'])


def _get_twitter_usernames_inside(consumer_key, consumer_secret, lat, lon, radius):
    client = Client(consumer_key, consumer_secret)

    seen_screen_names = set()

    lat = '%.10f' % lat
    lon = '%.10f' % lon

    params = {
        'count': '10000',
        'q': cli_args.twitter_query,
        'geocode': ','.join([lat, lon, radius]),
        'result_type': 'recent',
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

def get_twitter_users(consumer_key, consumer_secret, radius_miles, locations):
    seen_usernames = set()

    for search_lat, search_lng in locations:
        distance = '%dmi' % (radius_miles)

        twitter_users = _get_twitter_usernames_inside(
            consumer_key,
            consumer_secret,
            search_lat,
            search_lng,
            distance
        )

        for username, (lat, lng) in twitter_users:
            if username in seen_usernames:
                continue
            else:
                seen_usernames.add(username)

            yield username, (lat, lng)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--volunteer-distance', type=int, default=15000)
    parser.add_argument('--donut-inner-distance', type=int, default=8)  # Currently not used.
    parser.add_argument('--donut-outer-distance', type=int, default=10)
    parser.add_argument('--flood-warning-severe', action='store_true', default=True)
    parser.add_argument('--flood-warning-warning', action='store_true')
    parser.add_argument('--flood-warning-alert', action='store_true')
    parser.add_argument('--no-flood-warning-severe', dest='flood_warning_severe', action='store_false')
    parser.add_argument('--no-flood-warning-warning', dest='flood_warning_warning', action='store_false')
    parser.add_argument('--no-flood-warning-alert', dest='flood_warning_alert', action='store_false')
    parser.add_argument('--twitter-query', type=str, default='')
    parser.add_argument('--twitter-consumer-key', type=str, required=True)
    parser.add_argument('--twitter-consumer-secret', type=str, required=True)

    cli_args = parser.parse_args()

    # Figure out requested severities.
    severities = []
    if cli_args.flood_warning_severe:
        severities.append(SEVERE_WARNING)

    if cli_args.flood_warning_warning:
        severities.append(WARNING)

    if cli_args.flood_warning_alert:
        severities.append(ALERT)

    # So we don't spam people.
    seen_twitter_users = set()

    for severity in severities:
        volunteers = list(get_volunteers())
        locations = get_flood_warning_locations(severity=severity)

        users = get_twitter_users(
            cli_args.twitter_consumer_key,
            cli_args.twitter_consumer_secret,
            cli_args.donut_outer_distance,
            locations
        )

        for twitter_user, (twitter_user_lat, twitter_user_lng) in users:
            if twitter_user in seen_twitter_users:
                continue
            else:
                seen_twitter_users.add(twitter_user)

            local_volunteers = points_within_distance(
                Point(lat=twitter_user_lat, lng=twitter_user_lng),
                volunteers,
                cli_args.volunteer_distance
            )
            num_volunteers = sum(1 for _ in local_volunteers)
            print "%s\t%d\t%d" % (twitter_user, severity, num_volunteers)
