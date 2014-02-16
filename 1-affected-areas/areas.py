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

    ASPXAUTH = 'EE3F15872589517DFFD89C1767C70BDC389EFE72786842F7D4690E7CC9D4E35B6D2E0FB139726A36714A0A1C4B7074DFB5BB4C2B06080E8F170E333E89E7DFC8DAF8D152B941986AE4D2FC579FE0A41056BA9B72C9E70C3E01CF47E54E33693FCD9A282DFE22A4477571D42AC6156AF0645C0F72'
    r = requests.get(
        'http://apifa.shoothill.com/api/Floods',
        headers={
            'Cookie': 'cc_cookie_accept=cc_cookie_accept; .ASPXAUTH=%s;' % ASPXAUTH
        }
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

