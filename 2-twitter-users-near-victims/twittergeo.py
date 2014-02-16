import json
from twitterClient import Client
from urllib import urlencode

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--consumer-key', type=str, required=True)
parser.add_argument('--consumer-secret', type=str, required=True)
args = parser.parse_args()

consumer_key=args.consumer_key
consumer_secret=args.consumer_secret


#location = Location(consumer_key, consumer_secret)

def get_user_name_near_lat_long(lat, lon, radius):
	client = Client(consumer_key, consumer_secret)

	seen_screen_names = set()

	lat = '%.10f' % lat
	lon = '%.10f' % lon
	# radius = '%.10f' % radius

	params = {
		'count': '10000',
		'q': '',
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


distances = [
	# '2mi',
	# '5mi',
	# '10mi',
	'10mi',
]

locations = [
	[51.061632546372024, -2.935403688517919],
	[51.07723695738862, -2.9508876213724142],
	[51.39195734327949, -0.47369593903413265],
	[51.38972325231583, -0.48914085274412866],
	[51.38024227558948, -0.45894696652977773],
	[51.405988430191314, -0.5046219352403924],
	[51.39439891429481, -0.4716284455294148],
	[51.42974919545905, -0.5195557785325841],
	[51.46617420560472, -0.5463796580567679],
	[51.42803574943933, -0.526846231407814],
	[51.459346042280686, -0.5600442193492219],
	[51.48301372774637, -0.5919363857003214],
	[51.45715806457794, -0.5769043435338257],
	[51.45405583641052, -0.5711915934343226],
	[51.46032021950458, -0.5696153529206296],
	[51.48317827987806, -0.5827709814723137],
]

seen_usernames = set()

for distance in distances:
	for search_lat, search_lng in locations:
		for username, (lat, lng) in get_user_name_near_lat_long(search_lat, search_lng, distance):
			if username in seen_usernames:
				continue
			seen_usernames.add(username)

			print username, (lat, lng)

