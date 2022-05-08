import unittest
import betamax
import requests

from src.hyp_client.v1 import HypClient

CASSETTE_LIBRARY_DIR = 'tests/cassettes/'


class TestConversion(unittest.TestCase):
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

        with self.recorder.use_cassette("conversion-bad-access-token"):
            response = self.client.conversion(participant_id="fuzzybear", experiment_id=8)

            self.assertEqual(response["status_code"], 401)
            self.assertEqual(response["message"], "Missing or invalid access token.")
            self.assertEqual(response["payload"], "")

    def test_no_variant_assignment_found(self):
        with self.recorder.use_cassette("conversion-no-variant-assignment-found"):
            response = self.client.conversion(participant_id="grumpybear", experiment_id=8)

            self.assertEqual(response["status_code"], 404)
            self.assertEqual(response["message"], "No variant assignment for participant grumpybear in experiment 8 was found. Participants must be assigned to a variant before conversion can be recorded.") # noqa E501
            self.assertEqual(response["payload"], "")

    def test_conversion(self):
        with self.recorder.use_cassette("conversion-successful-conversion"):
            response = self.client.conversion(participant_id="fuzzybear", experiment_id=8)

            self.assertEqual(response["status_code"], 200)
            self.assertEqual(response["message"], "success")
            self.assertEqual(response["payload"]["converted"], True)

            response = self.client.conversion(participant_id="sillybear", experiment_id=8)

            self.assertEqual(response["status_code"], 200)
            self.assertEqual(response["message"], "success")
            self.assertEqual(response["payload"]["converted"], True)

    def test_try_conversion(self):
        with self.recorder.use_cassette("conversion-try-conversion"):
            with self.assertLogs("hyp_python_client", "INFO") as log_capture:
                conversion = self.client.try_conversion(participant_id="fuzzybear", experiment_id=8)
                self.assertEqual(conversion, True)
                self.assertEqual(log_capture.output, ["INFO:hyp_python_client:Successfully converted participant fuzzybear in experiment 8."])

                conversion = self.client.try_conversion(participant_id="sillybear", experiment_id=888)
                self.assertEqual(conversion, False)
                self.assertEqual(log_capture.output[-1], "WARNING:hyp_python_client:Failed to convert participant sillybear in experiment 888. Returning False.")

    def test_try_conversion_missing_data(self):
        with self.assertLogs("hyp_python_client", "INFO") as log_capture:
            conversion = self.client.try_conversion(participant_id=None, experiment_id=8)
            self.assertEqual(conversion, False)
            self.assertEqual(log_capture.output[-1], "WARNING:hyp_python_client:Failed to convert due to missing participant ID or experiment ID. Returning False.")

        with self.assertLogs("hyp_python_client", "INFO") as log_capture:
            conversion = self.client.try_conversion(participant_id="fuzzybear", experiment_id=None)
            self.assertEqual(conversion, False)
            self.assertEqual(log_capture.output[-1], "WARNING:hyp_python_client:Failed to convert due to missing participant ID or experiment ID. Returning False.")

if __name__ == '__main__':
    unittest.main()
