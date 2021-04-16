import bb
import os

from locust import task, HttpLocust


class AllEndpoints(bb.UserBehavior):

    @task(2)
    def get_eob(self):
        resource = '/v1/fhir/ExplanationOfBenefit/?patient=%s' % self.patient
        self.make_req(resource)

    @task(1)
    def get_coverage(self):
        resource = '/v1/fhir/Coverage/?patient=%s' % self.patient
        self.make_req(resource)

    @task(1)
    def get_patient(self):
        resource ='/v1/fhir/Patient/%s' % self.patient
        self.make_req(resource)


class User(HttpLocust):
    task_set = AllEndpoints
    min_wait = int(os.environ.get("BB_LOAD_TEST_MIN_WAIT", 1000))
    max_wait = int(os.environ.get("BB_LOAD_TEST_MAX_WAIT", 5000))
    tokens = bb.Tokens(os.environ.get('BB_TKNS_FILE', 'tkns.txt'))
