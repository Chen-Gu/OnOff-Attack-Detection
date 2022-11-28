import numpy as np
import matplotlib.pyplot as plt
from numpy import polynomial as P
from sympy import *
import codecs
from web3 import Web3, HTTPProvider, eth
from web3.eth import Eth
from web3.middleware import geth_poa_middleware
from queue import Queue

# The setup of the smart contract
address_0 = "0x58d627990040181d7720886e84bCf0F3C11920C1"
abi = [{"constant":true,"inputs":[{"name":"ta","type":"uint256"},{"name":"tb","type":"uint256"}],"name":"time","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"df","type":"uint256"}],"name":"judge","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]
w3 = Web3(HTTPProvider("http://localhost:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
acc = w3.eth.accounts[0]
w3.eth.defaultAccount = acc
w3.geth.personal.unlockAccount(acc, "123")
address = w3.toChecksumAddress(address_0)
contract = w3.eth.contract(address, abi=abi)

def DetectionTime(ta, tb):
    tx_hash = contract.functions.time(ta, tb).transact()
    temp1 = w3.eth.waitForTransactionReceipt(tx_hash)
    return contract.functions.time(ta, tb).call()

def ReadTxt():
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
        flag = DetectionTime(listhead, listrear)
        if flag == True:
            break
        line = f.readline()
    f.close()
    return timestamp, trust

def get_all_function():
    print(contract.all_functions())

def AttackJudge(df):
    tx_hash = contract.functions.judge(df).transact()
    temp1 = w3.eth.waitForTransactionReceipt(tx_hash)
    return contract.functions.judge(df).call()

if __name__ == "__main__":
    timestamp, trust = ReadTxt()
    x = np.array(timestamp)
    y = np.array(trust)

    # Polynomial fitting
    z = np.polyfit(x, y, 3)
    m = symbols('m')
    f = z[0]*m**3 + z[1]*m**2 + z[2]*m + z[3]
    num = integrate(f, (m, 1, 3))
    print(int(num*1000))
    flag = AttackJudge(int(num*1000))

    if flag == True:
        print("No detection of the on-off attack.")
    else:
        print("Detection of the on-off attack.")



