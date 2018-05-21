import bb
import os

from locust import task, HttpLocust


class AllEndpoints(bb.UserBehavior):

    @task(2)
    def get_eob(self):
        patient = self.get_random_userinfo()
        resource = '/v1/fhir/ExplanationOfBenefit/?patient=%s' % patient
        self.make_req(resource)

    @task(1)
    def get_coverage(self):
        patient = self.get_random_userinfo()
        resource = '/v1/fhir/Coverage/'
        self.make_req(resource)

    @task(1)
    def get_patient(self):
        patient = self.get_random_userinfo()
        resource ='/v1/fhir/Patient/%s' % patient
        self.make_req(resource)


class WebsiteUser(HttpLocust):
    task_set = AllEndpoints
    min_wait = int(os.environ.get("BB_LOAD_TEST_MIN_WAIT", 1000))
    max_wait = int(os.environ.get("BB_LOAD_TEST_MAX_WAIT", 5000))
