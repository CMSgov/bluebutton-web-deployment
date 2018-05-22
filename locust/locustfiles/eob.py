import bb
import os

from locust import task, HttpLocust


class EOBEndpoint(bb.UserBehavior):

    @task()
    def get_eob(self):
        resource = '/v1/fhir/ExplanationOfBenefit/?patient=%s' % self.patient
        self.make_req(resource)


class User(HttpLocust):
    task_set = EOBEndpoint
    min_wait = int(os.environ.get("BB_LOAD_TEST_MIN_WAIT", 1000))
    max_wait = int(os.environ.get("BB_LOAD_TEST_MAX_WAIT", 5000))
    tokens = bb.Tokens(os.environ.get('BB_TKNS_FILE', 'tkns.txt'))
