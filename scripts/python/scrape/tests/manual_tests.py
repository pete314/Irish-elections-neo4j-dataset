#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Peter Nagy
Since: March 2016
Description: Manual tests for classes
"""

from scrape.factory.Downloader import Downloader

if __name__ == '__main__':
    """Test downloader
    """
    d = Downloader()
    result = d.download("http://electionsireland.org/results/general/32dail.cfm", {'User-agent': 'GMIT-research'}, 2)
    if result['code'] == 200:
        print result['html']
    else:
        print "whohoo"
