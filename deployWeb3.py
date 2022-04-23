import os
import json
from web3 import Web3
from dotenv import load_dotenv #for getting data from .env file
from solcx import compile_standard, install_solc
install_solc("0.6.0")

load_dotenv()
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


install_solc("0.6.0")

# Solidity Source Code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        }

    },
    solc_version="0.6.0",
)
with open("compiled_code.json","w") as file:
    json.dump(compiled_sol, file)

#to deploy a contract, you need an abi and bytecode
#get bytecode
    bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
        "bytecode"
        ]["object"]


#getabi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#for connecting to ganache or rinkeby
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/6a569b434c2e45469e2268020555fd93"))
chain_id = 4
my_address = "Removed because of Github"
private_key = os.getenv("PRIVATE_KEY")

#create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
#Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

'''
1- Build a transaction
2- sign a transaction
3- send a transaction
'''
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "gasPrice": w3.eth.gas_price, "nonce": nonce}
    )
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
 
#send this signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_reciept = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed")

'''
working with a contract you always need:
contract address
contract abi
'''
simple_storage = w3.eth.contract(address=tx_reciept.contractAddress, abi=abi)
#Call -> Simulate making the call and getting a return value
#transact -> Actually make a state change

#Initial value of favorite number
print(simple_storage.functions.retrieve().call())
print("Updating Contract....")
#print(simple_storage.functions.store(15).call())
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1, "gasPrice": w3.eth.gas_price }
) 
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_reciept = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated")
#brought from smart contract
print(simple_storage.functions.retrieve().call())
