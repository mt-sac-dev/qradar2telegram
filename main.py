from pprint import pprint
from os import path
import pickle
import requests
import datetime
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()

# Script for posting events in Telegram

SIEM_KEY = os.getenv("SIEM_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")

SIEM_URL = os.getenv("SIEM_URL")

urllib3.disable_warnings()


def post_telegram_issue(message):
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + BOT_CHAT_ID + '&parse_mode=Markdown&text=' + message
    # response = requests.get(send_text, proxies=PROXIES)
    response = requests.get(send_text)
    return response.json()


def get_siem_offenses(base_url, sec_code,
                      fields="id,description,status,start_time,severity,offense_source,source_network,"
                             "destination_networks"):
    headers = {
        'sec': sec_code,
        'version': '8.1',
    }
    response = requests.get(base_url + 'api/siem/offenses', headers=headers,
                            params={"fields": fields, "filter": "status=OPEN"}, verify=False)
    return response.json()


def get_severity_appearance(severity):
    if severity == 1 or severity == 2:
        return "🟦🟦⬜️⬜️⬜️⬜️ ️"
    if severity == 3 or severity == 4:
        return "🟩🟩🟩⬜️⬜️⬜️"
    if severity == 5 or severity == 6:
        return "🟨🟨🟨🟨⬜️⬜️"
    if severity == 7 or severity == 8:
        return "🟧🟧🟧🟧🟧⬜️️"
    return "🟥🟥🟥🟥🟥🟥"



def create_offense_for_telegram(raw_offense):
    time = raw_offense['start_time'] / 1000.0
    time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
    offense_url = SIEM_URL +'console/qradar/jsp/QRadar.jsp?appName=Sem%26pageId=OffenseSummary%26summaryId={id}'.format(
        id=raw_offense['id'])
    try:
        source = raw_offense['offense_source']

    except:
        source = ""

    offense = '*Offense id*: {id} - {title}' \
              '\r\n*Time:* {time}' \
              '\r\n*Source:* {source}' \
              '\r\n*Source Network:* {source_network}' \
              '\r\n*Destination Networks:* {destination_networks}' \
              '\r\n*Severity:* {severity}' \
              '\r\n*URL:* [click here]({offense_url})'.format(
        title=raw_offense['description'].replace('\n', ''),
        time=time,
        source=source,
        source_network=raw_offense['source_network'],
        destination_networks=raw_offense['destination_networks'],
        severity=get_severity_appearance(raw_offense['severity']),
        offense_url=offense_url, id=raw_offense['id'])

    return offense


def load_cache(filename='cache1.pkl'):
    if not path.exists(filename):
        return set()

    with open(filename, 'rb') as f:
        return pickle.load(f)


def save_cache(cache, filename='cache1.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(cache, f)


if __name__ == '__main__':
    sent_offenses_cache = load_cache()
    print('in cache:')
    pprint(sent_offenses_cache)
    min_offense_id = 2205

    offenses = get_siem_offenses(SIEM_URL, SIEM_KEY)
    offenses_not_in_cache = (offense for offense in offenses if offense['id'] not in sent_offenses_cache)

    for offense in offenses:
        offense_id = int(offense['id'])
        min_offense_id = offense_id if (min_offense_id is None) else min(offense_id, min_offense_id)

    for offense in offenses_not_in_cache:
        offense_id = int(offense['id'])
        telegram_issue = create_offense_for_telegram(offense)

        print('posting offense #: %d ...' % offense_id)
        post_telegram_issue(telegram_issue)

        sent_offenses_cache.add(offense_id)

    if min_offense_id is not None:
        print('removing items from cache, older than # %d ...' % min_offense_id)
        sent_offenses_cache = set((x for x in sent_offenses_cache if x >= min_offense_id))

    # save cache
    save_cache(sent_offenses_cache)
