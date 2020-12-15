import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# proxy examples
proxies = {
	"http": "http://20cfyJ:FpGWu9@45.133.220.119:8000",
	"https": "https://20cfyJ:FpGWu9@45.133.220.119:8000"
}

s = requests.Session()
# uncomment line below if you want to use proxy
# s.proxies = proxies

def telegram_bot_sendtext(bot_message):
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&parse_mode=html&text=' + bot_message
    response = s.get(send_text)
    return response.json()