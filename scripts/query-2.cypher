/*
FILEDS:
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
Find people who run in the same election as Enda Kenny
and  got more than 10000 votes.
*/

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


/******************************
	What I tried before
*******************************/
/////////////
MATCH (ek:ConstituencyCandidate{name:"Enda Kenny"}),(nb:ConstituencyCandidate{name:".*"}), p = allShortestPaths((ek)-[r:RUN_IN_CONST]-(nb))
RETURN p
/////////////
MATCH (ConstituencyCandidate{name:"Enda Kenny"})<-[:RUN_IN_CONST]-(Constituency)-[:RUN_IN_CONST]->(_constituency)
RETURN _constituency.name, collect(constituency)
/////////////
MATCH (ConstituencyCandidate{name:"Enda Kenny"})-[r:PERSON_IN_CONST]->() RETURN r LIMIT 25
/////////////
match (ConstituencyCandidate{name:"Enda Kenny"})-[*0..2]-(n) return n;