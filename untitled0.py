#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 07:36:01 2024

@author: user
"""
from settings import returns
import requests

class ChatUser():
    def __init__(self):
        self.chats = int(input('how many do you need chat?: '))
        self.message= int(input('how many massage per chat?:(maximum)'))
        self.BASE_API_URL, self.HASH_CODES = returns()
        
    def get_bearer_token(self):
        if not self.HASH_CODES:
            print("Error: HASH_CODES is empty!")
        else:
            app_code = self.HASH_CODES  # Replace with your actual app code
            headers = {'X-App-Code': app_code}
    
            response = requests.get(f'{self.BASE_API_URL}passport')
            response.raise_for_status()
            self.user.access_token = response.json().get('access_token')
            return self.user.access_token
chat = ChatUser()
chat.get_bearer_token()