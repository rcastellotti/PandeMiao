import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
