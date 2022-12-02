#!/usr/bin/env python
from mastodon import Mastodon
import os
import sys
import re

# https://medium.com/@martin.heinz/getting-started-with-mastodon-api-in-python-9f105309ed43

def process_follows(token, host):
    '''Retrieve a followers object and return a list of usernames'''
    source = Mastodon(access_token=token, api_base_url=f"https://{host}")
    source_follows_raw = source.account_following(source.account_verify_credentials()["id"])
    accounts = []
    for i in source_follows_raw:
        print(f"username: {i['username']}, account: {i['acct']}, id: {i['id']}")
        result = re.search(r'(.*)@(.*)$', i["acct"])
        if not result:
            accounts.append(f"{i['username']}@{host}")

        else:
            accounts.append(i["acct"])
    return accounts


# read source data from env vars
source_host = os.environ.get("SOURCE_MASTODON")
if not source_host:
    sys.exit("ERROR: no environment variable SOURCE_MASTODON configured!")
    
source_token = os.environ.get("SOURCE_MASTODON_TOKEN")
if not source_token:
    sys.exit("ERROR: no environment variable SOURCE_MASTODON_TOKEN configured!")

# read target data from env vars
target_host = os.environ.get("TARGET_MASTODON")
if not target_host:
    sys.exit("ERROR: no environment variable TARGET_MASTODON configured!")

target_token = os.environ.get("TARGET_MASTODON_TOKEN")
if not target_token:
    sys.exit("ERROR: no environment variable TARGET_MASTODON_TOKEN configured!")


def main ():
    # collect source follows
    source_follows = process_follows(source_token, source_host)
    # print(source_follows)
    target_follows = process_follows(target_token, target_host)
    # print(target_follows)
    all_follows = source_follows + target_follows
    all_follows = list(set(all_follows))
    # print(all_follows)
    print("missing from source:")
    source_missing = list(set(all_follows) - set(source_follows))
    print(source_missing)
    print(f"attempting to update source follows on {source_host}")
    for i in source_missing:
        print(f"adding {i} to source follows")
        source = Mastodon(access_token=source_token, api_base_url=f"https://{source_host}")
        source.account_follow(i)
        # source.follows(i)
    target_missing = list(set(all_follows) - set(target_follows))
    print("missing from target:")
    print(target_missing)

if __name__ == "__main__":
    # create()
    main()