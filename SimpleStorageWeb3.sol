// SPDX-License-Identifier: MIT 
pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 favoriteNumber;
    bool favoritebool;

    struct People {
        uint256 favoriteNumber;
        string name;
    }
    People[] public people;
    mapping(string => uint256) public nametoFavoriteNumber;
    
  function store(uint256 _favoriteNumber) public  returns(uint256) {
      favoriteNumber = _favoriteNumber;
      return _favoriteNumber;
  }
  function retrieve() public view returns(uint256) {
      return favoriteNumber;
  }


  function addperson(string memory _name, uint256 _favoriteNumber) public {
      people.push(People(_favoriteNumber,_name));
      nametoFavoriteNumber[_name] = _favoriteNumber;
  }


}