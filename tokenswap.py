import json
from web3 import Web3
from datetime import datetime
from databaseconnection import *
from avaxsender import *

#Binance smart chain testnet rpc provider
rpc_provider = process.env.RPC_CONNECTION

#Rpc connection
web3 = Web3(Web3.HTTPProvider(rpc_provider))

#contract abi for migration contract
abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"getStaker","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"staker","type":"address"}],"name":"isClaimAvailable","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"stakeTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"stakedAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_staker","type":"address"}],"name":"stakerAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stakerLen","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

#contract address for migration contract
contract_address = web3.toChecksumAddress("0xa91144Bfbf55f90DEA5a1963389738014B8B3A3F")

#contract instance @web3
contract = web3.eth.contract(address = contract_address, abi = abi)


#admin address, this address will pay gas for transact() functions
admin_address = ""
admin_privatekey = ""


#staker amount. this will be used to iterate in for loop
stakerlen = contract.functions.stakerLen().call()


#all balances will be added to this dict
all_balances = dict()



#all balances as a function // balance'lar sql database'e çekilecek
def balances():
    for i in range(stakerlen):
        address = contract.functions.getStaker(i).call()
        all_balances[address] = contract.functions.stakerAmount(address).call()


#all_balances'a giden bütün verileri sql database'ine yazar
def addbalancestodatabase():
    create_table()
    now = datetime.now()
    today = now.strftime("%d/%m/%Y")

    for i,j in all_balances.items():
        
        if (contract.functions.isClaimAvailable(i).call()):

            add_data(i,j/(10**18),today)

            
def startmigrating():
    balances()
    addbalancestodatabase()

def finishmigrating():
    balances()
    for i in all_stakers:
        dbsent(i)
