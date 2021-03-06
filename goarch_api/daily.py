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

from lxml import etree

from goarch_api.client import HTTPClient
from goarch_api.models import Reading, Translation
from goarch_api.saint import Saint


class Daily:
    def __init__(self, date=None):
        self.date = date
        self._path = "/daily.asp"
        self.public_url = "https://www.goarch.org/chapel"

        if date is not None:
            self._path += f"?date={date}"
            self.public_url += f"?date={date}"

        self.formatted_date = None
        self.icon = None
        self.fasting = None
        self.tone = None
        self.readings = []
        self.lectionary_title = None
        self.saints = []

    def get_data(self):
        client = HTTPClient()

        resp = client.get(self._path)

        if resp is not None:
            tree = etree.fromstring(resp.encode())
            date = tree.find("date").text

            self.formatted_date = tree.find("formatteddate").text

            self.icon = tree.find("icon").text
            self.fasting = tree.find("fasting").text

            if tree.find("tone") is not None:
                self.tone = tree.find("tone").text

            for reading in tree.find("readings").iterchildren():
                _id = reading.get("id")
                _type = reading.find("type").text
                type_bb = reading.find("typebb").text
                event = reading.find("event").text

                translation = reading.find("translation")
                t_lang = translation.get("{http://www.w3.org/XML/1998/namespace}lang")
                t_title = translation.find("title").text
                t_short_title = translation.find("shorttitle").text

                # more often than not, these things have a newline after the text in the element
                t_clip = translation.find("clip").text.strip()

                converted_translation = Translation(title=t_title, short_title=t_short_title, clip=t_clip, lang=t_lang)

                converted_reading = Reading(_id, _type, type_bb, event, translation=converted_translation, date=date)

                self.readings.append(converted_reading)

            self.lectionary_title = tree.find("lectionarytitle").text.strip()

            self.saints = []

            for saint in tree.find("saintsfeasts").iterchildren():
                _id = saint.find("id").text
                converted_saint = Saint(_id)

                self.saints.append(converted_saint)
