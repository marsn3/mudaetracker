# Discord IDs
# Replace values with your own.
CHANNEL_ID = 0000  # ID of claiming channel
SERVER_ID = 0000  # ID of Discord server
MUDAE = 432610292342587392  # User ID of Mudae

# Mudaetracker settings
MUDAE_PREFIX = "$"
PREFIX = "."
PAGES = 1  # How many Pages $top has, default Is 67
HOURS = 72  # How often the Top1000 should be checked
IM_LIST = "im_list.txt"  # File with characters to check additionally to the top1000

#  User login info.
#  This is not sent to any external server, but only used to login to browser Discord.
#  See Browser.browser_login() (specifically line 49-77) in browsers.py to see how it is exactly used.
LOGIN_INFO = ("example@example.com", "your_password")
TOKEN = "your_bot_token"  # Your Discord Bot Token

# Geckodriver path
WEB_DRIVER_PATH = "geckodriver"  # Full path to geckodriver if it isn't on PATH
