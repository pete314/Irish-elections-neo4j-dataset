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

def link_crawler_manual_test():
    """Test LinkCrawler
    """
    sites_domain = 'http://electionsireland.org/results/general/32dail.cfm'
    site_test = 'https://blog.crosssec.com'
    link_crawler = LinkCrawler(site_test)
    result = link_crawler.run_thread()
    if len(result) > 0:
        print "Found %d unique links!" % len(result)
        for key, page in result.iteritems():
            print page.get_url()
    else:
        print "Something went wrong :("


if __name__ == '__main__':
    downloader_manul_test()
    link_crawler_manual_test()

