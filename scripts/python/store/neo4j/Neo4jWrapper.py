#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Peter Nagy
Since: 2016-02-22
Description: Wrapper for Neo4j functions
Source: https://github.com/pete314/neo4j_adventures/blob/master/basics/Neo4jWrapper.py
"""

from py2neo import Graph
from py2neo import neo4j
import sys

class Neo4jWrapper(object):

    def __init__(self, user_name, password, connection_string="", current_id=1):
        self.connection_string = connection_string \
                    if connection_string != "" \
                    else "http://"+ user_name+":"+password+"@localhost:7474/db/data/"
        self.graph_db = Graph(self.connection_string)
        self.current_id = current_id

    def delete_all_nodes(self):
        self.graph_db.delete_all()

    def insert_single_node(self, cypher_statement, params_dict):
        """
        Insert a single node into database
        :param cypher_statement: the statement to execute
        :param params_dict: the values for the statment
        :return: inserted records
        """
        batch = neo4j.WriteBatch(self.graph_db)
        batch.append(neo4j.CypherJob(cypher_statement, params_dict))
        return batch.submit()


    def insert_multiple_nodes(self, cypher_statement, params_dict_list):
        """
        Execute multiple inserts
        :param cypher_statement:
        :param params_dict_list: list of dict to insert
        :return: inserted records
        """
        batch = neo4j.WriteBatch(self.graph_db)
        for params_dict in params_dict_list:
            batch.append(neo4j.CypherJob(cypher_statement, params_dict))
        return batch.submit()

    def isrt_multiple_nodes_with_realtion(self, cypher_statement, params_dict_list, relation_statement):
        """
        The relation script will match current insert an connect to the static node given in statement
        :param cypher_statement:
        :param params_dict_list: list of dict to insert
        :param relation_statement:
        :return:
        """
        batch = neo4j.WriteBatch(self.graph_db)
        for params_dict in params_dict_list:
            batch.append(neo4j.CypherJob(cypher_statement, params_dict))
        return batch.submit()
