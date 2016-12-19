import argparse

from session import *
from xvfb import *
from http import run_server

def cli():
    parser = argparse.ArgumentParser(description="Download Javscript rendered web pages")
    parser.add_argument("url", help="The url to download after rendering")
    args = parser.parse_args()

    start_xvfb()
    s = Session()
    s.visit(args.url)
    print s.body().encode("utf8")


def http() :
    parser = argparse.ArgumentParser(description="Download Javscript rendered web pages")
    parser.add_argument("--port", "-p", default="1234", help="The port the server will bind to")
    args = parser.parse_args()

    run_server(args.port)


if __name__ == "__main__" :
    cli()
