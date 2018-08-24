import re
import html

from lxml import etree

from goarch_api.client import HTTPClient
from goarch_api.models import Translation, Icon


def remove_html_tags(raw):
    regex = re.compile('<.*?>')
    return html.unescape(re.sub(regex, " ", raw))


class Lectionary:
    # this class will provide full readings from Reading objects
    def __init__(self, _type, code, event, date=None):
        self.type = _type
        self.code = code
        self.event = event
        self.date = date

        self._path = f"/lectionary.asp?type={_type}&code={str(code)}&event={str(event)}"
        self.public_url = f"https://www.goarch.org/chapel/lectionary?type={_type}&code={str(code)}&event={str(event)}"

        if date is not None:
            self._path += f"&date={date}"
            self.public_url += f"&date={date}"

    def get_data(self):
        client = HTTPClient()

        resp = client.get(self._path)

        if resp is not None:
            tree = etree.fromstring(resp.encode())

            self.display_title = tree.find("displaytitle").text
            self.event = tree.find("event").text
            self.prokeimenon = tree.find("prokeimenon").text

            icon = tree.find("icon")
            i_file_path = icon.find("url").text.replace("http://onlinechapel.goarch.org/images/", "")
            i_copyright = icon.find("copyright").text

            self.icon = Icon(i_file_path, i_copyright)

            self.translations = []

            for translation in tree.findall("translation"):
                lang = translation.get("xml:lang")

                if lang != "ar":  # because arabic and the html escape stuff doesn't really work
                    title = translation.find("title").text
                    short_title = translation.find("shorttitle").text
                    clip = translation.find("clip").text.strip()
                    body = remove_html_tags(translation.find("body").text).strip()

                    if self.type == "epistle":
                        prok_mode = translation.find("prokmode").text
                        prok_psalm = translation.find("prokpsalm").text.replace(": ", ":")
                        prok_prokeimenon = translation.find("prokprokeimenon").text
                        prok_verse = translation.find("prokverse").text

                        converted_translation = Translation(lang=lang, title=title, short_title=short_title,
                                                            clip=clip, body=body, prok_mode=prok_mode,
                                                            prok_psalm=prok_psalm, prok_prokeimenon=prok_prokeimenon,
                                                            prok_verse=prok_verse)
                    else:
                        converted_translation = Translation(lang=lang, title=title, short_title=short_title,
                                                            clip=clip, body=body)

                    self.translations.append(converted_translation)
