from sys import implementation
from webbrowser import get
from brownie import FundMe, config, network, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENT,
)


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract
    # if we are on presistent network like rinkeby, use the associated address
    # otherwise deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()

        price_feed_address = MockV3Aggregator[-1].address

    fundme = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"contract deployed to{fundme.address}")
    return fundme


def main():
    deploy_fund_me()
