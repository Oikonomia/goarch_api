import requests
import sys


class HTTPClient:
    def __init__(self):
        self.session = requests.session()

        user_agent = 'goarch_api (https://github.com/Oikonomia/goarch_api 1.0.1), Python/'
        self.user_agent = f"{user_agent}{sys.version_info[0]}.{sys.version_info[1]}"

    def request(self, method, path):
        base_url = "https://onlinechapel.goarch.org"

        headers = {
            "User-Agent": self.user_agent
        }

        url = f"{base_url}{path}"
        resp = self.session.request(method, url, headers=headers)

        exception_strings = {
            "400": "Bad Request",
            "401": "Unauthorized",
            "403": "Forbidden",
            "500": "Internal Server Error",
            "501": "Not Implemented",
            "502": "Bad Gateway",
            "503": "Service Unavailable"
        }

        if str(resp.status_code) in exception_strings.keys():
            raise Exception(exception_strings[str(resp.status_code)])
        else:
            return resp.text

    def get(self, url):
        return self.request("GET", url)