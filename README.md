# sync-mastodon-follows
This script syncs follows between primary and secondary Mastodon accounts

# Setup

1) create an Application on the mastodon servers you want to sync called 'sync-mastodon-follows', following the directions here: https://martinheinz.dev/blog/86

2) create a toml configuration under ~/.sync-mastodon-follows.conf using the example file and the tokens from the Applications you created

# Caveats

Currently, due to Mastodon handles account forwarding among other things and how search results are handled, multiple entries will be found for the same user. I couldn't think of a clean way to figure our programatically how to determine which user is correct, so I don't try to. Instead I throw an error and present the data. The 'fix' for handling these cases is to manually verify you're following the right account and add that user to the ignore list in the configuration file. Sorry it's the best I could think of right now.

I think this script is likely double-processing things. I'll try to fix it at some point, but my intention for this is just to run it occasionally to push new follows to my secondary mastodon account as a sort of backup, so it's not really designed to be performant, so I might also not fix it. :)