#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Core module.

Author: Daniel J. Umpierrez
"""
import argparse
import sys
import time
from pprint import pprint
from typing import List

from lxml import html
from splinter.browser import FirefoxWebDriver

FAILS = 0  # tickets failed to parse


def _flight_request(args):
    """URL Builder."""
    if int(args.adults) > 1 or args.childs:
        passengers = f';px:{args.adults}'
        if args.childs:
            passengers += f',{args.childs}'
    else:
        passengers = str()
    params = {'passengers': passengers, **vars(args)}
    url = 'https://www.google.com/flights/#flt={from_airport}.{to_airport}.{date_start}*{to_airport}.{from_airport}.{date_end};c:{currency};e:1;s:0*0{passengers};sd:1;t:f'
    url = url.format(**params)
    print('https://www.google.com/flights/#flt=AGP.FUE.2019-11-10*FUE.AGP.2019-11-17;c:EUR;e:1;s:0*0;px:2,1;sd:1;t:f')
    print(url)

    return url


def _parse_card(card, date_start, date_end, adults, childs):
    """Parse flight card, getting company, flight timing and date, etc.

    :param card:
    :return: flight info dictionary.
    """
    global FAILS
    data = dict()
    try:
        data = {
            'date_start': date_start,
            'date_end': date_end,
            'adults': adults,
            'childs': childs,
            # 'link':      card.xpath('./@href')[0],
            # 'price':     card.xpath('/html/body/div[3]/div[2]/div/div[2]/div[3]/div/jsl/div/div[2]/main[4]/div[7]/div[1]/div[5]/div[4]/div[1]/ol/li/div/div[1]/div[2]/div[1]/div[1]/div[5]/div[1]')[0].text,
            'price': card.xpath('./div/div[1]/div[2]/div[1]/div[1]/div[5]/div[1]')[0].text.strip('\t ').replace(
                '\xa0', ' '),
            # 'departure': card.xpath('/html/body/div[3]/div[2]/div/div[2]/div[3]/div/jsl/div/div[2]/main[4]/div[7]/div[1]/div[5]/div[4]/div[1]/ol/li/div/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div/span[1]/span/span')[0].text,
            'departure': card.xpath('./div/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div/span[1]/span/span')[0].text,
            'arrival': card.xpath('./div/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div/span[2]/span/span')[0].text,
            'duration': card.xpath('./div/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]')[0].text.replace('\xa0', ' '),
            'stops': card.xpath('./div/div[1]/div[2]/div[1]/div[1]/div[4]/div[1]/div/div/span')[0].text,
            'airline': card.xpath('./div/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/span[1]/span/span')[
                0].text_content()
        }

    except Exception as inst:
        print(str(inst))
        print('Failed to parse card...')
        FAILS += 1

    return FlightOffer(**data)


# def _store_flights(flights, path=None):
#     """Stores flights in csv.
#
#     :param flights: flights data.
#     :param path: file path where data will be stored.
#     """
#     headers = ['link', 'price', 'departure', 'arrival', 'duration', 'airline', 'stops']
#     with open(path or 'test_search.csv', 'wt') as csvfile:
#         writer = DictWriter(csvfile, fieldnames=headers)
#         writer.writeheader()
#
#         for f in flights:
#             writer.writerow({k: v.encode('utf8') for k, v in f.items()})


class FlightCollector():
    """Flight data collector class."""

    def __init__(self):
        self.browser = FirefoxWebDriver(headless=True)

    def search_all(self, args, time_sleep=3) -> List[FlightOffer]:
        """Search for all flights for all searches.

        NOTE: might be useful to add search name

        :param list searches: list of dictionaries, defininf search
        :param int time_sleep(int): seconds to sleep TODO: need to define/replace/improve
        :return: list of flight dicts
        """
        url = _flight_request(args)

        self.browser.visit(url)
        time.sleep(time_sleep)

        dom = html.fromstring(self.browser.html)
        bs = Bs(self.browser.html)
        # self.browser.quit()
        flights = dom.xpath(
            './div[3]/div[2]/div/div[2]/div[3]/div/jsl/div/div[2]/main[4]/div[7]/div[1]/div[5]/div[2]/ol/li')

        if len(flights) == 0:
            print(' - Sorry, no flights found.')
        else:
            print(f' - {len(flights)} flights found.')
            return [_parse_card(f, args.date_start, args.date_end, args.adults, args.childs) for f in flights]


def main(args):
    """Sample of data collection routine."""

    # searches_file = Path('searches.json')  # get all searches in the json
    # searches = json.loads(searches_file.read_text())['searches']

    fs = FlightCollector()
    try:
        flights = fs.search_all(args)
        pprint(flights)
        # print(f'Failed to parse {FAILS} flights')
    except Exception as err:
        print(str(err))


if __name__ == '__main__':
    sys.argv.extend(
        ['-f', 'AGP', '-t', 'FUE', '-s', '2019-11-10', '-e', '2019-11-17', '-C', 'es', '--adults', '2', '--childs',
         '1'])
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from-airport', required=True)
    parser.add_argument('-t', '--to-airport', required=True)
    parser.add_argument('-s', '--date-start', required=True)
    parser.add_argument('-e', '--date-end', required=True)
    parser.add_argument('-C', '--country-code', default='es')
    parser.add_argument('-c', '--currency', default='EUR')
    parser.add_argument('--adults', default='1')
    parser.add_argument('--childs')
    # parser.add_argument('--babies')
    # parser.add_argument('--babies-sit')
    args = parser.parse_args()
    main(args)
