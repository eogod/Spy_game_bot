from os import getenv
from dotenv import load_dotenv

def load_config():
    """Load environment variables from a .env file and return the BOT_TOKEN."""
    load_dotenv()
    bot_token = getenv('BOT_TOKEN')
    if bot_token is None:
        raise ValueError("BOT_TOKEN not found in environment variables. Please check your .env file.")

    return bot_token

def load_database():
    load_dotenv()
    base_url = getenv('DATABASE_URL')
    if base_url is None:
        raise ValueError("Database url is not set. Please check your .env file")

    return base_url