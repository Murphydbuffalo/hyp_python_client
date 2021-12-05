import requests


class HypClient:
    def __init__(self, access_token):
        self.access_token = access_token

    def assignment(self, participant_id, experiment_id):
        response = requests.post(
            f'https://app.onhyp.com/api/v1/assign/{participant_id}/{experiment_id}',
            headers={'X_HYP_TOKEN': self.access_token},
        )

        result = response.json()
        result["status_code"] = response.status_code

        return result

    def conversion(self, participant_id, experiment_id):
        response = requests.patch(
            f'https://app.onhyp.com/api/v1/convert/{participant_id}/{experiment_id}',
            headers={'X_HYP_TOKEN': self.access_token},
        )

        result = response.json()
        result["status_code"] = response.status_code

        return result
