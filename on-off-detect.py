import linecache
import numpy as np
# import matplotlib.pyplot as plt
from numpy import polynomial as P
from sympy import *
import codecs
from web3 import Web3, HTTPProvider, eth
from web3.eth import Eth
from web3.middleware import geth_poa_middleware
from queue import Queue

address_0 = "0x4ee0CB375fFd6Ef29EdD7232fC0f920592621978"
abi = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "df",
				"type": "uint256"
			}
		],
		"name": "setOnOffAttackResult",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "ta",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "tb",
				"type": "uint256"
			}
		],
		"name": "setTimeResult",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getOnOffAttackResult",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTimeResult",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "df",
				"type": "uint256"
			}
		],
		"name": "isOnOffAttack",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "pure",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "ta",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "tb",
				"type": "uint256"
			}
		],
		"name": "isTimeInterval",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "pure",
		"type": "function"
	}
]
# Connect to the local geth
w3 = Web3(HTTPProvider("http://localhost:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
acc = w3.eth.accounts[0]
w3.eth.defaultAccount = acc
w3.geth.personal.unlockAccount(acc, "123")
address = w3.toChecksumAddress(address_0)
contract = w3.eth.contract(address, abi=abi)

time_results = []
judge_results = []

def isTimeInterval(ta, tb):  # Determine the right time interval and send results to the blockchian
    tx_hash = contract.functions.isTimeInterval(ta, tb).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)
    contract.functions.setTimeResult(ta, tb).transact()
    result = contract.functions.getTimeResult().call()
    time_results.append(result)
    return result

def readtxt():
    timestamp = []
    trust = []

    f = codecs.open('trust_value.txt', mode='r', encoding='utf-8')
    line = f.readline()

    while line:

        a = line.split('|')
        _timestamp = a[0]
        _trust = a[1]
        timestamp.append(float(_timestamp))
        trust.append(float(_trust))

        listhead = int(timestamp[0])
        listrear = int(timestamp[-1])
        flag = isTimeInterval(listhead, listrear)

        if flag == True:
            break
        line = f.readline()
    f.close()
    return timestamp, trust, listhead, listrear

def get_all_function():
    print(contract.all_functions())

def isOnOffAttack(df):  # Determine the on-off attack and send results to the blockchian
    tx_hash = contract.functions.isOnOffAttack(df).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)
    contract.functions.setOnOffAttackResult(df).transact()
    result = contract.functions.getOnOffAttackResult().call()
    judge_results.append(result)
    return result


if __name__ == "__main__":

    storeResult = []
    timestamp, trust, ta, tb = readtxt()

    x = np.array(timestamp)
    y = np.array(trust)

    z = np.polyfit(x, y, 3)

    m = symbols('m')
    f = z[0]*m**3 + z[1]*m**2 + z[2]*m + z[3]

    num = integrate(f, (m, ta, tb)) / (tb - ta)

    result = isOnOffAttack(int(num*1000))
    storeResult.append(result)

    if result == True:
        print("No on-off Attack Detected !!!")
    else:
        print("on-off Attack Detected!!!")



