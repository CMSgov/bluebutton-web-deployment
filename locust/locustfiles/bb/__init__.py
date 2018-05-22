"""
BlueButton (2.0!) Locust Test

A basic locust test for blue button.

Environment variables:

    - BB_LOAD_TEST_BASE_URL: The protocol + host to test (e.g. https://sandbox.bluebutton.cms.gov)
    - BB_LOAD_TEST_MIN_WAIT: The minimum number of ms for a client to wait before starting a new request
    - BB_LOAD_TEST_MAX_WAIT: The maximum number of ms for a client to wait before starting a new request
    - BB_TKNS_FILE :         The location of the file containing access tokens to use during the test
    - BB_CLIENT_ID:          The client id of the OAuth application
    - BB_CLIENT_SECRET:      The client secret of the OAuth application
"""

from locust import TaskSet, HttpLocust, web, events
from requests_oauthlib import OAuth2Session
import os
import json
import random

# The base URL for the API server where testing will take place.
base_url = os.environ.get("BB_LOAD_TEST_BASE_URL", "https://sandbox.bluebutton.cms.gov")
client_id = os.environ["BB_CLIENT_ID"]
client_secret = os.environ["BB_CLIENT_SECRET"]


class UserBehavior(TaskSet):

    count = 0
    max_count = 50

    token = None
    patient = None

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        # Set the auth header
        self.token = self.parent.tokens.next()
        self.client.headers['Authorization'] = 'Bearer ' + self.token

        # Get patient info
        response = self.client.get("%s%s" % (base_url, '/v1/connect/userinfo'))
        self.patient = json.loads(response.content).get('patient')

        # Revoke the access token when we're done
        events.quitting += self.quitting

    def quitting(self):
        self.client.post("%s%s" % (base_url, '/v1/o/revoke_token/'), data={
                'token': self.token,
                'client_id': client_id,
                'client_secret': client_secret
            })

    def check_count(self):
        if self.count >= self.max_count:
            self.client.cookies.clear()

    def record_req(self):
        self.count += 1

    def make_req(self, resource):
        self.check_count()
        self.client.get("%s%s" % (base_url, resource))
        self.record_req()


class Tokens(object):

    _tokens = []

    def __init__(self, file):
        with open(file) as f:
            self._tokens = [json.loads(line)['access_token'] for line in f]

    def next(self):
        return self._tokens.pop()
