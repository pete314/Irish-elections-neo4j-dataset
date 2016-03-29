# Irish Constituencies Neo4j Database
###### Student name, G00123456

## Introduction
The project has 3 parts:
*Retreive data from internet about Irish Voting result focusing on Constituency, Candidates, Political Parties
*Strucutre the data and create apropiate nodes and relations in Neo4j
*Create queries fro retreiving interesting data about results

This project is focusing on Candidates and Constituency and retreives election results from these two entry points. Candidate information is not limited to Irish elections.


## Database
After looking at the election results and the data associated with it I realized that I could write a handy crawler with a specific scraper for the purpose. The scraper is designed to extract data from [electionsireland.org/](http://electionsireland.org/).
The crawler is written in python, which has 3 parts(kept in ./supports):
*Downloader & LinkCrawler: Simple crwaler with capability to identify errors and retry if any. Written with "ethical crawling" in mind, so if robots.txt block the crawler, no result is returned. LinkCrwaler keep track of visited pages in it own thread, so if multi threaded duplicates may exist.
*Scraper: Is a class written to be used within LinkCrawler, can be fully customized to support any page layout/dom, uses sax equalent lxml to deal with html tree, mostly with xpath.
*Neo4j wrapper: deals with dabatase communication. Really simple straigth forward class connected with scraper. 
There are couple support classes, python files not worth meantioning in depth.

¬¬¬
IF YOU RUN THE CRAWLER MAKE SURE THAT YOU UNDERSTAND WHAT THE DEPTH FACTOR IS, EVEN WITH DEPTH=4 IT IS POSSIBLE TO SCRAPE 10 000+ pAGES!

Notes:
The neo4j instanc does not use username and password as there is no need for it on local only setup.
Currently there are 22000+ nodes in the database with 5 different node structure and with 60000+ relationships in 3 relation types.
¬¬¬


## Queries
Then explain them one by one in the following sections.

#### Query one title
Find candidates and political who got more than 10000 votes
```cypher
MATCH 
	(ph:PersonHistory)-[r:RUN_FOR]->(p:Party)
WHERE
	length(ph.votes) > 5
RETURN r
```

#### Query two title
This query retreives the Bacon number of an actor...
```cypher
MATCH
	(Bacon)
RETURN
	Bacon;
```

#### Query three title
This query retreives the Bacon number of an actor...
```cypher
MATCH
	(Bacon)
RETURN
	Bacon;
```

## References
1. [Neo4J website](http://neo4j.com/), the website of the Neo4j database.
2. [Python 2 documentation](https://docs.python.org/2/), the offical python v2.* documentation.
3. [electionsireland.org/](http://electionsireland.org/), data for crawling.
