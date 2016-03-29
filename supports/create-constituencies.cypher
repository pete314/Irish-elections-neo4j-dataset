// The data setup is in the ./backup_LARGES_NUMBER.cypher
// Please use it to rebuild the database
// In this file I only keep the relation building scripts

//RUN_FOR (PARTY)
match (cc:PersonHistory), (p:Party)
where cc.party = p.Name
create (cc)-[r:RUN_FOR]->(p)
return r

//RUN_IN_CONST (find witch Constituency a person run in)
match (cc:ConstituencyCandidate), (c:Constituency) 
where cc.area = c.name 
create (cc)-[r:RUN_IN_CONST]->(c)
return r limit 50000;

//PERSON_IN_CONST (connection between personal history and constitution results)
match (cc:ConstituencyCandidate), (ph:PersonHistory)
where cc.name = ph.person
and cc.name is not null
and ph.person is not null
create (ph)-[r:PERSON_IN_CONST]->(cc)
return r limit 50000;