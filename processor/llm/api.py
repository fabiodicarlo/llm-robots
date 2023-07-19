import requests
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class LlmApi:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:6500'
        self.url_input_data = self.base_url + '/api/input_data/'
        self.url_check_status = self.base_url + '/api/check_status/'
        self.url_get_processed_data = self.base_url + '/api/get_processed_data/'

    def check_status(self):
        response = requests.post(self.url_check_status)
        logging.debug(response.json())
        return response.json()["ready"]

    def set_data(self, question):
        response = requests.post(self.url_input_data, json={"command": question})
        logging.debug(response.json())

    def get_processed_data(self):
        response = requests.post(self.url_get_processed_data)
        if response.status_code == 200:
            result = response.json()
            logging.debug(result)
            return result
        return None
