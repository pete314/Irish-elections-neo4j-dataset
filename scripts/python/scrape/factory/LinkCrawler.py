#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Peter Nagy
Since: March 2016
Description: Link Crawler
Partial-Source: Peter Nagy https://github.com/pete314/cap-crawler/
"""

import robotparser
import urlparse
import hashlib
import sys
import os
from Queue import Queue
from Downloader import Downloader
from BeautifulSoup import BeautifulSoup
from scrape.entity.PageEntity import PageEntity
from scrape.factory.ElectionsIrelandScraper import ElectionsIrelandScraper

DEFAULT_AGENT = 'Mozilla/5.0 (compatible; http://research.gmit.ie/)'
DEFAULT_SCRAPER = ElectionsIrelandScraper("")

def url_md5_digest(url):
    """Simple method to create md5 to speed up dict and save memory"""
    return hashlib.md5(url).hexdigest()


class LinkCrawler(object):
    def __init__(self, site_domain, starting_url=None, focus_link_bits = list(), page_map=None, timeout=60, user_agent=None, max_depth=2, scraper=DEFAULT_SCRAPER):
        """
        Init link crawler
        :param site_domain: The domain to check
        :param starting_url: The starting point for crawling, or None if root
        :param page_map: dist(PageEntity) or none
        :param timeout: time to wait between trying the page again
        :param user_agent: HTTP header
        :return:
        """
        self.site_domain = site_domain
        self.starting_url = site_domain if starting_url is None else starting_url
        self.page_map = dict() if page_map is None else page_map
        self.queue = Queue()
        self.user_agent = DEFAULT_AGENT if user_agent is None else user_agent
        self.downloader = Downloader(delay_time=timeout)
        self.robots = self.parse_robots_file(self.site_domain)
        self.max_depth = max_depth
        self.visited_pages = dict()
        self.depth_cnt = 0
        self.scraper = scraper
        self.focus_link_bits = focus_link_bits

    def start_crawl(self):
        print "Start crawling \n"
        dummy_q = Queue()
        dummy_q.put(self.starting_url)
        return self.process_list(dummy_q)


    def process_list(self, url_queue):
        """Processing url queue with depth
        @todo: This should be refactored, problems:
                >Depth logic clean
                >Threading only possible with RLock
        :param url_queue Queue() with String urls
        :return dict(PageEntity())
        """
        while not url_queue.empty():
            sys.stdout.write("\rDepth %d, Url Processed %d" % (self.depth_cnt, len(self.visited_pages)))
            sys.stdout.flush

            url = url_queue.get()
            url_digest = url_md5_digest(url)
            if self.robots.can_fetch(self.user_agent, url) and not self.visited_pages.has_key(url_digest):
                result = self.downloader(url)
                if result['code'] is 200:
                    """ DEBUG ONLY print("Status for %s is %s" % (site, result['code'])) """
                    self.scrap_content_links(result['html'], url)
                    self.visited_pages[url_digest] = True
            else:
                print("\nWARNING - Page blocked by robots or visited")

        print '\n-------'
        # Recursively call itself to reach depth
        self.depth_cnt += 1
        if self.max_depth is 0:
            self.process_list(self.queue)
        elif self.max_depth > self.depth_cnt:
            current_depth_links = self.queue
            self.queue = Queue()
            self.process_list(current_depth_links)

        return self.page_map

    def scrap_content_links(self, html=None, site=None, same_domain_only=True):
        """
        Regex the links from the downloaded content
        :param html: downloaded html content
        :param site: the base url to compare to
        :param same_domain_only: (True) - does not look for external links
        :return: links[] - list of all link on page
        """
        if html is None:
            return
        else:

            """
            Debug only
            write_to_disk(site, html)
            """
            if self.scraper is not None and isinstance(self.scraper, ElectionsIrelandScraper):
                data_scraper = ElectionsIrelandScraper(html)
                data_scraper.check_content_page(site)

            links = []
            soup = BeautifulSoup(html)
            for tag in soup.findAll('a', href=True):
                if tag['href'] != '#' and not links.__contains__(tag['href']):
                    link = self.normalize_link(site, tag['href'])
                    if same_domain_only and self.check_same_domain(site, link):
                        # THIS WILL EXCLUDE EXTERNAL LINKS AND ONLY LOOK FOR LINKS ON SAME DOMAIN
                        link_hash = url_md5_digest(link)
                        if not self.page_map.has_key(link_hash) and self.check_link_in_focus(link):
                            # THIS WILL TAKE CARE OF DUPLICATES
                            self.page_map[link_hash] = PageEntity(link)
                            self.queue.put(link)

    def normalize_link(self, site, link):
        """
        Remove hash and add site url to relative links
        :param site: The base url of the site
        :param link: The link to work with
        :return:
        """
        link, _ = urlparse.urldefrag(link)
        return urlparse.urljoin(site, link)

    def check_same_domain(self, site_base_url, check_url):
        """
        Check if url is same domain
        :param site_base_url: base url to compare to
        :param check_url: url to validate
        :return: bool
        """
        return urlparse.urlparse(site_base_url).netloc == urlparse.urlparse(check_url).netloc

    def parse_robots_file(self, base_url):
        """
        Parse the robot file if exists
        :param base_url: The base url to parse robots.txt from
        :return: RobotFileParser
        """
        parse_rf = robotparser.RobotFileParser()
        parse_rf.set_url(urlparse.urljoin(base_url, '/robots.txt'))
        parse_rf.read()
        return parse_rf

    def check_link_in_focus(self, link):
        if len(self.focus_link_bits) == 0:
            return True

        for str_bits in self.focus_link_bits:
            if str_bits in link:
                return True

        return False

# ++++++++++++++++++++
# Static functions From here
def write_to_disk(file_name, html):
    file_name = file_name.replace("/", "_") + ".html"
    file_name = file_name.replace(":", "-")
    file_name = file_name.replace("?", "QM")
    base_path = os.path.dirname(__file__)
    file_path = os.path.abspath(os.path.join(base_path, "..", "..", "scraped_data", file_name))

    with open(file_path, 'w+') as file_pointer:
        file_pointer.write(html)
