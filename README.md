goarch_api
===
[![PyPI](https://img.shields.io/pypi/v/goarch-api.svg)](https://pypi.org/project/goarch-api/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/goarch_api.svg)](https://pypi.org/project/goarch-api/)

!! **Unusable, read below.** !!

A Python interface for the Greek Orthodox Archdiocese of America's Chapel API.

Install through pip: `pip install goarch-api`

Documentation coming soon.

----

### Usability

This interface is no longer able to (properly) be used as the API is behind Cloudflare, which will detect requests with this library through its anti-bot protection. You could attempt to get cloudscraper or cfscrape to work with this, but those projects are too unreliable for implementation here. There might be other ways to do this, like through a headless browser or so on, but it ends up being too impractical for something this small. I plan on making an interface that scrapes the OCA's website, but in the meantime there's nothing that I can do.
