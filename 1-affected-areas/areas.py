import json
import requests


class Severity:
    SEVERE_WARNING = 1
    WARNING = 2
    ALERT = 3
    WARNING_NO_LONGER_IN_FORCE = 4
    MONITORED_LOCATION = 5


def _shoothill_api_floods():
    """Nasty hacks to access the shoothill API.

    :returns: a list of areas affected by flooding.
    """

    r = requests.get(
        'http://dbec32afb59243e0a83d0216b56eccce.cloudapp.net/api/Floods',
    )

    return r.json()


def get_affected_areas(severity=None):
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

if __name__ == '__main__':
    for lat, lng in get_affected_areas(severity=Severity.SEVERE_WARNING):
        print json.dumps([lat, lng])

