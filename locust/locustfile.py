#!/usr/bin/python
"""
BlueButton (2.0!) Locust Test

A basic locust test for blue button.  This right now simply has stubs for the
oauth flow and tries to retrieve the access token from the
"LOCUST_BB_LOAD_TEST_ACCESS_TOKEN" environment variable.

Other environment variables:

    - LOCUST_BB_LOAD_TEST_BASE_URL:    The protocol + host to test (e.g. https://dev.bluebutton.cms.gov)
    - LOCUST_BB_LOAD_TEST_MIN_WAIT:    The minimum number of ms for a client to wait before starting a new request
    - LOCUST_BB_LOAD_TEST_MAX_WAIT:    The maximum number of ms for a client to wait before starting a new request

Things to do:

- Somehow integrate oauth setup
- Actually load test oauth setup (comments below)
"""

from locust import HttpLocust, TaskSet, task, web
from requests_oauthlib import OAuth2Session
import os
import json

# The base URL for the API server where testing will take place.
base_url = os.environ.get("LOCUST_BB_LOAD_TEST_BASE_URL", "https://dev.bluebutton.cms.gov")
access_token = os.environ["LOCUST_BB_LOAD_TEST_ACCESS_TOKEN"]


class UserBehavior(TaskSet):

    count = 0
    max_count = 50

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

        self.client.headers['Authorization'] = 'Bearer ' + access_token
        response = self.client.get("%s%s" % (base_url, '/v1/connect/userinfo'))
        data = json.loads(response.content)

        self.patient = data.get('patient')

    def check_count(self):
        if self.count >= self.max_count:
            self.client.cookies.clear()

    def record_req(self):
        self.count += 1

    def make_req(self, resource):
        self.check_count()
        self.client.get("%s%s" % (base_url, resource))
        self.record_req()

    @task(11)
    def get_userinfo(self):
        resource = '/v1/connect/userinfo'
        self.make_req(resource)

    @task(26)
    def get_eob(self):
        resource = '/v1/fhir/ExplanationOfBenefit/?patient=%s&_format=json' % self.patient
        self.make_req(resource)

    @task(13)
    def get_coverage(self):
        resource = '/v1/fhir/Coverage/?_format=json'
        self.make_req(resource)

    @task(22)
    def get_patient(self):
        resource ='/v1/fhir/Patient/%s?_format=json' % self.patient
        self.make_req(resource)

    @task(6)
    def get_metadata(self):
        resource = '/v1/fhir/metadata?format=json'
        self.make_req(resource)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = int(os.environ.get("LOCUST_BB_LOAD_TEST_MIN_WAIT", 0))
    max_wait = int(os.environ.get("LOCUST_BB_LOAD_TEST_MAX_WAIT", 500))
