#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Peter Nagy
Since: Jan 2016
Description: Downloader Unit Test
Source: Peter Nagy (myself :) ) https://github.com/pete314/cap-crawler/
"""

from scrape.factory.Downloader import Downloader
import unittest

TEST_SITE_URL_200 = 'https://crosssec.com'
TEST_SITE_URL_401 = 'https://web.crosssec.com/login'
TEST_HEADER = {'User-agent': "Mozilla/5.0 (compatible; https://peternagy.ie/)"}

class TestDownloader(unittest.TestCase):
    """
    Test downloader returns correct status
    """
    def init_downloader_result(self, url):
        return Downloader().download(url, TEST_HEADER, 2)

    def test_success_response(self):
        result = self.init_downloader_result(TEST_SITE_URL_200)
        self.assertEqual(result['code'], 200)

    def test_success_response_401(self):
        result = self.init_downloader_result(TEST_SITE_URL_401)
        self.assertEqual(result['code'], 401)

    def test_success_content_scrapping(self):
        result = self.init_downloader_result(TEST_SITE_URL_200)
        self.assertNotEqual(len(result['html']), 0)

if __name__ == '__main__':
    unittest.main()