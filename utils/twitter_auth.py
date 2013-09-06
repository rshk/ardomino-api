#!/usr/bin/env python

import os
from twython import Twython

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

if CONSUMER_KEY is None or CONSUMER_SECRET is None:
    raise ValueError(
        "You must pass CONSUMER_KEY and CONSUMER_SECRET in the env")

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET)
auth = twitter.get_authentication_tokens()

OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

print "Now visit {} and give me the PIN.".format(auth['auth_url'])
oauth_verifier = raw_input("PIN: ")

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
final_step = twitter.get_authorized_tokens(oauth_verifier)

OAUTH_TOKEN = final_step['oauth_token']
OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']
twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

twitter.verify_credentials()
user_info = twitter.get_account_settings()
print("## You're now logged in as {}"
      "".format(user_info['screen_name']))

print """\
## Your Twitter authentication tokens
OAUTH_TOKEN = {oauth_token!r}
OAUTH_TOKEN_SECRET = {oauth_token_secret!r}
""".format(
    oauth_token=final_step['oauth_token'],
    oauth_token_secret=final_step['oauth_token_secret'])
