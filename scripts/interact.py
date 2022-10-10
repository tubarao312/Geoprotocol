from web3 import Web3
import json
from web3.middleware import geth_poa_middleware
from time import sleep
import os
import pandas as pd

# Open Wallet Info JSON
with open("walletInfo.json", "r") as file:
    walletInfo = json.load(file)

# Assign Private and Public Keys
PRIVATE_KEY = walletInfo["main"]["private"]
PUBLIC_KEY = walletInfo["main"]["public"]

# Connect to Infura Node
NODE_URL = walletInfo["infuraURL"]
web3 = Web3(Web3.HTTPProvider(NODE_URL))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# ABI Path to Data Bank Contract
ABI_PATH = os.path.dirname(os.getcwd()) + "\\build\\contracts\\DataBank.json"

# Open Contract Info JSON
with open("contractInfo.json", "r") as file:
    contractInfo = json.load(file)

# Fetch databank contract address
ADDRESS = contractInfo["databank"]

print(ABI_PATH)

# Fetch contract
def get_contract():
    """Gets the Data Bank Contract."""
    
    with open(ABI_PATH) as f:
        abi = json.load(f)

    return web3.eth.contract(address=ADDRESS, abi=abi["abi"])

# Contract Interaction Functions

def build_report_dict(bank, index) -> dict:
    """Builds a dictionary of a report's data."""
    
    # Fetch Report Data
    address = web3.toChecksumAddress(PUBLIC_KEY)

    # Call all getter functions
    reportType = bank.functions.get_report_type(index).call({'from': address })
    reportImage = bank.functions.get_report_image(index).call({'from': address})
    reportText = bank.functions.get_report_text(index).call({'from': address})
    reportLocation = bank.functions.get_report_location(index).call({'from': address})
    reportApproved = bank.functions.get_report_approved(index).call({'from': address})
    reportStaked = bank.functions.get_report_staked_amount(index).call({'from': address})
    reportReporter = bank.functions.get_report_reporter(index).call({'from': address})
    reportTimestamp = bank.functions.get_report_timestamp(index).call({'from': address})

    # Dictionary of report data
    report = {
        "reportType": reportType,
        "reportImage": reportImage,
        "reportText": reportText,
        "reportLocation": reportLocation,
        "reportApproved": reportApproved,
        "reportStaked": reportStaked,
        "reportReporter": reportReporter,
        "reportTimestamp": reportTimestamp
    }

    return report

def approve_report(bank, index):
    """Approves a report in the Data Bank Contract."""

    # Build Transaction
    tx = bank.functions.approve_report(index).buildTransaction({
        'from': PUBLIC_KEY,
        'nonce': web3.eth.get_transaction_count(PUBLIC_KEY)
        })

    # Sign Transaction with Private Key
    tx_create = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)

    # Send TXN and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

def submit_report(bank, reportType, image, text, location):
    """Submits a report to the Data Bank Contract."""

    # Build Transaction
    tx = bank.functions.submit_report(reportType, image, text, location).buildTransaction({
        'value': 5000,
        'from': PUBLIC_KEY,
        'nonce': web3.eth.get_transaction_count(PUBLIC_KEY)
        })

    # Sign Transaction with Private Key
    tx_create = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)

    # Send TXN and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

def build_report_df(bank, lastNReports):
    """Builds a Pandas DataFrame of the last N reports."""

    # Fetch Report Data
    address = web3.toChecksumAddress(PUBLIC_KEY)
    reportCount = bank.functions.get_report_count().call({'from': address})

    # Create DataFrame
    df = pd.DataFrame(columns=["reportType", "reportImage", "reportText", "reportLocation", "reportApproved", "reportStaked", "reportReporter", "reportTimestamp"])

    # Populate DataFrame
    for i in range(reportCount - lastNReports, reportCount):
        report = build_report_dict(bank, i)
        df = pd.concat([df, pd.DataFrame(report, index=[i])])

    return df

# Testing
bank = get_contract()

d = build_report_df(bank, 8)

d.head()