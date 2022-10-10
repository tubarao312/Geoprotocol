from brownie import DataBank, Geocoin, network, config
import json, os
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

# Whether to verify the contracts on Etherscan
PUBLISH_CODE = True

# JSON Functions ########################################################

def get_json():
    path = os.path.dirname(os.path.abspath(__file__)) + "\\contractInfo.json"

    with open(path, "r") as file:
        addresses = json.load(file)

    return addresses

def update_json(dictionary):
    path = os.path.dirname(os.path.abspath(__file__)) + "\\contractInfo.json"

    with open(path, "w") as file:
        json.dump(dictionary, file)

# Deploying Contracts ##################################################

def deploy_databank():
    """ Deploys databank contract."""

    account = get_account()

    bank = DataBank.deploy(
        {"from": account}, publish_source=PUBLISH_CODE)

    return bank

# Main Function ########################################################

def main():
    address = deploy_databank().address

    d = {
        "databank": address,
        "geocoin": DataBank.at(address).get_token_address()
    }

    update_json(d)

    print("DataBank and Geocoin contracts successfully deployed!")