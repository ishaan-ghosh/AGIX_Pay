import os
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv('SEPOLIA_NODE_URL')))
AGIX_CONTRACT_ADDRESS = os.getenv('AGIX_CONTRACT_ADDR')  
# Needed from SNET team
AGIX_ABI = []
from_private_key = os.getenv('FROM_PRIVATE_KEY')




# NOTE: SET DELIVERY WALLET ADDRESS
to_address = ''

# NOTE: SET TRANSACTION AMOUNT IN AGIX TOKENS
amount = Web3.to_wei(1, 'ether')





def transfer_agix(from_private_key, to_address, amount):
    account = Account.from_key(from_private_key)
    contract = w3.eth.contract(address=AGIX_CONTRACT_ADDRESS, abi=AGIX_ABI)
    nonce = w3.eth.get_transaction_count(account.address)

    estimated_gas = contract.functions.transfer(to_address, amount).estimate_gas({
        'from': account.address,
        'nonce': nonce,
    })

    gas_limit = int(estimated_gas * 1.2)

    tx = contract.functions.transfer(to_address, amount).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': gas_limit, 
        'gasPrice': w3.eth.gas_price,
        'chainId': 11155111  
    })

    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_receipt

if __name__ == "__main__":
    receipt = transfer_agix(from_private_key, to_address, amount)
    print(f"Transaction successful. Transaction hash: {receipt['transactionHash'].hex()}")