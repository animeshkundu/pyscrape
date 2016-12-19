from distutils.core import setup, Command

setup(name='pyscrape',
      version='0.0.1',
      description='A lightweight Javascript-aware, headless web scraping library for Python',
      author='Agix',
      author_email='anik.edu@gmail.com',
      license='Apache 2.0',
      url='https://github.com/animeshkundu/pyscrape',
      packages=['pyscrape'],
      install_requires=[
          'webkit_server>=1.0', 
          'lxml', 
          'xvfbwrapper', 
          'tornado', 
          'futures', 
          'fake-useragent'
          ],
      entry_points={
          'console_scripts': [
              'pyscrape = pyscrape.__init__:cli', 
              'pyrun = pyscrape.__init__:http'
              ]
          },
      )
