import unittest

from hyp.v1 import HypClient


# TODO: use VCR
# TODO: tell elias about test customer
class TestAssignment(unittest.TestCase):
    def setUp(self):
        self.client = HypClient("PRODUCTION/HYP/5ab8d3d8-6eca-4e11-9203-1b64faea1f33")

    def test_bad_access_token(self):
        client = HypClient(access_token="foo")
        response = client.assignment(participant_id="fuzzybear", experiment_id=8)

        self.assertEqual(response["status_code"], 401)
        self.assertEqual(response["message"], "Missing or invalid access token.")
        self.assertEqual(response["payload"], "")

    def test_no_experiment_found(self):
        response = self.client.assignment(participant_id="fuzzybear", experiment_id=13)

        self.assertEqual(response["status_code"], 404)
        self.assertEqual(response["message"], "No experiment with ID 13 was found.")
        self.assertEqual(response["payload"], "")

    def test_consistent_assignment(self):
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


if __name__ == '__main__':
    unittest.main()
