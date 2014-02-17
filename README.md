FludBudUK
=========

**Find users to target:**

```bash
python find_users_to_target.py \
	--twitter-consumer-key=$consumer_key \
	--twitter-consumer-secret=$consumer_secret \
	--flood-warning-severe \
	--flood-warning-warning \
	--flood-warning-alert > users.txt
```

**Prioritise them as you want:**

```python
sort -k2n -k3nr -k1 users.txt | cut -f1 -f3 > users_sorted.txt
```

**Send messages to all matched users:**

You need:

* Twitter API Details
* Three files in `pusher/input/`:
    * `users.txt`: Tab separated txt file containing a list of twitter usernames and nearby volunteer counts.
    * `messages.txt`: A txt file listing messages templates with two "%s" for replacing with twitter username and volunteer counts.
    * `blacklist.txt`: Users you don't want to send to. Successfully sent messages will have usernames added here.

```bash
./run.sh \
	--consumer_key=$consumer_key \
	--consumer_secret=$consumer_secret \
	--access_token_key=$access_key \
	--access_token_secret=$access_secret \
	--sleep_time=60 \
	[--dry_run=true]
```
