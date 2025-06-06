import time
import hashlib
import hmac
import requests
import os
import base64

class BitgetAPI:
    def __init__(self):
        self.api_key = os.getenv("BITGET_API_KEY")
        self.api_secret = os.getenv("BITGET_API_SECRET")
        self.api_passphrase = os.getenv("BITGET_API_PASSPHRASE")
        self.base_url = "https://api.bitget.com"

    def _get_timestamp(self):
        return str(int(time.time() * 1000))

    def _sign(self, method, path, timestamp, body=""):
        pre_hash = timestamp + method.upper() + path + body
        h = hmac.new(self.api_secret.encode(), pre_hash.encode(), hashlib.sha256)
        return base64.b64encode(h.digest()).decode()

    def get_positions(self):
        method = "GET"
        path = "/api/mix/v1/position/allPosition"
        query = "productType=USDT-FUTURES"
        timestamp = self._get_timestamp()
        sign = self._sign(method, path + "?" + query, timestamp)

        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": sign,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.api_passphrase,
            "Content-Type": "application/json"
        }

        url = self.base_url + path + "?" + query
        response = requests.get(url, headers=headers)

        try:
            return response.json()
        except Exception:
            return {"error": "invalid json", "raw": response.text}
