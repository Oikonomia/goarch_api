"""
    Copyright (c) 2018-2019 Elliott Pardee <me [at] vypr [dot] xyz>
    This file is part of goarch_api.

    goarch_api is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    goarch_api is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with goarch_api.  If not, see <http://www.gnu.org/licenses/>.
"""

import requests
import sys


class HTTPClient:
    def __init__(self):
        self.session = requests.session()

        base_ua = 'goarch_api (https://github.com/vypr/goarch_api 1.1.0), Python/'
        self.user_agent = f"{base_ua}{sys.version_info[0]}.{sys.version_info[1]}"

    def request(self, method, path):
        base_url = "http://onlinechapel.goarch.org"

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
