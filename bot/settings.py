'''Load settings from the environment.'''

import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')

NEO4J_USERNAME = os.environ.get('NEO4J_USERNAME')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD')
NEO4J_URI = os.environ.get('NEO4J_URI')
NEO4J_ENCRYPTED = not os.environ.get('NEO4J_ENCRYPTED') == "Off"
