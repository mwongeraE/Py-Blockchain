import solcx
import json
import os

solcx.install_solc("0.6.0")

from solcx import compile_standard
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# Compile our solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode.sourceMap"]}
            }
        },
    }
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache 1.1 Sepolia
w3 = Web3(
    Web3.HTTPProvider("https://sepolia.infura.io/v3/e5644cfc9d10462d929c9160b56fdd84")
)
chain_id = 11155111
my_address = "0x8e98CC3BE969B8171626bCf51ff747971fcd8fbe"
private_key = os.getenv("private_key")

# Create the contract in py
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)
print(nonce)

# 1 Build transaction
# 2 Sign a transaction
# 3 Send a transaction
transaction = SimpleStorage.constructor().build_transaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# Send this signed transactions
print("Deploying contract ...")

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed")
# Working with contract
# Contract abi
# Contract address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> simulate making a call and getting a return value
# transact -> Actually make a state change

# Initial value of favorite number
print(simple_storage.functions.retrieve().call())
print("Updating contract ...")
store_transaction = simple_storage.functions.store(15).build_transaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated")
print(simple_storage.functions.retrieve().call())
