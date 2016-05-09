# Irish Constituencies Neo4j Database

## Introduction
In 2016 there was a general election in the Republic of Ireland.
The country is divided into constituencies, with a number of seats available in each.
A large number of candidates ran in each constituency.

This project is inspired by the well known FiveThirtyEight blog by Nate Silver:

>*Nate Silver has become today's leading statistician through his innovative analyses of political polling. He first gained national attention during the 2008 presidential election, when he correctly predicted the results of the primaries and the presidential winner in 49 states. In 2012, he called 50 of 50 states.*

> **leighbureaultd.com**

![Nate Silver's prediction](https://raw.githubusercontent.com/pete314/Irish-elections-neo4j-dataset/master/md_img/nate.png)

#####Irish constituencies
![Irish constituencies - map](https://raw.githubusercontent.com/pete314/Irish-elections-neo4j-dataset/master/md_img/irish_const_map_2011-2016.png)
Background of these constituencies with more details can be found [Parliamentary constituencies in the Republic of Ireland - wikipedia](https://en.wikipedia.org/wiki/Parliamentary_constituencies_in_the_Republic_of_Ireland)
## Implementation
The project has the following parts:<br/>
1. Retreive data from internet about Irish Voting result focusing on Constituency, Candidates, Political Parties<br/>
2. Strucutre the data and create apropiate nodes and relations in Neo4j<br/>
3. Create queries for retrieving interesting data about results<br/>

This project is focusing on Candidates and Constituency and ruses election results from these two entry points. Candidate information is not limited to Irish elections.

Backups can be found in supports folder along with the setup script. Please use the larges backup nuber in order to setup the lates dataset. Current highest is *_003.cypher

> The data may contain duplicates and so does the relations, which is not a problem for this project as it can be filtered down with node search.

## Database
The project is based on a [Neo4J](http://neo4j.com/) which is a graph database. One of the greatest advantage for using graph database against a relational database like MySql is that the data does not need a strictly specified schema, which implies that some nodes (records in sql), can have different properties than others. There is no need for any sort of alteration if the data is not in the same structure. Also there are no joins as such, but still relationships can be created between nodes, which acts like view in sql terms. For more comparison visit [Neo4j's From SQL to Cypher](http://neo4j.com/developer/guide-sql-to-cypher/)
I personally was a big fan of relational databases(as I am Certified Oracle Database dev & admin), but I moved my focus couple years ago to NoSql. The comparison for NoSql is really interesting as well, which is [available here](http://neo4j.com/developer/graph-db-vs-nosql/).

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

**More information about setting up a Neo4j database is available on [Neo4j Documentation page](http://neo4j.com/docs/stable/server-installation.html)** 

##Usage of crawler
After looking at the election results and the data associated with it I realized that I could write a handy crawler with a specific scraper for the purpose. The scraper is designed to extract data from [electionsireland.org/](http://electionsireland.org/).
The crawler is written in python, which has 3 parts(kept in ./supports):<br/>
**Downloader & LinkCrawler**: Simple crawler with capability to identify errors and retry if any. Written with "ethical crawling" in mind, so if "robots.txt" blocks the crawler, no result is returned. LinkCrawaler keeps track of visited pages in it own thread, so if multi threaded duplicates may exist.<br/>
**Scraper**: Is a class written to be used within LinkCrawler, can be fully customized to support any page layout/dom, uses [SAX](https://en.wikipedia.org/wiki/Simple_API_for_XML) equivalent [lxml](http://lxml.de/) used to deal with html tree and quick extraction, mostly with [xPath](https://en.wikipedia.org/wiki/XPath).<br/>
**Neo4j wrapper**: deals with dabatase communication. Really simple straigth forward class connected with scraper. 
There are couple support classes, python files not worth meantioning in depth.

The script is only handling data collection, and all additional relations are added after script finishes. This is requred as there could be millions of realtions even between 1000's of nodes. The scripts to create realations can be found in the support folder.


> IF YOU RUN THE CRAWLER MAKE SURE THAT YOU UNDERSTAND WHAT THE DEPTH FACTOR IS, EVEN WITH DEPTH=4 IT IS POSSIBLE TO SCRAPE 10 000+ PAGES!

Notes:
>The neo4j instance does not use username and password as there is no need for it on local only setup.
>Currently there is 22000+ nodes in the database with 5 different node types and with 60000+ relationships in 3 relation types.



#####Setting up/working with the script

 1. Download python 2.7 & and pip
 2. Install both
 3. Get few dependacies with pip install BeautifulSoup, lxml, ba2, urllib2
 4. Open the repository code base from "/path/to/donwload/repository/support/python"
 5. Execution can be done by "./scrape/scrape_runner.py"

## Queries
Duplicates may exist so query results can be different from actual facts for this reason, also data may be inconsistent. There are no grantees that the source had the right data nor that the crawler picked up all.
The queries are focusing on graph based functionality, as filtering, on it's own (having, where, union, optional match[aka. join] etc.) can be done much faster in NoSql or even Sql (with the right setup). Also focusing on generalized matching without structure, which can hardly be done in the previously mentioned database types.

####Node types
```cypher
(PartyCandidates {id:'STRING_HASH', constituency:'STRING', party:'STRING', candidate:'STRING', date:'STRING'})

(Person {id:'STRING_HASH', Name:'STRING'})

(PersonHistory {id:'STRING_HASH', election:'STRING', date:'STRING', party:'STRING', status:'STRING', constituency:'STRING', seat:'INT', votes:'INT/STRING', share:'FLOAT', quota:'STRING', person:'STRING'})

(Constituency {id, name:'STRING', county:'STRING', date:'STRING', seats:'STRING', candidates:'STRING', counts:'STRING', electorate:'STRING', quota:'STRING', total_valid:'STRING', total_valid_percent:'STRING', spoilt_votes:'STRING', total_poll:'STRING', total_poll_percent:'STRING'})

(ConstituencyCandidate {id, area:'STRING', election_date:'INT/STRING', name:'STRING', party:'STRING', proof_vote:'STRING', share_vote:'STRING', quota:'STRING', count:'STRING', status:'STRING', seat:'STRING'})


//RELATIONS
//In order to run relation generation, queries import smallest backup, or initialize with crawler
 
//---!!!!!!!!!!!!!!!!!!!!!!!!!!!!!---
//---THE LAST BACKUP ALREADY CONTAINS THESE---
//---!!!!!!!!!!!!!!!!!!!!!!!!!!!!!---

//***RUN_FOR*** (PARTY)
match (cc:PersonHistory), (p:Party)
where cc.party = p.Name
create (cc)-[r:RUN_FOR]->(p)
return r

//***RUN_IN_CONST*** 
//(find witch Constituency a person run in)

match (cc:ConstituencyCandidate), (c:Constituency) 
where cc.area = c.name 
create (cc)-[r:RUN_IN_CONST]->(c)
return r limit 50000;

//***PERSON_IN_CONST*** 
//(connection between personal history and constitution results)
//only create 50000 relations, as there are over 2 million!

match (cc:ConstituencyCandidate), (ph:PersonHistory)
where cc.name = ph.person
and cc.name is not null
and ph.person is not null
create (ph)-[r:PERSON_IN_CONST]->(cc)
return r limit 50000;
```
#### Find nodes based on relation and filters
Find candidates who got elected for each political party. The query will match the relations between Political parties and PersonHistory and then apply filers for status and election date.
>Reference: [Match nodes & realitions](http://neo4j.com/docs/stable/query-match.html) 
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
>Reference: [Node matching - WHERE](http://neo4j.com/docs/stable/query-where.html)
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
RETURN 
    distinct m.name, m.area, m.election_date
ORDER BY
	m.election_date desc, 
	m.area
```

#### Find shortest path between nodes
Find the sortest path between two Candidates.
>Reference: [Match nodes & realitions](http://neo4j.com/docs/stable/query-match.html) 
```cypher
MATCH p=shortestPath(
  (c1:ConstituencyCandidate {name:"Jim Tallon"})-[*]-(c2:ConstituencyCandidate {name:"Charlie Keddy"})
)
RETURN p
```

## Notes
**Github does not support large files, so the final working database, with data is available at [Google Drive](https://drive.google.com/file/d/0B4tkAG6jw0etWEVxWFViSHhYcEk/view?usp=sharing)**<br>
The exported cypher queries contain a single large transaction which can take a long time to import, but there are options to import with split. 


## References
1. [Neo4J website](http://neo4j.com/), the website of the Neo4j database.
2. [Neo4j's From SQL to Cypher](http://neo4j.com/developer/guide-sql-to-cypher/)
3. [Neo4J's NoSql comparison](http://neo4j.com/developer/graph-db-vs-nosql/).
4. [Neo4j Cookbook - Amazon](http://www.amazon.com/gp/product/178328725X/) 
5. [Python 2 documentation](https://docs.python.org/2/), the offical python v2.* documentation.
6. [electionsireland.org/](http://electionsireland.org/), data for crawling.
7. [Java.com - jre installer](https://java.com/en/download/)
8. [SAX - wikipedia](https://en.wikipedia.org/wiki/Simple_API_for_XML) 
9. [Python lxml - documentation](http://lxml.de/) 
10. [xPath - wikipedia](https://en.wikipedia.org/wiki/XPath)
