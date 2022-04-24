import logging
import requests


class HypClient:
    def __init__(self, access_token, session=requests.Session()):
        self.access_token = access_token
        self.session = session
        self.logger = logging.getLogger("hyp_python_client")

    def try_assignment(self, participant_id, experiment_id, fallback):
        response = self.assignment(participant_id, experiment_id)

        if response["message"] == "success":
            self.logger.info(f'Successfully got assignment for participant {participant_id} in experiment {experiment_id}.')
            return response["payload"]["variant_name"]
        else:
            self.logger.warning(f'Failed to get assignment for participant {participant_id} in experiment {experiment_id}. Returning fallback {fallback}.')
            return fallback

    def assignment(self, participant_id, experiment_id):
        response = self.session.post(
            f'https://app.onhyp.com/api/v1/assign/{participant_id}/{experiment_id}',
            headers={'X_HYP_TOKEN': self.access_token},
        )

        result = response.json()
        result["status_code"] = response.status_code

        return result

    def try_conversion(self, participant_id, experiment_id):
        response = self.conversion(participant_id, experiment_id)

        if response["message"] == "success":
            self.logger.info(f'Successfully converted participant {participant_id} in experiment {experiment_id}.')
            return response["payload"]["converted"]
        else:
            self.logger.warning(f'Failed to convert participant {participant_id} in experiment {experiment_id}. Returning False.')
            return False

    def conversion(self, participant_id, experiment_id):
        response = self.session.patch(
            f'https://app.onhyp.com/api/v1/convert/{participant_id}/{experiment_id}',
            headers={'X_HYP_TOKEN': self.access_token},
        )

        result = response.json()
        result["status_code"] = response.status_code

        return result
