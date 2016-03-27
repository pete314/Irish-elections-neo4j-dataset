#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Peter Nagy
Since: 03 2016
Project:
Description: This is a custom content scraper for ElectionsIreland.org
"""
from BeautifulSoup import BeautifulSoup
from lxml import html

class ElectionsIrelandScraper(object):
    def __init__(self, html_content):
        self.html_content = html_content

    def check_content_page(self):
        soup = BeautifulSoup(self.html_content)
        element = soup.find("span", {"class": "title3"})
        self.election = element.next
        if "General Election" in self.election:
            self.parse_consent_details()

    def parse_consent_details(self):
        html_tree = html.fromstring(self.html_content)

        # Get county and town
        voting_town = html_tree.xpath("//span[contains(@class, 'title3') and em]")
        voting_county = html_tree.xpath("//span[contains(@class, 'title3') and em]/em")
        print voting_town[0].text
        print voting_county[0].text

        # Get
        voters_info_table = html_tree.xpath("//table[contains(@class, 'consdetail')]")
        for table in voters_info_table:
            td_list = table.xpath(".//tr/td")
            for td in td_list:
                print td.text
        #print seat_count[0].text
