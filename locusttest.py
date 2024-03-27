import configparser
import sys
import logging
import settings
import random
from locust import HttpUser, task, between


class Config:
    @classmethod
    def load(cls):
        config = configparser.ConfigParser()
        config.read('config.ini')
        cls.chats = int(config.get('chats', 'count', fallback=1))
        cls.messages = int(config.get('messages', 'count', fallback=1))


class CommandLineUser(HttpUser):
    wait_time = between(5, 15)
    # BASE_API_URL = settings.BASE_API_URL
    BASE_API_URL = "https://baas-dev.buildai.company/api/"
    #HASH_CODES = settings.HASH_CODES 
    HASH_CODES = "n8HgfIAGLskbEfZr1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Config.load()
        self.access_token = None
        self.random_number = random.randint(1, Config.messages)

    def on_start(self):
        try:
            if not self.access_token:
                self.access_token = self.get_bearer_token()
                if not self.access_token:
                    sys.exit(1)
            # self.create_message()
        except Exception as e:
            logging.error(f"Error during task execution: {str(e)}")

    def get_bearer_token(self):
        if not self.HASH_CODES:
            logging.error("Error: HASH_CODES is empty!")
        else:
            app_code = self.HASH_CODES
            headers = {'X-App-Code': app_code}
            response = self.client.get(f'{self.BASE_API_URL}passport', headers=headers)
            logging.info(response)
            
            # response.raise_for_status()
            logging.info(f"Access token retrieved with status code: {response.status_code}")
            return response.json().get('access_token')
            

    @task
    def create_message(self):
        try:
            if not self.access_token:
                logging.error("Error: Access token is missing!")
                return
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            payload = {
                'inputs': [],
                'query': 'Hello, chatbot!',
                'response_mode': 'streaming'
            }
            response = self.client.post(f'{self.BASE_API_URL}chat-messages', headers=headers, json=payload)
            response.raise_for_status()
            logging.info(f"Message created with status code: {response.status_code}")
        except Exception as e:
            logging.error(f"Error during message creation: {str(e)}")


def main():
    logging.basicConfig(level=logging.INFO)
    CommandLineUser.host = settings.BASE_API_URL
    CommandLineUser.wait_time = between(1, 3)
    CommandLineUser.wait_time = 0


if __name__ == "__main__":
    main()
