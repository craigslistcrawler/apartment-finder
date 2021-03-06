import os
## Price

# The minimum rent you want to pay per month.
MIN_PRICE = 0

# The maximum rent you want to pay per month.
MAX_PRICE = 4000

## Location preferences

# The Craigslist site you want to search on.
# For instance, https://sfbay.craigslist.org is SF and the Bay Area.
# You only need the beginning of the URL.
CRAIGSLIST_SITE = 'denver'

#if counter_var == 0:
#    CRAIGSLIST_HOUSING_SECTION = 'mpa'
#if counter_var == 1:
#    CRAIGSLIST_HOUSING_SECTION = 'sna'
#else:
#    CRAIGSLIST_HOUSING_SECTION = 'mca'
CRAIGSLIST_HOUSING_SECTION = 'mpa'
## System settings

# How long we should sleep between scrapes of Craigslist.
# Too fast may get rate limited.
# Too slow may miss listings.
SLEEP_INTERVAL = 1 * 10 # 20 minutes

# Which slack channel to post the listings into.
SLACK_CHANNEL = "#coloradomotorcycles"

# The token that allows us to connect to slack.
# Should be put in private.py, or set as an environment variable.
SLACK_TOKEN = os.getenv('SLACK_TOKEN', "")

# Any private settings are imported here.
try:
    from private import *
except Exception:
    pass

# Any external private settings are imported from here.
try:
    from config.private import *
except Exception:
    pass
