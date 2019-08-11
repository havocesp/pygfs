# -*- coding:utf-8 -*-
"""model module"""
from datetime import datetime as dt

from dateparser import parse


class FlightOffer:
    """Flight offers container."""

    def __init__(self, **kwargs):
        self._data = dict(kwargs)
        self.timestamp = dt.now().timestamp()
        self.price = kwargs.get('price')
        self.duration = kwargs.get('duration')
        self.adults = kwargs.get('adults')
        self.childs = kwargs.get('childs') or 0
        self.stops = kwargs.get('stops')
        self.airline = kwargs.get('airline')
        self.departure = parse(f"{kwargs.get('date_start')} {kwargs.get('departure')}")
        self.arrival = parse(f"{kwargs.get('date_end')} {kwargs.get('arrival')}")

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return f'FlightOffer{str(self)}'
