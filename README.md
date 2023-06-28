## This is a script for posting events in Telegram.
For use you must have a file *.env*, that will contain ```SIEM_KEY```, ```BOT_TOKEN``` , ```BOT_CHAT_ID``` and ```SIEM_URL```

Example of *.env*:
```
SIEM_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
BOT_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
BOT_CHAT_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

SIEM_URL=https://XXXXXXXXXXXXXXXXXXXXXXXXXX/
```
<br/>
 
These values will be substituted in the next part of the code:
```
SIEM_KEY = os.getenv("SIEM_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")

SIEM_URL = os.getenv("SIEM_URL")
```
