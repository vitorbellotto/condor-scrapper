'This is docstring section for this file'
#!/usr/bin/env python

from setuptools import setup, find_packages
'This is a docstring for the module required for condor-scrapper'

setup(
  name = 'condor-scraper',
  version = '0.1',
  packages = find_packages(),
  install_requires =
    '''
    ludibrio>=3.1.0
    selenium>=2.25.0
    parsedatetime>=0.8.7
    path.py>=2.4.1
    ipdb>=0.7
    '''.split(),
  entry_points = {
    'console_scripts': 'flightscraper = flightscraper:main'
  },
  # extra metadata for pypi
  author = 'Vitor Hugo Bellotto Zago',
  author_email = 'vitorhugobz NOSPAM at REMOVECAPS gmail',
  url = 'http://github.com/yang/flight-scraper',
  description =
    'Drives a browser to search for tickets across multiple airline sites, '
    'scraping/emailing/plotting fare information.',
  license = 'GPL',
  keywords =
    '''
    air airfare airline flight flights search scraper scraping ticket tickets
    travel
    '''.strip(),
  classifiers = [
    'Development Status :: 1 - Alpha',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
  ],
)
