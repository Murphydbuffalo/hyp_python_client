# hyp_python_client
Python API client for [Hyp](https://onhyp.com/).

# Installation
```shell
pip install hyp-python-client
```

# Usage
```python
from hyp_client.v1 import HypClient

client = HypClient("PRODUCTION/HYP/5ab8d3d8-6eca-4e11-9203-1b64faea1f33")
client.assignment(participant_id="fuzzybear", experiment_id=8)
# {'payload': {'variant_id': 18, 'variant_name': 'v2'}, 'message': 'success', 'status_code': 200}

client.conversion(participant_id="fuzzybear", experiment_id=8)
# {'payload': {'converted': True}, 'message': 'success', 'status_code': 200}

# No experiment found
client.assignment(participant_id="fuzzybear", experiment_id=13)
# {'payload': '', 'message': 'No experiment with ID 13 was found.', 'status_code': 404}

client.conversion(participant_id="fuzzybear", experiment_id=13)
# {'payload': '', 'message': 'No variant assignment for participant fuzzybear in experiment 8 was found. Participants must be assigned to a variant before conversion can be recorded.', 'status_code': 404}
```
