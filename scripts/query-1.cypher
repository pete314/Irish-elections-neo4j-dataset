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
Find candidates who got elected for each political party
*/

MATCH 
	(ph:PersonHistory)-[r:RUN_FOR]->(p:Party)
WHERE
	ph.date = "2016"
AND
	ph.status = "Elected"
RETURN distinct r

/******************************
	What I tried before
		Just as proof of work :)
*******************************/
MATCH p=(a:PersonHistory)-->(b:Constituency)-->(c:PersonHistory)
WHERE a.party=~'.*Fine.*' AND c.constituency=~'.*alway.*'
RETURN nodes(p)


MATCH 
	(ph:PersonHistory)-[r:RUN_FOR]->(p:Party)
WHERE
	length(ph.votes) > 5
RETURN r