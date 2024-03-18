from SDK import base

from . import settings


class DifyRequestHandler(BaseHTTPSDK):
    PASSPORT_URL = settings.BASE_API_URL + "passport"
    CHAT_MESSAGES_URL = settings.BASE_API_URL + "chat-messages"

    def __init__(self):
        pass

    def get_token(self, app_code):
        response = self.get(self.PASSPORT_URL, headers={"X-App-Code": app_code}, return_response=true)
        return response

    def create_message(self, message, token):
        data = {
            message: message
        }
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.post(
            self.CHAT_MESSAGES_URL,
            data=data,
            headers=headers
        )
        return response
