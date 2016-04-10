============
PartyCandidates: id, constituency, party, candidate, date
Person: id, Name
PersonHistory: id, election, date, party, status, constituency, seat, votes, share, quota, person
Constituency: id, name, county, date, seats, candidates, counts, electorate, quota, total_valid, 
						total_valid_percent, spoilt_votes, total_poll, total_poll_percent
ConstituencyCandidate: id, area, election_date, name, party, proof_vote, share_vote, quota
										count, status, seat

QUERY DESCRIPTION:
===================
Find the sortest path between two Candidates
*/
MATCH p=shortestPath(
  (c1:ConstituencyCandidate {name:"Jim Tallon"})-[*]-(c2:ConstituencyCandidate {name:"Charlie Keddy"})
)
RETURN p
	
/******************************
	What I tried before

		The Queries below are for different result set
*******************************/
MATCH 
	(c.Constituency)-[:RUN_IN_CONST]->(c.ConstituencyCandidate),
	(c.Constituency)-[:RUN_IN_CONST]->(c.ConstituencyCandidate)
where
	
RETURN r LIMIT 25

MATCH
	(ph:PersonHistory)-[:PERSON_IN_CONST]-(c:ConstituencyCandidate),
	
where
	c.area =~ ".*ublin.*"
return distinct r




		
MATCH 
	(ph:PersonHistory)-[r1:RUN_FOR]->(p:Party)
WHERE
	p.name = "Fianna Fail"
return ph
UNION
MATCH
	(ph:PersonHistory)-[r2:PERSON_IN_CONST]->(c:ConstituencyCandidate)
where
	c.area =~ ".*alway.*"
return ph

RETURN r LIMIT 25



MATCH 
	(:Constituency { county: "Connaught" })<-[:RUN_IN_CONST]-(candidate)-[:RUN_IN_CONST]->(c)
optional match
	(person:PersonHistory)
where
	person.Person = candidate.name
RETURN distinct person, candidate.name, candidate.proof_vote, candidate.seat, candidate.election_date,  c.county, c.date
ORDER BY
	candidate.name


	MATCH (:Constituency { county: "Connaught" })<-[:RUN_IN_CONST]-(candidate)-[:RUN_IN_CONST]->(c)
RETURN distinct candidate.name, candidate.proof_vote, candidate.seat, candidate.election_date,  c.county, c.date
ORDER BY
	candidate.name
	
START candidate=node(*) 
MATCH (:Constituency { county: "Connaught" })<-[:RUN_IN_CONST]-(candidate)
optional match (candidate)-[:PERSON_IN_CONST]->(p)
where 
	has(candidate.name)
AND
	has(p.election)
RETURN distinct candidate.name, candidate.proof_vote, candidate.seat, candidate.election_date,  p.election, p.date
ORDER BY
	candidate.name
