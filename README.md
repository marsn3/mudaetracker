# Top1000 Tracker

Track the Top 100 Characters of Mudae over Time.

## Requirements

- Firefox and [geckodriver](https://github.com/mozilla/geckodriver/releases)
- Python 3.8+
- Python modules: see `requirements.txt`

## Usage

Clone this repository and fill in the data in `config-example.py` and rename the file to `config.py`. Visit [here](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) for information about getting Discord ids. See [Getting a Bot token](https://github.com/jagrosh/MusicBot/wiki/Getting-a-Bot-Token) for info about getting a Bot Token.

Your bot must have the following permissions:

- View Channels
- Read Message History

Install Python 3.8+ and required modules. Optionally make a new virtual environment for it.

`pip install -r requirements.txt`

Install Firefox and geckodriver. This will be used to send the $top messages automatically. Put your geckodriver path in `config.py`. To start the bot, run `bot.py`.

By Default, the Bot will check the Top1000 every three Days, this Behavior can be changed by editing changing the Value of `HOURS` in `config.py`.

The bot creates a CSV File with the following format:
| Name | Rank | Date | Series |
| ---- | ---- | ---- | ------ |

You can also enter custom characters to be checked in `im_list.txt`, where every line equals one character.
It will save the information in a CSV FIle with the following format:
| name | claimrank | likerank | kakera | date | series |
| ---- | --------- | -------- | ------ | ---- | ------ |

If you want to download the csv files directly in discord, use `[p]csv`, where `[p]` is the prefix set in `config.py` (by default, it is`.`)

## Planned Features

- Exporting to .xlsx file with pivot tables
- (Automatic) generation of graphs from collected data
- Automatic uploading of the data to a GitHub Repo for Archiving

## Credits

[Selenium Code](browsers.py) and [README](README.md) adapted from [AutoWaifuClaimer](https://github.com/RandomBananazz/AutoWaifuClaimerV3/)

Regex to get data about custom characters modified from [EZMudae](https://github.com/Znunu/EzMudae)

## Disclaimer

I am not responsible for banned user accounts. Use at your own risk.

This project also collects your Discord email and password in **plain-text**. Although it does not use this information for any purpose other than to login to Discord on the web, please keep this information safe so that it is not accidentally accessed by other users of the computer. Also, feel free to manually audit the source code to see where exactly the information is being used (the only instance is in `browsers.Browser.browser_login()`).
