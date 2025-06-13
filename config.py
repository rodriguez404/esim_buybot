import os
from dotenv import load_dotenv
import json

load_dotenv()

BOT_TOKEN = os.getenv("bot_token")
PAYMENTS_TOKEN = os.getenv("payments_token")
SUPPORTED_LANGUAGES = {"ru", "en"}
try:
    ADMINS = json.loads(os.getenv("admins_list"))
except:
    ADMINS = []
    
class DATABASE:
    HOST = os.getenv("database_host")

class REDIS:
    HOST_URL = os.getenv("redis_host_url")
    PORT = os.getenv("redis_port")

class ESIM:
    ACCESS_CODE = os.getenv("esim_access_code")
    SECRET_KEY = os.getenv("esim_secret_key")
    HOST_API_URL = os.getenv("esim_host_api_url")
    API_PACKAGELIST_URL = os.getenv("esim_api_packagelist_url")