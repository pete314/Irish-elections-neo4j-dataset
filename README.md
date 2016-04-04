# Irish Constituencies Neo4j Database
###### Peter Nagy, G00317399

## Introduction
The project has the following parts:<br/>
1. Retreive data from internet about Irish Voting result focusing on Constituency, Candidates, Political Parties<br/>
2. Strucutre the data and create apropiate nodes and relations in Neo4j<br/>
3. Create queries fro retreiving interesting data about results<br/>

This project is focusing on Candidates and Constituency and retreives election results from these two entry points. Candidate information is not limited to Irish elections.

Backups can be found in supports folder along with the setup script. Please use the larges backup nuber in order to setup the lates dataset. Current highest is *_003.cypher

## Database
After looking at the election results and the data associated with it I realized that I could write a handy crawler with a specific scraper for the purpose. The scraper is designed to extract data from [electionsireland.org/](http://electionsireland.org/).
The crawler is written in python, which has 3 parts(kept in ./supports):<br/>
**Downloader & LinkCrawler**: Simple crwaler with capability to identify errors and retry if any. Written with "ethical crawling" in mind, so if robots.txt block the crawler, no result is returned. LinkCrwaler keep track of visited pages in it own thread, so if multi threaded duplicates may exist.<br/>
**Scraper**: Is a class written to be used within LinkCrawler, can be fully customized to support any page layout/dom, uses sax equalent lxml to deal with html tree, mostly with xpath.<br/>
**Neo4j wrapper**: deals with dabatase communication. Really simple straigth forward class connected with scraper. 
There are couple support classes, python files not worth meantioning in depth.

The script is only handling data collection, and all additional relations are added after script finishes. This is requred as there could be millions of realtions even between 1000's of nodes. The scripts to create realations can be found in the support folder.

```
IF YOU RUN THE CRAWLER MAKE SURE THAT YOU UNDERSTAND WHAT THE DEPTH FACTOR IS, EVEN WITH DEPTH=4 IT IS POSSIBLE TO SCRAPE 10 000+ pAGES!

Notes:
The neo4j instanc does not use username and password as there is no need for it on local only setup.
Currently there are 22000+ nodes in the database with 5 different node structure and with 60000+ relationships in 3 relation types.
```


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
2. [Python 2 documentation](https://docs.python.org/2/), the offical python v2.* documentation.
3. [electionsireland.org/](http://electionsireland.org/), data for crawling.
