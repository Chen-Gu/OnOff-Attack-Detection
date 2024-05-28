// SPDX-License-Identifier: SimPL-2.0
pragma solidity ^0.8.24;

contract OnOffDetect {
    uint256 private constant THR = 0.8 * 1000; // threshold
    uint256 private constant TIMESLICE = 30; // time in seconds
    bool private timeIntervalResult;
    bool private onOffAttackResult;

    function isTimeInterval(uint256 ta, uint256 tb) public pure returns (bool) {
        uint256 t = tb - ta;
        if (t >= TIMESLICE){
            return true;
        } 
        else{
            return false;
        }
    }

    function isOnOffAttack(uint256 df) public pure returns (bool) {
         if (df > THR){
            return true;
        }           
        else{
            return false;
        }          
    }
    
    function setTimeResult(uint256 ta, uint256 tb) public {//set
        timeIntervalResult = isTimeInterval(ta, tb);
    }

    function setOnOffAttackResult(uint256 df) public {
        onOffAttackResult = isOnOffAttack(df);
    }

    function getTimeResult() public view returns (bool) {//get
        return timeIntervalResult;
    }

    function getOnOffAttackResult() public view returns (bool) {
        return onOffAttackResult;
    }
}
