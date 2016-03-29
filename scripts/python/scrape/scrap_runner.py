#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Peter Nagy
Since: 03 2016
Project: python
Description: This is a wrapper for the scrape task
"""

from scrape.factory.LinkCrawler import LinkCrawler


def print_header(site_base_url, site_starting_point, depth_no, focus_list):
    print "****************************"
    print "* SCRAPER PROCESS STARTED"
    print "* Site: %s" % site_base_url
    print "* Starting @: %s" % site_starting_point
    print "* Depth: %d" % depth_no
    print "* Focus: %s" % focus_list
    print "* Scraper: HARD CODED"
    print "***************************"

def startin_scraper():
    """
    Running a crawling, scraping process
    Environment: cmd
    Warning: The crawler visits pages onece and filters visited pages.
             With default settings it will only crawl pages belongs to same site.
             If the depth is set to higher number the process is growing exponentially.
             In this setup it could crawl ~34000 pages, from electionsireland.org!!!
             Site is crawled with timeout and back-off time, to avoid knock the site offline.
             If crawler is blocked by robots.txt the page want be crawled(favour ethical crawling).

    :return: None
    """
    site_base_url = 'http://electionsireland.org'
    site_starting_point = 'http://electionsireland.org/results/general/index.cfm'
    depth_no = 4
    focus_set = {"election", "candidate", "party", "dail", "general"}
    print_header(site_base_url, site_starting_point, depth_no, focus_set)

    #START the process
    link_crawler = LinkCrawler(site_base_url, site_starting_point, max_depth=depth_no, focus_link_bits=focus_set)
    result = link_crawler.start_crawl()
    if len(result) > 0:
        print "\n\nFound %d unique links!" % len(result)
        for key, page in result.iteritems():
            print page.get_url()
    else:
        print "\n\nSomething went wrong :("


if __name__ == "__main__":
    startin_scraper()