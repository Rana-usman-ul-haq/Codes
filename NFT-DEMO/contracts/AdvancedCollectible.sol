//SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Breed{PUG, SHIBA_INU, ST_BERNARD}
    mapping(uint256 => Breed) tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;

 constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee) public 
     VRFConsumerBase(_vrfCoordinator, _linktoken)
     ERC721("Dogie", DOG)
     {
      tokenCounter = 0;
      keyhash = _keyhash;
      fee = _fee;
    }
     
    
    
    function createcollecible(string memory tokenURI) public view returns (bytes32){
        bytes32 requestId = requestRandomness(keyhash, fee);

    }



     
    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) interal override {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        address owner = requestIdToSender[requestId];
        _safemint(xxx, newTokenId);
        //_setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
     } 
}