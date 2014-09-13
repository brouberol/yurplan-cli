# -*- coding: utf-8 -*-

import json
import os
import requests

from collections import namedtuple

Attendant = namedtuple('Attendant', ['first_name', 'last_name', 'email'])


class YurplanClient(object):

    YURPLAN_API = "http://yurplan.com/api.php/"
    LOGIN_API = YURPLAN_API + 'auth'
    EVENTS_API = YURPLAN_API + 'events'
    EVENT_ID = os.environ['YURPLAN_EVENT_ID']
    EVENT_URL = EVENTS_API + '/' + str(EVENT_ID)
    TICKETS_API = EVENT_URL + '/tickets'
    API_KEY = os.environ['YURPLAN_API_KEY']
    EMAIL = os.environ['YURPLAN_EMAIL']
    PASSWORD = os.environ['YURPLAN_PASSWORD']

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        self.session.params.update({'key': self.API_KEY})
        self.login(self.EMAIL, self.PASSWORD)

    def login(self, email, password):
        """Log in the Yurplan API and add the token to the HTTP session."""
        data = json.dumps({'email': email, 'password': password})
        r = self.session.post(self.LOGIN_API, data=data)
        if not r.ok:
            raise requests.HTTPError(r.json())
        self.token = r.json()['data']['token']
        self.session.params.update({'token': self.token})

    def tickets(self):
        """Query the Yurplan API for the tickets information associated
        with the event.

        """
        r = self.session.get(self.TICKETS_API)
        return r.json()

    def attendants(self):
        """Return the list of people attending the event as list of
        Attendant instances, a namedtuple containing the attendant
        first name, last name and email.

        """
        return [
            Attendant(t['firstname'], t['lastname'], t['email_address'])
            for t in self.tickets()['data']['tickets']
            if t['type']['name'] == u"Réservation"
        ]
