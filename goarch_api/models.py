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


class Reading:
    def __init__(self, _id, _type, type_bb, event, translation=None, date=None):
        self.id = _id
        self.type = _type
        self.type_bb = type_bb
        self.event = event
        self.translation = translation
        self.date = date

        is_gospel = (_type == "G" and type_bb == "gospel")
        is_epistle = (_type == "E" and type_bb == "epistle")
        is_matins = (_type == "MG" and type_bb == "mg")
        is_ot = (_type == "OT" and type_bb == "ot")

        if not (is_ot ^ is_gospel ^ is_epistle ^ is_matins):
            raise Exception("Invalid or mismatching reading types.")

        if is_epistle:
            if date is None:
                raise Exception("Epistles must have the 'date' keyword argument.")


class Translation:
    def __init__(self, **kwargs):
        self.lang = kwargs["lang"] if "lang" in kwargs.keys() else None

        self.title = kwargs["title"] if "title" in kwargs.keys() else None
        self.short_title = kwargs["short_title"] if "short_title" in kwargs.keys() else None

        self.clip = kwargs["clip"] if "clip" in kwargs.keys() else None

        self.prok_mode = kwargs["prok_mode"] if "prok_mode" in kwargs.keys() else None
        self.prok_psalm = kwargs["prok_psalm"] if "prok_psalm" in kwargs.keys() else None
        self.prok_prokeimenon = kwargs["prok_prokeimenon"] if "prok_prokeimenon" in kwargs.keys() else None
        self.prok_verse = kwargs["prok_verse"] if "prok_verse" in kwargs.keys() else None

        self.body = kwargs["body"] if "body" in kwargs.keys() else None

        self.copyright = kwargs["_copyright"] if "_copyright" in kwargs.keys() else None


class Icon:
    def __init__(self, file_path, _copyright, _id=None):
        self.id = _id
        self.file_path = file_path
        self.url = f"https://onlinechapel.goarch.org/images/{file_path}"
        self.copyright = _copyright


# this is like a Reading/Translation hybrid
class LectionaryReading:
    def __init__(self, _id, _type, title, short_title):
        self.id = _id
        self.type = _type
        self.title = title
        self.short_title = short_title


class Hymn:
    def __init__(self, _type, title, short_title, tone, translation):
        self.type = _type.title()
        self.title = title
        self.short_title = short_title
        self.tone = tone
        self.translation = translation
