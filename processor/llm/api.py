import requests
import json

headers = {'ngrok-skip-browser-warning': 'true'}


class LlmApi:
    def __init__(self):
        self.base_url = 'https://c598-35-192-57-179.ngrok-free.app'
        self.url_colab_question = self.base_url + '/ai/question'
        self.url_colab_answer = self.base_url + '/ai/answer'
        self.url_colab_queue = self.base_url + '/ai/queue'

    def schema_answer(self):
        schema = {
            "type": "object",
            "properties": {
                "subject": {"type": "string"},
                "verb": {"type": "string"},
                "object": {"type": "string"},
            }
        }
        return schema

    def api_start_queue(self):
        requests.post(self.url_colab_queue, headers=headers, timeout=None)

    def api_send_question(self, question):
        data = {
            'question': question,
            'schema': json.dumps(self.schema_answer())
        }
        requests.post(self.url_colab_question, headers=headers, data=data, timeout=None)

    def api_get_answer(self):
        response = requests.post(self.url_colab_answer, headers=headers, timeout=None)
        if response.status_code == 200:
            return response.json()
        return None
