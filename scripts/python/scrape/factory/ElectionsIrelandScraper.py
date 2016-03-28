#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Peter Nagy
Since: 03 2016
Description: This is a custom content scraper for ElectionsIreland.org
"""
from BeautifulSoup import BeautifulSoup
from lxml import html
import string

class ElectionsIrelandScraper(object):
    def __init__(self, html_content):
        self.html_content = html_content
        self.area_data = {
            "voters_area": None,
            "voters_county": None,
            "seats": None,
            "candidates": None,
            "counts": None,
            "electorate": None,
            "quota": None,
            "total_valid": None,
            "total_valid_percent": None,
            "spoilt_votes": None,
            "spoilt_votes_percent": None,
            "total_poll": None,
            "total_poll_percent": None
        }

    def check_content_page(self):
        soup = BeautifulSoup(self.html_content)
        element = soup.find("span", {"class": "title3"})
        self.election = element.next
        if "General Election" in self.election:
            self.parse_consent_details()
            self.parse_total_voters()

    def parse_consent_details(self):
        """ Parse consent details """
        html_tree = html.fromstring(self.html_content)

        # Get county and town
        voting_town_elements = html_tree.xpath("//span[contains(@class, 'title3') and em]")
        for town_element in voting_town_elements:
            voting_county = town_element.xpath(".//em")
            self.area_data['voters_area'] = str_replace_items(town_element.text, {"\n"}).strip()
            self.area_data['voters_county'] = str_replace_items(voting_county[0].text, {"(", ")", " "})

        # Get constitution details
        voters_info_table = html_tree.xpath("//table[contains(@class, 'consdetail')]")
        for table in voters_info_table:
            td_list = table.xpath(".//tr/td")
            for td in td_list:
                str_holder = str_replace_items(td.text,  {"\n", "\r", "\t", " ", ","})
                if "Seats" in str_holder:
                    self.area_data['seats'] = int(str_replace_items(str_holder, {"Seats"}))
                elif "Candidates" in str_holder:
                    self.area_data['candidates'] = int(str_replace_items(str_holder, {"Candidates"}))
                elif "Counts" in str_holder:
                    self.area_data['counts'] = int(str_replace_items(str_holder, {"Counts"}))
                elif "Electorate" in str_holder:
                    self.area_data['electorate'] = int(str_replace_items(str_holder, {"Electorate:"}))
                elif "Quota" in str_holder:
                    self.area_data['quota'] = int(str_replace_items(str_holder, {"Quota:"}))

        """
        for data in self.area_data.itervalues():
            print data
        """

    def parse_total_voters(self):
        """Parse the area results"""
        candidate_data = {
            "name": None,
            "party": None,
            "proof_vote": None,
            "share_vote": None,
            "quota": None,
            "count": 0,
            "status": None,
            "seat": 0
        }

        self.candidate_data_list = list()

        html_tree = html.fromstring(self.html_content)
        result_table = html_tree.xpath("//table[@class='rtable']")

        for r_table in result_table:
            """
            Note: /b is the elected fellow
            candidate(str) .//a[contains (@href, 'candidate')]
            party(str) .//a/img/@title
            1st_pref_vote(0,0)  .//td[6]/b
            share_vote(%) .//td[8]/b
            quota(0,0): .//td[10]/b
            count(0):   .//td[12]
            status: .//td[14]/strong
            seat: .//td[16]/strong
            """
            candidates = r_table.xpath(".//tr")
            for candiate in candidates:
                modifier = "b/"
                """ Candidate """
                selected_candidate = candiate.xpath(".//"+modifier+"a[contains (@href, 'candidate')]/text()")
                if len(selected_candidate) == 0:
                    selected_candidate = candiate.xpath(".//a[contains (@href, 'candidate')]/text()")
                    modifier = ""

                if len(selected_candidate) > 0:
                    if selected_candidate is not None:
                        candidate_data['name'] = selected_candidate[0].strip()
                else:
                    ## THIS IS NOT A VALID CANDIDATE
                    continue
                """ Party"""
                party = candiate.xpath(".//a/img/@title")
                if len(party) > 0:
                    candidate_data['party'] = str_replace_items(party[0], {"Non party/"}).strip()

                """ 1st proof votes """
                st_proof_votes = candiate.xpath(".//td[6]/" + modifier + "text()")
                if len(st_proof_votes) > 0:
                    candidate_data['proof_vote'] = str_replace_items(st_proof_votes[0], {","}).strip()

                """ Shared votes """
                st_shared_votes = candiate.xpath(".//td[8]/" + modifier + "text()")
                if len(st_shared_votes) > 0:
                    candidate_data['share_vote'] = str_replace_items(st_shared_votes[0], {"%"}).strip()

                """ Quota """
                st_quota = candiate.xpath(".//td[10]/" + modifier + "text()")
                if len(st_quota) > 0:
                    candidate_data['quota'] = st_quota[0].strip()

                """ Count """
                st_count = candiate.xpath(".//td[12]/" + modifier + "text()")
                if len(st_count) > 0:
                    candidate_data['count'] = str_replace_items(st_count[0], {"(", ")"}).strip()

                """ Status """
                st_status = candiate.xpath(".//td[14]/" + modifier + "text()")
                if len(st_status) > 0:
                    candidate_data['status'] = st_status[0].strip()

                """ Seat """
                st_seat = candiate.xpath(".//td[16]/" + modifier + "text()")
                if len(st_seat) > 0:
                    candidate_data['seat'] = st_seat[0].strip()

                ## ADD TO THE CANDIDATE DATA LIST
                self.candidate_data_list.append(candidate_data)

            """ PARSE the total counts """
            total_votes = r_table.xpath(".//tr[23]/td[5]/b/text()")
            if len(total_votes) > 0:
                self.area_data['total_valid'] = int(str_replace_items(total_votes[0], {","}).strip())
            total_votes_percent = r_table.xpath(".//tr[23]/td[5]/b/text()")
            if len(total_votes_percent) > 0:
                self.area_data['total_valid_percent'] = str_replace_items(total_votes_percent[0], {"%"}).strip()

            """ PARSE spoilt votes """
            total_spoilt = r_table.xpath(".//tr[25]/td[5]/b/text()")
            if len(total_spoilt) > 0:
                self.area_data['spoilt_votes'] = int(str_replace_items(total_spoilt[0], {","}).strip())
            total_spoilt_percent = r_table.xpath(".//tr[25]/td[5]/b/text()")
            if len(total_spoilt_percent) > 0:
                self.area_data['spoilt_votes_percent'] = str_replace_items(total_spoilt_percent[0], {"%"}).strip()

            """ PARSE Total poll """
            total_poll = r_table.xpath(".//tr[27]/td[5]/b/text()")
            if len(total_poll) > 0:
                self.area_data['total_poll'] = int(str_replace_items(total_poll[0], {","}).strip())
            total_poll_percent = r_table.xpath(".//tr[27]/td[5]/b/text()")
            if len(total_poll_percent) > 0:
                self.area_data['total_poll_percent'] = str_replace_items(total_poll_percent[0], {"%"}).strip()

            for data in self.area_data.itervalues():
                print data

            """
            for cd in candidate_data_list:
                print "------------- candidate\n"
                for data in cd.itervalues():
                    print data
            """

def str_extract_from_list(emt_list):
    for element in emt_list:
        element = element
        if len(element) > 0 and element is not None:
            return element



def str_replace_items(str_base, items=set(), replace_with=""):
    """Simple recursive replace for multiple elements to replace"""
    for item in items:
        str_base = str_base.replace(item, replace_with)
    return str_base
