import json
from twitterClient import Client

# The consumer secret is an example and will not work for real requests
# To register an app visit https://dev.twitter.com/apps/new
CONSUMER_KEY = 'Sg6JxAqhYdyb7Fb6sIFHQ'
CONSUMER_SECRET = '4NjRM9MHw0bBB8KykRvIV2FyyoOUaQYXzZa4KGW4XX0'

client = Client(CONSUMER_KEY, CONSUMER_SECRET)

# Pretty print of tweet payload
tweet = client.request('https://api.twitter.com/1.1/statuses/show.json?id=434442310127222784')
print json.dumps(tweet, sort_keys=True, indent=4, separators=(',', ':'))

# Show rate limit status for this application
status = client.rate_limit_status()
print status['resources']['search']