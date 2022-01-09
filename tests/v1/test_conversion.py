import unittest
import betamax
import requests

from hyp.v1 import HypClient

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


if __name__ == '__main__':
    unittest.main()
