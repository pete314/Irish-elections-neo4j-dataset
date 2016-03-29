#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Peter Nagy
Since: March 2016
Description: Web page entity class, easing the data handling
"""

class PageEntity(object):
    def __init__(self, url, content=None):
        """
        Initialization of the class should happen after new link is crawled
        :param url:
        :param content:
        :return:
        """
        self.url = url
        self.content = content

    def __cmp__(self, other):
        """
        Simple comparison based on url, comes handy as this will be in queue/dict
        :param other: PageEntity to compare to
        :return: bool
        """
        return cmp(self.url, other.url)

    def set_content(self, content):
        self.content = content

    def get_content(self):
        return self.content

    def get_url(self):
        return self.url
