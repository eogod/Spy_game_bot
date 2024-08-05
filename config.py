import os
from dotenv import load_dotenv

def load_config():
    """Load environment variables from a .env file and return the BOT_TOKEN."""
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    if bot_token is None:
        raise ValueError("BOT_TOKEN not found in environment variables. Please check your .env file.")

    return bot_token
