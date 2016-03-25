#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Peter Nagy
Since: Jan 2016
Description: Downloader Unit Test
Notes: I wrote this code for another project, https://github.com/pete314/cap-crawler/
"""

from scrape.factory.Downloader import Downloader
import unittest

TEST_SITE_URL_200 = 'https://crosssec.com'
TEST_SITE_URL_401 = 'https://web.crosssec.com/login'
TEST_HEADER = {'User-agent': "GMIT-Research"}

class TestDownloader(unittest.TestCase):
    """
    Test downloader returns correct status
    """
    def test_success_response(self):
        result = Downloader().download(TEST_SITE_URL_200, TEST_HEADER, 2)
        self.assertEqual(result['code'], 200)


if __name__ == '__main__':
    unittest.main()