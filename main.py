#!/usr/bin/env python
from mastodon import Mastodon
import os
import sys
import re
import tomli

# TODO: handle pagination, I'm not getting more than 40 results back

homedir = os.path.expanduser("~")
toml_config = f"{homedir}/.sync-mastodon-follows.conf"
if not os.path.isfile(toml_config):
    sys.exit("ERROR: config file not found, please create ~/.sync-mastodon-follows.conf")


# https://medium.com/@martin.heinz/getting-started-with-mastodon-api-in-python-9f105309ed43

def process_follows(token, host):
    '''Retrieve a followers object and return a list of usernames'''
    source = Mastodon(access_token=token, api_base_url=f"https://{host}")
    # print(f"my id:{source.account_verify_credentials()['id']}")
    source_follows_raw = source.account_following(source.account_verify_credentials()["id"])
    accounts = []
    for i in source_follows_raw:
        # print(f"username: {i['username']}, account: {i['acct']}, id: {i['id']}")
        result = re.search(r'(.*)@(.*)$', i["acct"])
        if not result:
            accounts.append(f"{i['username']}@{host}")

        else:
            accounts.append(i["acct"])
    return accounts

def follow_accounts(accounts: list, host, token: str):
    for i in accounts:
        print(f"adding {i} to {host} follows")
        result = re.search(r'(.*)@(.*)$', i)
        if result.groups()[1] == host:
            i = result.groups()[0]
            print(f"{i} is already on this instance, removing @{host}")
        endpoint = Mastodon(access_token=token, api_base_url=f"https://{host}")
        results = endpoint.account_search(i)
        if len(results) == 0:
            print(f"#### ERROR: no results for {i}")
        elif len(results) > 1:
            print(f"#### ERROR: search for {i} resulted in multiple results, aborting. Found:")
            for e in results:
                print(f"#### found account: {e['acct']}, display name: {e['display_name']}")
        else:
            endpoint.account_follow(results[0]['id'])

def main ():
    with open(toml_config, mode="rb") as f:
        config = tomli.load(f)
    sites = list(config.keys())
    follows = {}
    for site in sites:
        print(f"processing {site}")
        site_res = process_follows(config[site]["token"], site)
        print(f"found {len(site_res)} follows on {site}")
        follows[site] = site_res
    
    all_follows = []
    for site in sites:
        all_follows = follows[site] + all_follows
    
    all_follows = list(set(all_follows))

    for site in sites:
        missing = list(set(all_follows) - set(follows[site]))
        missing = list(set(missing) - set(config[site]["ignore"]))
        follow_accounts(missing, site, config[site]["token"])

if __name__ == "__main__":
    main()
