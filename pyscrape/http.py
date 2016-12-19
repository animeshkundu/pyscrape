import sys
import tornado.gen
import tornado.web
import tornado.ioloop
import tornado.concurrent
import concurrent.futures
from fake_useragent import UserAgent

import xvfb
import session

def run_server(port) :
    app = tornado.web.Application([
        (r"/ping", PingHandler),
        (r"/", ScrapeHandler),
        (r"/scrape", ScrapeHandler),
        ])
    app.listen(port)
    xvfb.start_xvfb()
    tornado.ioloop.IOLoop.current().start()


class PingHandler(tornado.web.RequestHandler) :
    def get(self) :
        self.write("OK GET")

    def post(self) :
        self.write("OK POST")

class ScrapeHandler(tornado.web.RequestHandler) :
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=16)
    ua = UserAgent()

    @tornado.concurrent.run_on_executor
    def worker(self, url) :
        r = None
        if url :
            s = session.Session()
            s.set_header('User-Agent', self.ua.random)
            s.visit(url)
            r = s.body()
            s.reset()
        print url, len(r)
        return r

    @tornado.gen.coroutine
    def get(self) :
        url = self.get_query_argument('url')
        response = yield self.worker(url)
        self.write(response)

    @tornado.gen.coroutine
    def post(self) :
        url = self.get_body_argument('url')
        response = yield self.worker(url)
        self.write(response)

if __name__ == "__main__" :
    run_server(1234)
