import argparse
import logging
from locust import HttpUser, task, between, User


class ChatUser(HttpUser):
    wait_time = between(1, 3)  # Random wait time between requests

    def on_start(self):
        try:
            self.get_bearer_token()
            self.create_message()
        except Exception as e:
            logging.error(f"Error during task execution: {str(e)}")

    def get_bearer_token(self):
        app_code = 'n8HgfIAGLskbEfZr'  # Replace with your actual app code
        headers = {'X-App-Code': app_code}

        response = self.client.post('/api/passport', headers=headers)
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


class CommandLineUser(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_count = int(kwargs.pop('users_count', 1))


def main():
    parser = argparse.ArgumentParser(description='Locust test for chat application')
    parser.add_argument('--users', type=int, default=1, help='Number of users to simulate')
    args = parser.parse_args()

    CommandLineUser.users_count = args.users
    CommandLineUser.host = 'https://baas-dev.buildai.company'  # Replace with your chat app host

    CommandLineUser.tasks = [ChatUser]
    CommandLineUser.wait_time = between(1, 3)

    import locust.main
    locust.main.main()


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)  # Set logging level to ERROR for cleaner output
    main()
