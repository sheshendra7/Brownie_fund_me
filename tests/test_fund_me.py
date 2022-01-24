from operator import ge
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENT
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    # EntranceFee = fund_me.getEntranceFee()
    EntranceFee = 2500000000
    tx = fund_me({"from": account, "value": EntranceFee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == EntranceFee
    tx2.fund_me.withdraw({{"from": account}})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip("only for local testing")
    account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = account.add()
    with pytest.raises(execptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
