FludBudUK
=========

**Find users to target:**

```bash
python find_users_to_target.py \
	--twitter-consumer-key $key --twitter-consumer-secret $secret \
	--flood-warning-severe \
	--flood-warning-warning \
	--flood-warning-alert > users.txt
```

**Prioritise them as you want:**

```python
sort -k2n -k3nr -k1 users.txt | cut -f1 -f3 > users_sorted.txt
```

**Send messages to all matched users:**

Code will be pushed soon...
