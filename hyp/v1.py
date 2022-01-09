import requests


class HypClient:
    def __init__(self, access_token, session=requests.Session()):
        self.access_token = access_token
        self.session = session

    def assignment(self, participant_id, experiment_id):
        response = self.session.post(
            f'https://app.onhyp.com/api/v1/assign/{participant_id}/{experiment_id}',
            headers={'X_HYP_TOKEN': self.access_token},
        )

        result = response.json()
        result["status_code"] = response.status_code

        return result

    def conversion(self, participant_id, experiment_id):
        response = self.session.patch(
            f'https://app.onhyp.com/api/v1/convert/{participant_id}/{experiment_id}',
            headers={'X_HYP_TOKEN': self.access_token},
        )

        result = response.json()
        result["status_code"] = response.status_code

        return result
