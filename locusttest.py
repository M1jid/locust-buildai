from locust import HttpUser, task, between
import configparser
import logging
from settings import returns
import random

class Config:
    @classmethod
    def load(cls):
        config = configparser.ConfigParser()
        config.read('config.ini')
        cls.chats = int(config['chats']['count'])
        cls.messages = int(config['messages']['count'])

class CommandLineUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Config.load()  # Load config attributes
        self.wait_time = between(5, 15)  # Random wait time between requests
        self.BASE_API_URL, self.HASH_CODES = returns()
        
        try:
            self.random_number = random.randint(1, Config.messages)
        except ValueError:
            print("Error: Input number should be greater than zero!")
            
    def on_start(self):
        try:
            self.get_bearer_token()
            self.create_message()
        except Exception as e:
            logging.error(f"Error during task execution: {str(e)}")

    def get_bearer_token(self):
        if not self.HASH_CODES:
            print("Error: HASH_CODES is empty!")
        else:
            app_code = self.HASH_CODES  # Replace with your actual app code
            headers = {'X-App-Code': app_code}

            response = self.client.get(f'{self.BASE_API_URL}passport', headers=headers)
            response.raise_for_status()
            self.user.access_token = response.json().get('access_token')

    @task
    def create_message(self):
        try:
            headers = {'Authorization': f'Bearer {self.user.access_token}'}
            payload = {'user_id': self.user.username, 'message': 'Hello, chatbot!'}
            response = self.client.post('/chat', headers=headers, json=payload)
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Error during message creation: {str(e)}")


def main():
    CommandLineUser.host = 'https://baas-dev.buildai.company'  # Replace with your chat app host
    CommandLineUser.wait_time = between(1, 3)

    import locust.main
    locust.main.main()


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)  # Set logging level to ERROR for cleaner output
    main()
