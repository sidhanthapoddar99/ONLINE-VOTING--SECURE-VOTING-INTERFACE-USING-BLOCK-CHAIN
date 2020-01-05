	pragma solidity ^0.5.8;
/*
//smoke test
contract Election{
	//store candidate
	//read candidate
	string public candidate;
	//constructor
	//function Election () public {
	constructor () public {
		candidate = "candidate 1";
	}
}*/

// list candidate
contract Election{

	//mode a candiadate
	struct Candidate{
		uint id;
		string name;
		uint voteCount;
	}
	//store a candidate
	//fetch a candidate
	mapping(address => bool) public voters;

	mapping(uint => Candidate ) public candidates;
	//store candidate count
	uint public candidatesCount;

	// voted event
    event votedEvent (
        uint indexed _candidateId
    );

	constructor () public {
		addCandidate("BJP");
		addCandidate("CONG");
		addCandidate("AIADMK");
		addCandidate("NOTA");
	}
/*
	*You can fix it by saying memory for the bytes argument which is an array of byte
	*put "bytes *memory* data"  as  a variable
	*datalocation should be "storage" or "memory"
	*string memory _name
*/

	function addCandidate (string memory _name) private{
		candidatesCount ++;
		candidates[candidatesCount]= Candidate(candidatesCount, _name,0);

	}
	function vote (uint _candidateId) public {
        // update candidate vote Count
        candidates[_candidateId].voteCount ++;

    }
}
