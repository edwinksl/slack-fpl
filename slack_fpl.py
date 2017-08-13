#!/usr/bin/env python

import dotenv
import json
import os
import requests
from flask import Flask, request

app = Flask(__name__)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)
verification_token = os.environ['VERIFICATION_TOKEN']
league_id = os.environ['LEAGUE_ID']

RANK_WIDTH = 5
TEAM_WIDTH = 20
GW_WIDTH = 5
TOT_WIDTH = 5


@app.route('/apps/slack-fpl', methods=['POST'])
def fpl():
    if request.form['token'] == verification_token:
        url = 'https://fantasy.premierleague.com/drf/leagues-classic-standings/' + league_id
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            response_url = request.form['response_url']
            payload_ack = {'response_type': 'ephemeral', 'text': 'Got it!'}
            r_ack = requests.post(response_url, json=payload_ack)
            data = json.loads(r.text)
            results = data['standings']['results']
            header = f"{'Rank':<{RANK_WIDTH}}{'Team':<{TEAM_WIDTH}}{'GW':<{GW_WIDTH}}{'TOT':<{TOT_WIDTH}}\n"
            text = '```' + header
            for result in results:
                rank = result['rank']
                team = result['entry_name']
                gw = result['event_total']
                tot = result['total']
                row = f'{rank:<{RANK_WIDTH}}{team:<{TEAM_WIDTH}}{gw:<{GW_WIDTH}}{tot:<{TOT_WIDTH}}\n'
                text += row
            text += '```'
            payload_delayed = {'response_type': 'in_channel', 'text': text}
            r_delayed = requests.post(response_url, json=payload_delayed)
            return '', 200


if __name__ == '__main__':
    app.run()
