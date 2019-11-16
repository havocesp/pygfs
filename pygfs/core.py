#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Daniel J. Umpierrez
import argparse
from pprint import pprint

from model import FlightCollector


def load_airports_info():
    cwd: Path = Path(__file__).resolve(True).parent
    data_file = cwd.joinpath('data', 'airports-code-min.csv')
    if data_file.is_file():
        content = data_file.read_text('utf-8')
        return [l.split(',') for l in content.splitlines() if l]


def get_iata_code(airport):
    airports = load_airports_info()
    results = list()
    if airports:
        for a in airports:
            if airport in str(' '.join(a[1:])).lower():
                results.append(a[0])

    return results[0] if results and len(results) == 1 else results


def parse_args():
    parser = argparse.ArgumentParser(
        description='Google flights scrapper.')
    subparsers = parser.add_subparsers()
    search = subparsers.add_parser('search')
    search.add_argument('-f', '--from-airport',
                        help='Departure airport IATA code.')
    search.add_argument('-t', '--to-airport',
                        help='Destiny airport IATA code.')
    search.add_argument('-s', '--date-start', help='Starting date.')
    search.add_argument('-e', '--date-end', help='Final date.')
    search.add_argument('-d', '--day-range',
                        help='A comma separated days range. Example: 7,10')
    search.add_argument('-C', '--country-code', default='es',
                        help='Two characters length country code. (Default: es)')
    search.add_argument('-c', '--currency', default='EUR',
                        help='Three characters length currency  code. (Default: EUR)')
    search.add_argument('-a', '--adults', type=int, default=1,
                        help='Amount of adult passengers.')
    search.add_argument('--children', help='Amount of children passengers.')

    search = subparsers.add_parser('airport')
    search.add_argument('airport')

    return parser.parse_args()


def main(args):
    """Sample of data collection routine."""
    if args.airport:
        print(get_iata_code(args.airport))
    else:
        fs = FlightCollector()
        try:
            flights = fs.search_all(args)
            if flights and len(flights):
                pprint(flights)
            else:
                print(' - Sorry, no flights found.')
        except Exception as err:
            raise err


if __name__ == '__main__':
    # TODO: remove me (just for testing purposes)
    import sys

    sys.argv.extend(['airport', 'madrid'])
    # sys.argv.extend([
    #     '-t', 'FUE',
    #     '-f', 'AGP',
    #     '-s', '2019-11-24',
    #     '-e', '2020-04-30',
    #     '-d', '7,18',
    #     '-C', 'es',
    #     '--adults', '2',
    #     '--children', '1'
    # ])

    # TODO parser.add_argument('--max-scales', help='Comma sep max. scales for date_start and arrival. Example: 0,1')
    # TODO parser.add_argument('--airline', help='IATA airline code.')
    # TODO parser.add_argument('--date_start-time', help='Earliest time filter for results. (Example: 10:00)')
    # TODO parser.add_argument('--arrival-time', help='Latest time filter for results. (Example: 20:00)')
    # TODO Add IATA airline code searcher by airline name.')
    main(parse_args())
