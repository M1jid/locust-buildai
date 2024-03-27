
# Load Testing with Locust

## Overview
This repository contains scripts for load testing a chatbot API using Locust. Locust is an open-source load testing tool that allows you to define user behavior using Python code.

## Prerequisites
Before running the load tests, ensure you have the following installed:
-requirements.txt


## Setup
1. **Clone this repository to your local machine:**
   ```bash
   git clone <repository-url>
   cd locust-chatbot-load-testing
Set up a virtual environment (optional but recommended):

bash
pip install -r requirements.txt
Configuration
Open the config.ini file in the project root directory.
Adjust the parameters as needed:
chats: Number of concurrent chats to simulate.
messages: Number of messages to send per chat.
Running the Tests
Ensure your virtual environment is activated (if using).

Navigate to the project directory.

Execute the following command to start the Locust web interface:

bash
locust -f locusttest.py
Open your web browser and go to http://localhost:8089.

Enter the desired number of users to simulate and the hatch rate, then click "Start swarming".

Monitor the test results in the web interface.

Customization
You can modify the locusttest.py file to define custom user behaviors or scenarios.
Note
Ensure to review and adjust the code and configurations according to your specific requirements before running the tests.

options:
--host
locust -f locusttest.py --host=http://baas-dev.buildai.company/api/

REA

