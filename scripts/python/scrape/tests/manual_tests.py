#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Peter Nagy
Since: March 2016
Description: Manual tests for classes
"""

from scrape.factory.Downloader import Downloader
from scrape.factory.LinkCrawler import LinkCrawler

def downloader_manul_test():
    """Test downloader
    """
    d = Downloader()
    result = d.download("http://electionsireland.org/results/general/32dail.cfm", {'User-agent': 'GMIT-research'}, 2)
    if result['code'] == 200:
        print "It works\n"
    else:
        print "Something broke :( \n"

def link_crawler_manual_test(site_root, site_start=None, depth=2):
    """Test LinkCrawler
    """
    link_crawler = LinkCrawler(site_root, site_start, max_depth=depth)
    result = link_crawler.start_crawl()
    if len(result) > 0:
        print "\n\nFound %d unique links!" % len(result)
        for key, page in result.iteritems():
            print page.get_url()
    else:
        print "\n\nSomething went wrong :("


if __name__ == '__main__':
    downloader_manul_test()
    site_start = 'http://electionsireland.org/results/general/32dail.cfm'
    site_root = 'http://electionsireland.org'
    link_crawler_manual_test(site_root, site_start, 3)
