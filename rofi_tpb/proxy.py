from typing import List
from urllib.request import Request, urlopen

from lxml.etree import HTML

from .settings import HEADERS, PROXY_URL


def get_proxies() -> List[str]:

    req = Request(PROXY_URL, None, HEADERS)
    return HTML(urlopen(req).read()).xpath("//td[@class='site']/a/@href")
