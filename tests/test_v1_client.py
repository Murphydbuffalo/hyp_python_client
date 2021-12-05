import unittest

from hyp.v1 import HypClient


class TestV1Client(unittest.TestCase):
    def test_assignment(self):
        client = HypClient(access_token="foo")
        self.assertEqual(client.access_token, "foo")


if __name__ == '__main__':
    unittest.main()
