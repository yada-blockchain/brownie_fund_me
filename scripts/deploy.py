from unittest import mock
from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account, deploy_mocks, get_blockchain_environments

def deploy_fund_me():
    account = get_account()

    # Pass the price feed address to our fundme contract
    # If we are on a persistent network like rinkeBy, use associated address
    # otherwise, deploy mocks
    if network.show_active() not in get_blockchain_environments():
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source = config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")

    return fund_me


def main():
    deploy_fund_me()
