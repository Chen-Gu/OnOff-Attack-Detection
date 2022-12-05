pragma solidity ^0.4.0;

contract onoffdetect{
    uint256 thr = 0.8*1000;
    uint256 timeslice = 30; //time :s

    function time(uint256 ta, uint256 tb) public view returns(bool){ //时间片
        uint256 t;
        t = tb - ta;
        if (t >= timeslice){
            return true;
        }
            
        else{
            return false;
        }
    }

    function judge(uint256 df) public view returns(bool) { //积分判断
        if (df > thr){
            return true;
        }
            
        else{
            return false;
        }
           
    }

}
