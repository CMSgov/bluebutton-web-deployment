#!/usr/bin/python
"""
BlueButton (2.0!) Locust Test

A basic locust test for blue button.

Environment variables:

    - BB_LOAD_TEST_BASE_URL: The protocol + host to test (e.g. https://sandbox.bluebutton.cms.gov)
    - BB_LOAD_TEST_MIN_WAIT: The minimum number of ms for a client to wait before starting a new request
    - BB_LOAD_TEST_MAX_WAIT: The maximum number of ms for a client to wait before starting a new request
    - BB_TKNS_FILE :         The location of the file containing access tokens to use during the test
"""

from locust import HttpLocust, TaskSet, task, web
from requests_oauthlib import OAuth2Session
import os
import json
import random

# The base URL for the API server where testing will take place.
base_url = os.environ.get("BB_LOAD_TEST_BASE_URL", "https://sandbox.bluebutton.cms.gov")


class UserBehavior(TaskSet):

    count = 0
    max_count = 50
    tokens = []

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        with open(os.environ.get('BB_TKNS_FILE', 'tkns.txt')) as f:
            self.tokens = [json.loads(line)['access_token'] for line in f]

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
        response = self.client.get("%s%s" % (base_url, '/v1/connect/userinfo'))
        data = json.loads(response.content)
        return data.get('patient')

    def make_req(self, resource):
        self.check_count()
        self.client.get("%s%s" % (base_url, resource))
        self.record_req()

    @task()
    def get_eob(self):
        patient = self.get_random_userinfo()
        resource = '/v1/fhir/ExplanationOfBenefit/?patient=%s' % patient
        self.make_req(resource)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = int(os.environ.get("BB_LOAD_TEST_MIN_WAIT", 1000))
    max_wait = int(os.environ.get("BB_LOAD_TEST_MAX_WAIT", 5000))
