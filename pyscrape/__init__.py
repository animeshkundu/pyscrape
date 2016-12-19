import argparse

from session import *
from xvfb import *
from http import run_server

def cli():
    parser = argparse.ArgumentParser(description="Download Javscript rendered web pages")
    parser.add_argument("url", help="The url to download after rendering")
    xvfb.start_xvfb()
    s = session.Session()
    s.visit(url)
    print s.body()

def http() :
    parser = argparse.ArgumentParser(description="Download Javscript rendered web pages")
    parser.add_argument("--port", "-p", default="1234", help="The port the server will bind to")
    run_server(args.port)

 __name__ == "__main__" :
     cli()
