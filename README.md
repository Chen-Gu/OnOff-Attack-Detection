# On-off Attack Detection

The script is used to detect the on-off attack for the trust system. It has been tested on the Ethereum to detect this attack when given a time period (ta, tb), and a threshold shared among all miner nodes. There are some main functions in the smart contract:

isTimeInterval: Check whether a specific time period is longer than the time period of (tb-ta).

isOnOffAttack: Check whether the on-off attack occurs when the variable df is large than a threshold.
