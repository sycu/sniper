import re

from bs4 import BeautifulSoup


class AbstractMatcher(object):
    def match(self, html: str) -> int:
        raise NotImplementedError()


class CountRegexpMatcher(AbstractMatcher):
    def __init__(self, pattern: str):
        self.pattern = pattern

    def match(self, html: str) -> int:
        match = re.search(self.pattern, html)
        return int(match.group(1))


class SelectorMatcher(AbstractMatcher):
    def __init__(self, selector: str):
        self.selector = selector

    def match(self, html: str) -> int:
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.select(self.selector)
        return len(results)
