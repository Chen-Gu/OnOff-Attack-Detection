pragma solidity ^0.4.0;

contract OnoffDetect{
    uint256 thr = 2.0*1000;
    uint256 TimeSlice = 30; //time :s
    function time(uint256 ta, uint256 tb) public view returns(bool){
        uint256 t;
        t = tb - ta;
        if (t >= TimeSlice){
            return true;
        }        
        else{
            return false;
        }
    }
    function judge(uint256 df) public view returns(bool){
        if (df > thr){
            return true;
        }           
        else{
            return false;
        }         
    }
}