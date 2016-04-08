# Irish Constituencies Neo4j Database
###### Peter Nagy, G00317399

## Introduction

## Implementation
The project has the following parts:<br/>
1. Retreive data from internet about Irish Voting result focusing on Constituency, Candidates, Political Parties<br/>
2. Strucutre the data and create apropiate nodes and relations in Neo4j<br/>
3. Create queries fro retreiving interesting data about results<br/>

This project is focusing on Candidates and Constituency and retreives election results from these two entry points. Candidate information is not limited to Irish elections.

Backups can be found in supports folder along with the setup script. Please use the larges backup nuber in order to setup the lates dataset. Current highest is *_003.cypher

## Database
The project is based on a [Neo4J](http://neo4j.com/) which is a graph database. One of the greatest advantage for using graph database against a relational database like MySql is that the data does not need a strictly specified schema, which implies that some nodes (records in sql), can have different properties than others. There is no need for any sort of alteration if the data is not in the same structure. Also there are no joins as such, but still relationships can be created between nodes, which acts like view in sql terms. For more comparison visit [Neo4j's From SQL to Cypher](http://neo4j.com/developer/guide-sql-to-cypher/)
I personally was a big fan of relational databases(Certified oracle Database dev & admin), but I moved my focus couple years ago to NoSql. The comparison for NoSql is really interesting as well, which is [available here](http://neo4j.com/developer/graph-db-vs-nosql/).

#####Installation guide
Installation of this repositories database can be done by following steps:

 1. Get latest Java Jre from [Java.com](https://java.com/en/download/)<br>
 2. Get lates [Neo4J community edition](http://neo4j.com/download/) (free) <br>
 3. Install both of the above software in the order they are present.
 4. After installation finished, double click Neo4J icon, but don't start the database itself.
 5. Select options in the Neo4j window
 6. Under "Database tuning" click the edit button and remove the # symbol from the line "allow_store_upgrade=true". This will make the dataset backwards compatible.
 7.  Under "Server configuration" click the edit button and set "dbms.security.auth_enabled=false", this will allow you to connect to the database without password. **This should be only done in local setup, as everyone will be able to connect without username and password**
 8. Close the options windows and select Choose under Database location, where you should select "path/to/local/downloaded/repository/constituencies.graphdb"
 9. Start the database server in the main window.

**More information about setting up a Neo4j database is available here** 

##Usage of crawler
After looking at the election results and the data associated with it I realized that I could write a handy crawler with a specific scraper for the purpose. The scraper is designed to extract data from [electionsireland.org/](http://electionsireland.org/).
The crawler is written in python, which has 3 parts(kept in ./supports):<br/>
**Downloader & LinkCrawler**: Simple crwaler with capability to identify errors and retry if any. Written with "ethical crawling" in mind, so if robots.txt block the crawler, no result is returned. LinkCrwaler keep track of visited pages in it own thread, so if multi threaded duplicates may exist.<br/>
**Scraper**: Is a class written to be used within LinkCrawler, can be fully customized to support any page layout/dom, uses sax equalent lxml to deal with html tree, mostly with xpath.<br/>
**Neo4j wrapper**: deals with dabatase communication. Really simple straigth forward class connected with scraper. 
There are couple support classes, python files not worth meantioning in depth.

The script is only handling data collection, and all additional relations are added after script finishes. This is requred as there could be millions of realtions even between 1000's of nodes. The scripts to create realations can be found in the support folder.

```
IF YOU RUN THE CRAWLER MAKE SURE THAT YOU UNDERSTAND WHAT THE DEPTH FACTOR IS, EVEN WITH DEPTH=4 IT IS POSSIBLE TO SCRAPE 10 000+ PAGES!

Notes:
The neo4j instanc does not use username and password as there is no need for it on local only setup.
Currently there are 22000+ nodes in the database with 5 different node structure and with 60000+ relationships in 3 relation types.
```

#####Setting up/working with the script

 1. Download python 2.7 & and pip
 2. Install both
 3. Get few dependacies with pip install BeautifulSoup, lxml, ba2, urllib2
 4. Open the repository code base from /path/to/donwload/repository/support/python
 5. Execution can be done by ./scrape/scrape_runner.py

## Queries
Duplicates cmay exist so query results can be wrong for this reason, also data may be inconsistent. There are no gurantees that the source had the rigth data nor that the crawler picked up all.

#### Find candidates with filters
Find candidates who got elected for each political party. The query will match the relations between Political parties and PersonHistory and then apply filers for status and election date.
```cypher
MATCH 
	(ph:PersonHistory)-[r:RUN_FOR]->(p:Party)
WHERE
	ph.date = "2016"
AND
	ph.status = "Elected"
RETURN distinct r
```

#### Dynamic node matching
Find people who run in the same election as Enda Kenny
and  got more than 10000 votes.
```cypher
MATCH (n),(m)
WHERE 
	has(n.name)
AND
	n.name = "Enda Kenny"
AND
    m.election_date = n.election_date
AND
    length(m.proof_vote) > 4
return distinct m.name, m.area, m.election_date
order by
	m.election_date desc, 
	m.area
```

#### Find shorets path between nodes
Find the sortest path between two Candidates
```cypher
MATCH p=shortestPath(
  (c1:ConstituencyCandidate {name:"Jim Tallon"})-[*]-(c2:ConstituencyCandidate {name:"Charlie Keddy"})
)
RETURN p
```

## References
1. [Neo4J website](http://neo4j.com/), the website of the Neo4j database.
2. [Neo4j's From SQL to Cypher](http://neo4j.com/developer/guide-sql-to-cypher/)
3. [Neo4J's NoSql comparison](http://neo4j.com/developer/graph-db-vs-nosql/).
2. [Python 2 documentation](https://docs.python.org/2/), the offical python v2.* documentation.
3. [electionsireland.org/](http://electionsireland.org/), data for crawling.
4. [Java.com](https://java.com/en/download/)
