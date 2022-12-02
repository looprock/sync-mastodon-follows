# sync-mastodon-follows
This script syncs follows between primary and secondary Mastodon accounts

# Setup

1) create an Application on the mastodon servers you want to sync called 'sync-mastodon-follows', following the directions here: https://martinheinz.dev/blog/86
2) create a toml configuration under ~/.sync-mastodon-follows.conf using the example file and the tokens from the Applications you created
3) run: `poetry init` then `poetry shell`
4) run: `./sync-mastodon-follows.py`

# Caveats

Currently, due to how Mastodon does account forwarding, search results are handled, and other potential problems, sometimes multiple entries will be found for the same user. I couldn't think of a clean way to determine programatically which user is correct, so I don't try to. Instead I throw an error and present the data. The 'fix' for handling these cases is to manually verify you're following the right account and add that user to the ignore list in the configuration file. 

For example, if you ge the following output:
```
adding foobar@sackheads.social to hachyderm.io follows
#### ERROR: search for foobar@sackheads.social resulted in multiple results, aborting. Found:
#### found account: foobar@sackheads.social, display name: foobar
#### found account: foobar@twitterbridge.jannis.rocks, display name: foobar
```

1) log into hachyderm.io and search for foobar@sackheads.social and follow/make sure you're following the correct person
2) disable future attempts by updating the hachyderm.io section of the config with: 

`ignore = ["foobar@sackheads.social"]`


Sorry it's the best I could think of right now.

I think this script is likely double-processing things. I'll try to fix it at some point, but my intention for this is just to run it occasionally to push new follows to my secondary mastodon account as a sort of backup, so it's not really designed to be performant, so I might also not fix it. :)