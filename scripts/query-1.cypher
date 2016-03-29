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
Select all the candidates, parties and votes, with constituency 
where more than 10000 people voted
*/

MATCH 
	(cc:ConstituencyCandidate )-[r:RUN_FOR]->()
WHERE
	length(cc.proof_vote) > 5
RETURN r