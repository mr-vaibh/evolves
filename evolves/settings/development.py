from .base import *

# Media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# RazorPay configs
from dotenv import load_dotenv

env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

RAZOR_KEY_ID = os.environ.get('RAZOR_KEY_ID', '')
RAZOR_KEY_SECRET = os.environ.get('RAZOR_KEY_SECRET', '')