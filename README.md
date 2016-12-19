PyScrape
========

Javascript frameworks are all the rage now. Unfortunately that means some of my favourite tools, wget and curl, are no longer up to the task. Loading up a page on the browser then opening up source and then copying it is just too cumbersome.

I initially thought of creating an extension to help with the situation. Unfortunately an extension would never have the seamless feel of wget or curl for the unfortunate ones like me who are in a relationship with the terminal. Also an extension cannot be used in those quick and dirty bash/perl/python scripts.

Hence `pyscrape` and its http sibling `pyrun`. Hope it helps you navigate the unwieldy world of javascript rendering :) .

PyPI package - [scrapejs](https://pypi.python.org/pypi/scrapejs)


## Installation
sudo apt-get install qt5-default libqt5webkit5-dev build-essential python-lxml xvfb

pip install scrapejs

OR

1. Clone https://github.com/animeshkundu/pyscrape
2. pip install -r requirements.txt
3. python setup.py install


## Test
1. pyscrape http://www.google.co.in/
2. pyrun -p 1234; curl localhost:1234/scrape?url=http://www.google.co.in/


Improvements are welcome
