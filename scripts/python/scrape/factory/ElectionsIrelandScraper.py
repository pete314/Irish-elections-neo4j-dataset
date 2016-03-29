#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Peter Nagy
Since: 03 2016
Description: This is a custom content scraper for ElectionsIreland.org
Notes: This class is a disaster(complexity, readability, not reusable),
        @todo: should be refactored if used in production
"""
from store.neo4j.Neo4jWrapper import Neo4jWrapper
from BeautifulSoup import BeautifulSoup
from lxml import html
import hashlib
import uuid
import random

class ElectionsIrelandScraper(object):
    def __init__(self, html_content):
        self.html_content = html_content
        self.area_data = {
            "uuid": None,
            "election_date": None,
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

    def check_content_page(self, link):
        if "candidate" in link:
            # THIS IS A CANDIDTE PAGE SCRAPE
            return self.scrape_candidate_page()

        elif "election" or "general" in link:
            # THIS IS AN ELECTION PAGE SCRAPE
            return self.scrape_election_const_result_page()

        elif "party" in link:
            # THIS IS A PARTY PAGE SCRAPE
            return self.scrape_party_page()

    def scrape_party_page(self):
        """
        Sample page: http://electionsireland.org/party.cfm?election=2016&party=FF
        :return:
        """
        html_tree = html.fromstring(self.html_content)
        page_title_holder = html_tree.xpath("/html/body/table[2]/tr/td/h1/text()")

        if len(page_title_holder) > 0:
            page_title = self.extract_list_string(page_title_holder, {"\n", "\t"})
            if page_title is not None and "Candidates by Party" in page_title:
                party_data_list = self.extract_party_page(html_tree)
                if len(party_data_list) > 0:
                    return self.create_party_candidates(party_data_list)

        return False

    def create_party_candidates(self, party_data_list):
        """
        Create nodes in neo4j
        :param party_data_list: List holding dict's of data created in the below function
        :return:
        """
        create_party_candidate_statement = "create (pc:PartyCandidates {id:{id}, constituency:{constituency}, party:{party}," \
                                          " candidate:{candidate}, date:{date}})"
        db = Neo4jWrapper("", "")
        return db.insert_multiple_nodes(create_party_candidate_statement, party_data_list)

    def extract_party_page(self, html_tree):
        """ Extract the data from the party pages
        :param html_tree:
        :return:
        """
        party_data_list = list()
        result_date = self.extract_list_string(html_tree.xpath("/html/body/table[2]/tr/td/h2/em/text()"), {"\n", "\t"})
        if result_date is not None:
            data_table = html_tree.xpath("/html/body/table[4]/tbody/tr/td/table[2]/tr")
            for row in data_table:
                candidate_party = {'date': result_date}
                modifier = ""
                const_holder = row.xpath(".//td[1]/a/text()")
                if len(const_holder) == 0:
                    modifier = "/strong"
                    const_holder = row.xpath(".//td[1]/a" + modifier + "/text()")

                candidate_party['constituency'] = self.extract_list_string(const_holder, {"\n", "\r"})
                candidate_party['party'] = self.extract_list_string(row.xpath(".///td[2]/img/@title"), {"\n", "\t", "Non party/"})
                candidate_party['candidate'] = self.extract_list_string(row.xpath(".//td[3]/a" + modifier + "/text()"), {"\n", "\t"})
                candidate_party['id'] = hashlib.md5(str(random.randint(256, 9999999)) + uuid.uuid4().hex).hexdigest()

                party_data_list.append(candidate_party)

        return party_data_list

    def scrape_candidate_page(self):
        """
        Sample page: http://electionsireland.org/candidate.cfm?ID=900
        :return:
        """
        html_tree = html.fromstring(self.html_content)
        candidant_holder = html_tree.xpath("/html/body/table[3]/tr/td[2]/h1/text()")

        if len(candidant_holder) > 0:
            candidate_name = self.extract_list_string(candidant_holder, {"\n", "\t"})
            candidate_history_list = self.extract_candidate_history(html_tree)
            if len(candidate_history_list) > 0:
                return self.create_candidate_history_nodes(candidate_name, candidate_history_list)

        return False

    def create_candidate_history_nodes(self, candidate, history_data_list):
        """
        Create nodes from candidate data
        :param candidate:
        :param hostyory_data_list:
        :return:
        """
        p_uuid = hashlib.md5(str(random.randint(256, 9999999)) + uuid.uuid4().hex).hexdigest()
        create_person_node = "Create (p:Person {id:{uuid}, Name:{Name}})"
        person_dict = {'uuid': p_uuid, 'Name': candidate}

        create_person_history_node = "Create (ph:PersonHistory {id:{id}, election:{election}, date:{date}, party:{party}," \
                                     " status:{status}, constituency:{constituency}, seat:{seat}, votes:{votes}, share:{share}," \
                                     " quota:{quota}, person:'" + candidate + "'}) "
                                     # "create (p:Person {id:'"+p_uuid+"'})-[:RUN_FOR]->ph"
        db = Neo4jWrapper("", "")
        db.insert_single_node(create_person_node, person_dict)
        return db.insert_multiple_nodes(create_person_history_node, history_data_list)

    def extract_candidate_history(self, html_tree):
        """ Ecract the candidate data from page
        """
        history_table = html_tree.xpath("//html/body/table[8]/tr")
        candidate_history_list = list()
        for row in history_table:
            history_data = dict()
            date_holder = row.xpath("./td[1]/b/text()")
            if len(date_holder) == 0:
                continue

            history_data['date'] = self.extract_list_string(date_holder, {"\n", "\t", "By Election:"})
            history_data['election'] = self.extract_list_string(row.xpath("./td[3]/b/text()"), {"\n", "\t"})
            history_data['party'] = self.extract_list_string(row.xpath("./td[5]/a/img/@title"), {"\n", "\t", "Non party/"})
            history_data['status'] = self.extract_list_string(row.xpath("./td[7]/b/text()"), {"\n", "\t"})
            history_data['constituency'] = self.extract_list_string(row.xpath("./td[9]/b/a/text()"), {"\n", "\t"})
            history_data['seat'] = self.extract_list_string(row.xpath("./td[11]/b/text()"), {"\n", "\t"})
            history_data['count'] = self.extract_list_string(row.xpath("./td[13]/b/text()"), {"\n", "\t"})
            history_data['votes'] = self.extract_list_string(row.xpath("./td[15]/b/text()"), {"\n", "\t", ","})
            history_data['share'] = self.extract_list_string(row.xpath("./td[17]/b/text()"), {"\n", "\t", "%"})
            history_data['quota'] = self.extract_list_string(row.xpath("./td[19]/b/text()"), {"\n", "\t"})
            history_data['id'] = hashlib.md5(str(random.randint(256, 9999999)) + uuid.uuid4().hex).hexdigest()

            candidate_history_list.append(history_data)

        return candidate_history_list

    def extract_list_string(self, lst, replace_set=set()):
        if len(lst) > 0:
            return str_replace_items(lst[0], replace_set).strip()
        else:
            return None

    def scrape_election_const_result_page(self):
        """ Page sample: http://electionsireland.org/result.cfm?election=2016&cons=32
        :return:
        """
        soup = BeautifulSoup(self.html_content)
        element = soup.find("span", {"class": "title3"})
        if element is None:
            return False

        self.election = element.next
        self.area_data['uuid'] = uuid.uuid4().hex
        self.area_data['election_date'] = self.election.replace("General Election: ", "").strip()
        self.parse_consent_details()
        self.parse_total_voters()
        if len(self.candidate_data_list) > 0:
            self.create_neo_nodes_election()
            return True

        return False

    def create_neo_nodes_election(self):
        """ Simple node creation
        :return:
        """
        election_area_create_statement = "CREATE (const:Constituency {id:{uuid}, name:{voters_area}, county:{voters_county}," \
                                  " date:{election_date}, seats:{seats}, candidates:{candidates}, counts:{counts}," \
                                  " electorate:{electorate}, quota:{quota}, total_valid:{total_valid}," \
                                  " total_valid_percent:{total_valid_percent}, spoilt_votes:{spoilt_votes}," \
                                  " total_poll:{total_poll}, total_poll_percent:{total_poll_percent}})"

        area_candidate_create_statement = "CREATE (candid:ConstituencyCandidate {id:{uuid}, area:{voters_area}," \
                                          " election_date:{election_date}, name:{name}, party:{party}, proof_vote:{proof_vote}," \
                                          " share_vote:{share_vote}, quota:{quota}, count:{count}, status:{status}, seat:{seat}}) "
                                          # "create (const:Constituency {id:'"+self.area_data['uuid']+"'})-[:RUN_FOR]->candid"


        db = Neo4jWrapper("", "")
        db.insert_single_node(election_area_create_statement, self.area_data)
        db.insert_multiple_nodes(area_candidate_create_statement, self.candidate_data_list)

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
                if str_holder is None:
                    continue

                if "Seats" in str_holder:
                    self.area_data['seats'] = str_replace_items(str_holder, {"Seats"})
                elif "Candidates" in str_holder:
                    self.area_data['candidates'] = str_replace_items(str_holder, {"Candidates"})
                elif "Counts" in str_holder:
                    self.area_data['counts'] = str_replace_items(str_holder, {"Counts"})
                elif "Electorate" in str_holder:
                    self.area_data['electorate'] = str_replace_items(str_holder, {"Electorate:", ","})
                elif "Quota" in str_holder:
                    self.area_data['quota'] = str_replace_items(str_holder, {"Quota:", ","})


    def parse_total_voters(self):
        """Parse the area results"""

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

                candidate_data['voters_area'] = self.area_data['voters_area']
                candidate_data['election_date'] = self.area_data['election_date']
                candidate_data['uuid'] = hashlib.md5(str(random.randint(256, 9999999)) + uuid.uuid4().hex).hexdigest()
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


def str_extract_from_list(emt_list):
    for element in emt_list:
        if len(element) > 0 and element is not None:
            return element

    return None



def str_replace_items(str_base, items=set(), replace_with=""):
    """Simple recursive replace for multiple elements to replace"""
    if str_base is None:
        return None

    for item in items:
        str_base = str_base.replace(item, replace_with)
    return str_base

