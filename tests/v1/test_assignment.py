import unittest
import betamax
import requests

from src.hyp_client.v1 import HypClient

CASSETTE_LIBRARY_DIR = 'tests/cassettes/'


class TestAssignment(unittest.TestCase):
    def setUp(self):
        session = requests.Session()
        self.client = HypClient("PRODUCTION/HYP/5ab8d3d8-6eca-4e11-9203-1b64faea1f33", session)
        self.recorder = betamax.Betamax(
            session,
            cassette_library_dir=CASSETTE_LIBRARY_DIR,
            default_cassette_options={
                'match_requests_on': ['method', 'uri', 'headers'],
                'record_mode': 'once'
            }
        )

    def test_bad_access_token(self):
        self.client.access_token = "foo"

        with self.recorder.use_cassette("assignment-bad-access-token"):
            response = self.client.assignment(participant_id="fuzzybear", experiment_id=8)

            self.assertEqual(response["status_code"], 401)
            self.assertEqual(response["message"], "Missing or invalid access token.")
            self.assertEqual(response["payload"], "")

    def test_no_experiment_found(self):
        with self.recorder.use_cassette("assignment-no-experiment-found"):
            response = self.client.assignment(participant_id="fuzzybear", experiment_id=13)

            self.assertEqual(response["status_code"], 404)
            self.assertEqual(response["message"], "No experiment with ID 13 was found.")
            self.assertEqual(response["payload"], "")

    def test_consistent_assignment(self):
        with self.recorder.use_cassette("assignment-consistent-assignment"):
            response = self.client.assignment(participant_id="fuzzybear", experiment_id=8)

            self.assertEqual(response["status_code"], 200)
            self.assertEqual(response["message"], "success")
            self.assertEqual(response["payload"]["variant_name"], "v2")

            response = self.client.assignment(participant_id="sillybear", experiment_id=8)

            self.assertEqual(response["status_code"], 200)
            self.assertEqual(response["message"], "success")
            self.assertEqual(response["payload"]["variant_name"], "v1")

            # Repeat calls, assignment doesn't change
            response = self.client.assignment(participant_id="fuzzybear", experiment_id=8)

            self.assertEqual(response["status_code"], 200)
            self.assertEqual(response["message"], "success")
            self.assertEqual(response["payload"]["variant_name"], "v2")

            response = self.client.assignment(participant_id="sillybear", experiment_id=8)

            self.assertEqual(response["status_code"], 200)
            self.assertEqual(response["message"], "success")
            self.assertEqual(response["payload"]["variant_name"], "v1")

    def test_try_assignment(self):
        with self.recorder.use_cassette("assignment-try-assignment"):
            with self.assertLogs("hyp_python_client", "INFO") as log_capture:
                variant = self.client.try_assignment(participant_id="fuzzybear", experiment_id=8, fallback="this-can-be-anything")
                self.assertEqual(variant, "v2")
                self.assertEqual(log_capture.output, ["INFO:hyp_python_client:assignment successful for participant fuzzybear in experiment 8."])

                variant = self.client.try_assignment(participant_id="sillybear", experiment_id=888, fallback="this-can-be-anything")
                self.assertEqual(variant, "this-can-be-anything")
                self.assertEqual(log_capture.output[-1], "WARNING:hyp_python_client:assignment failed for participant sillybear in experiment 888. Error: No experiment with ID 888 was found. Returning fallback this-can-be-anything.")

    def test_try_assignment_missing_data(self):
        with self.assertLogs("hyp_python_client", "INFO") as log_capture:
            variant = self.client.try_assignment(participant_id=None, experiment_id=8, fallback="this-can-be-anything")
            self.assertEqual(variant, "this-can-be-anything")
            self.assertEqual(log_capture.output[-1], "WARNING:hyp_python_client:assignment failed due to missing participant ID. Returning fallback this-can-be-anything.")

        with self.assertLogs("hyp_python_client", "INFO") as log_capture:
            variant = self.client.try_assignment(participant_id="fuzzybear", experiment_id=None, fallback="this-can-be-anything")
            self.assertEqual(variant, "this-can-be-anything")
            self.assertEqual(log_capture.output[-1], "WARNING:hyp_python_client:assignment failed due to missing experiment ID. Returning fallback this-can-be-anything.")

        with self.assertLogs("hyp_python_client", "INFO") as log_capture:
            variant = self.client.try_assignment(participant_id=None, experiment_id=None, fallback="this-can-be-anything")
            self.assertEqual(variant, "this-can-be-anything")
            self.assertEqual(log_capture.output[-1], "WARNING:hyp_python_client:assignment failed due to missing participant ID and experiment ID. Returning fallback this-can-be-anything.")


if __name__ == '__main__':
    unittest.main()
