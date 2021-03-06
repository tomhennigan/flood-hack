import twitter
import time
import argparse
import sys
import logging

from random import choice

parser = argparse.ArgumentParser(description='Twitter Poster')

parser.add_argument('--consumer_key', help='Consumer Key', default="", required=True)
parser.add_argument('--consumer_secret', help='Consumer Secret', default="", required=True)
parser.add_argument('--access_token_key', help='Access Token Key', default="", required=True)
parser.add_argument('--access_token_secret', help='Access Token Secret', default="", required=True)
parser.add_argument('--sleep_time', help='How long to wait between tweets (seconds)', default="", required=True, type=int)
parser.add_argument('--dry_run', help='Print the tweets instead of actually sending them. Blacklist is still written!', default=False)

args = parser.parse_args()

log = logging.getLogger()
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.DEBUG)
log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)

users_to_send = open("input/users.txt").readlines()
users_blacklist = open("input/blacklist.txt", "r").readlines()
message_templates = open("input/messages.txt").readlines()


def tweet(message, log, dry_run):
    api = twitter.Api(
        consumer_key=args.consumer_key,
        consumer_secret=args.consumer_secret,
        access_token_key=args.access_token_key,
        access_token_secret=args.access_token_secret
    )

    try:
        if dry_run:
            log.debug("DRY RUN!")
            response = message
            log.debug(message)
        else:
            response = api.PostUpdates(message)
    except Exception, e:
        log.error("FAIL: Unable to send tweet \"%s\" : %s" % (message, e))
        response = False

    return response

def format_user(ts_user):
    return ts_user.split('\t')

def format_message(message_templates, user, count, retry_counter=0):
    """
    Pick a message from the message pool at random.
    If the message is over the max twitter message length, recursively try again 10 times
    before giving up.
    """
    message = choice(message_templates).split('\n')[0] % (user, count)

    if len(message) > 140:
        if retry_counter <= 10:
            retry_counter += 1
        else:
            return False

        return format_message(message_templates, user, count, retry_counter)

    return message


def add_blacklist(user, log):
    try:
        blacklist = open("input/blacklist.txt", "a")
        print >> blacklist, "%s\n" % user
        blacklist.close()
        return True
    except Exception, e:
        print e
        log.error("Unable to write to blacklist for %s" % user)
        return False


cleaned_blacklist = map(lambda line: line.rsplit("\n")[0], users_blacklist)

for user in users_to_send:
    user_and_count = format_user(user)

    if user_and_count[0] not in cleaned_blacklist:
        message = format_message(message_templates, user_and_count[0], user_and_count[1])

        if message:
            tweet_response = tweet(message, log, args.dry_run)

            if tweet_response:
                if not add_blacklist(user_and_count[0], log):
                    sys.exit()

                log.info("SUCCESS: \"%s\" to %s" % (message, user_and_count[0]))

                time.sleep(args.sleep_time)
        else:
            log.warning("SKIPPING %s: %s - Message too long and too many retries." % (user_and_count[0], message))
    else:
        log.warning("SKIPPING %s: Blacklist hit." % user_and_count[0])
log.warning("End of input")



