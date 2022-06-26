// contracts/migration.sol
// SPDX-License-Identifier: MIT //0xa91144Bfbf55f90DEA5a1963389738014B8B3A3F
pragma solidity 0.6.12;

import "./perabsc.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v3.4.0/contracts/utils/EnumerableSet.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/8e0296096449d9b1cd7c5631e917330635244c37/contracts/access/Ownable.sol";

contract Migration is Ownable{
    PERA pera = PERA(0xbF9f2fe1a4A04c9cb39E5B7737Cd01fc81FE670A);
    using EnumerableSet for EnumerableSet.AddressSet;
    mapping(address => uint) public stakedAmount;
    EnumerableSet.AddressSet stakedAddresses;
    mapping(address=>uint) public stakeTime;


    function transferFrom(uint256 _value) external {
        require(_value <= pera.balanceOf(msg.sender));
        stakedAmount[msg.sender] += _value;
        if (!stakedAddresses.contains(msg.sender)){
            stakedAddresses.add(msg.sender);
            }
        stakeTime[msg.sender] = block.number;
        pera.transferFrom(msg.sender, address(this), _value);
    }
    
    function withdraw() external onlyOwner(){
        uint amount = pera.balanceOf(address(this));
        pera.transfer(owner(), amount);
    }
    
    function stakerAmount(address _staker) external view returns(uint){
        uint amount = stakedAmount[_staker];
        return amount;
    }
    function getStaker(uint _index) external view returns(address){
        return stakedAddresses.at(_index);
    }
    function stakerLen() external view returns(uint){
        return stakedAddresses.length();
    }

    function isClaimAvailable(address staker) external view returns(bool){
        if(block.number - stakeTime[staker] >= 10){
            return true;
        }else{
            return false;
        }
    }

}