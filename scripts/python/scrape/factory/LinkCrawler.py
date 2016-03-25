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
import threading
from Queue import Queue
from Downloader import Downloader
from BeautifulSoup import BeautifulSoup
from scrape.entity.PageEntity import PageEntity

DEFAULT_AGENT = 'Mozilla/5.0 (compatible; http://research.gmit.ie/)'

def url_md5_diggest(url):
    """Simple method to create md5 to speed up dict and save memory"""
    return hashlib.md5(url).hexdigest()

class LinkCrawler(object):
    lock = threading.RLock()

    def __init__(self, site_domain, page_map=None, max_threads=10, timeout=60, user_agent=None, max_depth=2):
        """
        Intit link crawler
        :param site_domain:
        :param page_map:
        :param max_threads:
        :param timeout:
        :param user_agent:
        :return:
        """
        self.site_domain = site_domain
        self.queue = Queue()
        self.page_map = dict() if page_map is None else page_map
        self.max_threads = max_threads
        self.timeout = timeout
        self.user_agent = DEFAULT_AGENT if user_agent is None else user_agent
        self.threads = []
        self.downloader = Downloader()
        self.robots = None
        self.max_depth = max_depth

    def process_list(self, is_thread=False):
        if not is_thread:
            self.queue.put(self.site_domain)
            self.robots = self.parse_robots_file(self.site_domain)

        dept_cnt = 0
        while not self.queue.empty() and dept_cnt < self.max_depth:
            site = self.queue.get()
            if self.robots.can_fetch(self.user_agent, site):
                result = self.downloader(site)
                if result['code'] is 200:
                    """ DEBUG ONLY print("Status for %s is %s" % (site, result['code'])) """
                    self.scrap_content_links(result['html'], site)
            else:
                print("Page blocked by robots")

            dept_cnt += 1

        if not is_thread:
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
            links = []
            soup = BeautifulSoup(html)
            for tag in soup.findAll('a', href=True):
                if tag['href'] != '#' and not links.__contains__(tag['href']):
                    link = self.normalize_link(site, tag['href'])
                    if same_domain_only and self.check_same_domain(site, link):
                        # THIS WILL EXCLUDE EXTERNAL LINKS AND ONLY LOOK FOR LINKS ON SAME DOMAIN
                        link_hash = url_md5_diggest(link)
                        if not self.page_map.has_key(link_hash):
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

    def run_thread(self):
        """
        Execute process_list in threads after getting the first
        """
        self.process_list()
        t_list = list()
        for i in range(0, self.max_threads):
            t = threading.Thread(target=self.process_list(False))
            t.start()
            t_list.append(t)

        # Join the threads
        while t_list.count() > 0:
            t = t_list.pop()
            t.join()

        return self.page_map