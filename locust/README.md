### Load testing with locust

There are two [locust](https://locust.io/) test plans included:

- The `locustfiles/eob.py` test plan exercises the Explanation of Benefits (EOB) endpoint only
- The `locustfiles/all.py` test plan exercises the EOB, Coverage and Patient endpoints

#### Set up and run the load tests

Define the required environment variables:

```sh
export BB_CLIENT_ID=<client_id>
export BB_CLIENT_SECRET=<client_secret>
export BB_SUB_DOMAIN=sandbox.bluebutton.cms.gov
export BB_LOAD_TEST_TYPE=all
```

Optional environment variables:

```sh
# BB_NUM_BENES (number of synthetic benes, default: 4)
# BB_LOAD_TEST_DURATION (number of seconds, default: 20)
# BB_LOAD_TEST_HATCH_RATE (hatch rate for clients added per second, default: 1)
# BB_LOAD_TEST_MIN_WAIT (how many ms to wait between requests, lower bound, default: 1000)
# BB_LOAD_TEST_MAX_WAIT (how many ms to wait between requests, upper bound, default: 5000)
# BB_TKNS_WORKERS (how many tkns workers to use when fetching access tokens, default: 2)
```

Once your environment is prepared:

```sh
./run.sh
```
