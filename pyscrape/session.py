from webkit import Driver as DefaultDriver

from itertools import chain
try:
    import urlparse
except ImportError:
    import urllib
    urlparse = urllib.parse

class Session(object):
    def __init__(self,
            driver = None,
            base_url = None):
        self.driver = driver or DefaultDriver()
        self.base_url = base_url

    # implement proxy pattern
    def __getattr__(self, attr):
        return getattr(self.driver, attr)

    def __dir__(self):
        dir_chain = chain(dir(type(self)), dir(self.driver))
        return list(set(dir_chain))

    def visit(self, url):
        return self.driver.visit(self.complete_url(url))

    def complete_url(self, url):
        if self.base_url:
            return urlparse.urljoin(self.base_url, url)
        else:
            return url
