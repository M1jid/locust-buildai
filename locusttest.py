import configparser
import sys
import logging
import settings
import re


from locust import HttpUser, task, between


class Config:
    @classmethod
    def load(cls):
        config = configparser.ConfigParser()
        config.read('config.ini')
        chats = int(config.get('chats', 'count', fallback=1))
        messages = int(config.get('messages', 'count', fallback=1))
        return chats, messages

class CommandLineUser(HttpUser):
    wait_time = between(2, 5)
    BASE_API_URL = "https://baas-dev.buildai.company/api/"
    HASH_CODES = "n8HgfIAGLskbEfZr"
    is_creating_chat = True  
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = None

    def on_start(self):
        try:
            if not self.access_token:
                self.access_token = self.get_bearer_token()
                if not self.access_token:
                    sys.exit(1)
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

            if response.status_code != 200:
                logging.error(f"Failed to retrieve access token. Status code: {response.status_code}")
                return None

            logging.info(f"Access token retrieved with status code: {response.status_code}")
            return response.json().get('access_token')

    @task
    def create_chat(self):
        chats, messages = Config.load()
        if self.is_creating_chat:
            try:
                if not self.access_token:
                    logging.error("Error: Access token is missing!")
                    
                headers = {
                    'Authorization': f'Bearer {self.access_token}'
                }
                payload = {
                    'inputs': [],
                    "conversation_id":'',
                    'query': 'Hello, chatbot!',
                    'response_mode': 'streaming'
                }
                for _ in range(chats):
                    response = self.client.post(f'{self.BASE_API_URL}chat-messages', headers=headers, json=payload)
                    response.raise_for_status()

                    pattern = r'"conversation_id": "(.+?)"'
                    response_text = response.text
                    conversation_ids = re.findall(pattern,response_text )
                    unique_conversation_ids = {conversation_id: None for conversation_id in conversation_ids}

                    self.unique_conversation_ids = list(unique_conversation_ids.keys())
                    # print(response.text)
                    logging.info(f"chat created with status code: {response.status_code}")
                    self.is_creating_chat = False
                
                    
 
                    
    
            except Exception as e:
                logging.error(f"Error during message creation: {str(e)}")



        
    
     
        self.is_creating_chat = True   
    @task
    def create_message(self):
         
        chats, messages = Config.load()
        if self.is_creating_chat:
            try:
                if not self.access_token:
                    logging.error("Error: Access token is missing!")
                    
                headers = {
                    'Authorization': f'Bearer {self.access_token}'
                }
                payload = {
                    'inputs': [],
                    "conversation_id":self.unique_conversation_ids[0],
                    'query': 'Hello, chatbot!',
                    'response_mode': 'streaming'
                }
                for _ in range(messages):
                    response_chat = self.client.post(f'{self.BASE_API_URL}chat-messages', headers=headers, json=payload)
                    response_chat.raise_for_status()

                    logging.info(f"message created with status code: {response_chat.status_code}")
                self.is_creating_chat = False

                print(response_chat.text)

    

            except Exception as e:
                logging.error(f"Error during message creation: {str(e)}")   

    def main(self):
        logging.basicConfig(level=logging.INFO)
        CommandLineUser.host = settings.BASE_API_URL
        CommandLineUser.wait_time = between(1, 3)
        CommandLineUser.wait_time = 0


if __name__ == "__main__":
    user = CommandLineUser()
    user.main()