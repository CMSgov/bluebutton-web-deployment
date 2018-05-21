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

from locust import TaskSet, web, events
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
    tokens = []
    patients = {}

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        with open(os.environ.get('BB_TKNS_FILE', 'tkns.txt')) as f:
            self.tokens = [json.loads(line)['access_token'] for line in f]

        events.quitting += self.quitting

    def quitting(self):
        for token in self.tokens:
            self.client.post("%s%s" % (base_url, '/v1/o/revoke_token/'), data={
                    'token': token,
                    'client_id': client_id,
                    'client_secret': client_secret
                })

    def check_count(self):
        if self.count >= self.max_count:
            self.client.cookies.clear()

    def record_req(self):
        self.count += 1

    def get_token(self):
        secure_random = random.SystemRandom()
        return secure_random.choice(self.tokens)

    def set_auth_header(self, token):
        self.client.headers['Authorization'] = 'Bearer ' + token

    def get_random_userinfo(self):
        access_token = self.get_token()
        self.set_auth_header(access_token)
        try:
            return self.patients[access_token]
        except KeyError:
            response = self.client.get("%s%s" % (base_url, '/v1/connect/userinfo'))
            self.patients[access_token] = json.loads(response.content).get('patient')
            return self.patients[access_token]

    def make_req(self, resource):
        self.check_count()
        self.client.get("%s%s" % (base_url, resource))
        self.record_req()
