#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Peter Nagy
Since: 03 2016
Project: python
Description: Manual scraper test
"""
import os
from scrape.factory.ElectionsIrelandScraper import ElectionsIrelandScraper

"""THIS HAS TO BE DELETED JUST FOR TESTING"""
def load_file_content(file_name):
    base_path = os.path.dirname(__file__)
    file_path = os.path.abspath(os.path.join(base_path, "..", "..", "scraped_data", file_name))
    print file_path
    with open(file_path, 'r+') as file_pointer:
        return file_pointer.read()

    return None


if __name__ == "__main__":
    file_name = "http-__electionsireland.org_result.cfmQMelection=2016&cons=204.html"
    file_name_candidate_page = "http-__electionsireland.org_candidate.cfmQMID=3189.html"
    html = load_file_content(file_name_candidate_page)
    eis = ElectionsIrelandScraper(html)
    result = eis.check_content_page(file_name_candidate_page)