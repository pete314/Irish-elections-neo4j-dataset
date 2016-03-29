#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Peter Nagy
Since: 03 2016
Project: python
Description: This is a wrapper for the scrape task
"""

from scrape.factory.LinkCrawler import LinkCrawler
from multiprocessing.dummy import Pool as ThreadPool

def return_election_date_for_filter(dail_num):
    dates = {
        '32': 2016,
        '31': 2011,
        '30': 2007,
        '29': 2002,
        '28': 1997,
        '27': 1992,
        '26': 1989,
        '19': 1969,
        '18': 1965,
        '17': 1961,
        '16': 1957,
        '15': 1954,
        '14': 1951,
        '13': 1948,
        '12': 1944,
        '11': 1943,
        '10': 1938,
        '09': 1937,
        '08': 1933,
        '07': 1932,
        '06': 1927,
        '05': 1927,
        '04': 1923,
        '03': 1922,
        '02': 1921,
        '01': 1918,
    }
    return dates[dail_num]


def print_header(site_base_url, site_starting_point, depth_no, focus_list):
    print "****************************"
    print "* SCRAPER PROCESS STARTED"
    print "* Site: %s" % site_base_url
    print "* Starting @: %s" % site_starting_point
    print "* Depth: %d" % depth_no
    print "* Focus: %s" % focus_list
    print "* Scraper: HARD CODED"
    print "***************************"

def startin_scraper(dail_no = 32):
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
    site_starting_point = 'http://electionsireland.org/results/general/' + dail_no + 'dail.cfm'
    depth_no = 3
    # This will result in 9700 pages to scrape with dept=4
    # focus_set = {"election", "candidate", "party", "dail", "general"}
    # This will result in 3428 pages scraped with dept=3
    focus_set = {"election=" + str(return_election_date_for_filter(dail_no)), "candidate.cfm?ID="}
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

    startin_scraper("32")

    """ RUN As threads

    num_list = ["32", "30", "29", "28", "27", "26"]

    pool = ThreadPool(6)
    result = pool.map(startin_scraper, num_list)

    pool.close()
    pool.join()
    """

