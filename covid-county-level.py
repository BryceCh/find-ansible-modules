#!/usr/bin/env python3

import os
import sys

from datetime import datetime, timedelta
from sodapy import Socrata  # https://github.com/xmunoz/sodapy
from termcolor import colored


def current_week_covid_level(state=None, county=None):
    '''return data from CDC COVID 19 Community Levels by County data set,
       sorted by high/medium/low and then county name

       endpoint information and schema at:
       https://data.cdc.gov/Public-Health-Surveillance/United-States-COVID-19-Community-Levels-by-County/3nnm-4jni
    '''

    # with an undefined app token, API calls will be rate-limited
    # https://dev.socrata.com/docs/app-tokens.html
    socrata_token = os.environ.get('COVID_COUNTY_LEVEL_APP_TOKEN') or None
    socrata_domain = 'data.cdc.gov'

    # CDC data is updated weekly, so use today and a week ago
    # for SoQL where clause
    today = datetime.date(datetime.now())
    last_week = today - timedelta(days=7)

    with Socrata(socrata_domain, socrata_token, timeout=10) as client:
        where = f'date_updated between "{str(last_week)}" and "{str(today)}"'
        data = client.get('3nnm-4jni', state=state, county=county, where=where)

    weights = {'high': 0, 'medium': 1, 'low': 2}
    return sorted(data, key=lambda d: (weights[d['covid_19_community_level'].lower()], d['county']))


def main():
    state = 'Maryland'
    colors = {'high': 'red', 'medium': 'yellow', 'low': 'green'}

    for item in current_week_covid_level(state=state):
        level = item["covid_19_community_level"]
        color = colors[level.lower()]

        print(f'{item["county"] + ":" : <25}', colored(level, color))


if __name__ == '__main__':
    sys.exit(main())
