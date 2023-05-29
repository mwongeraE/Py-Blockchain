from brownie import FundMe
from .helpful_scripts import get_account_fund_me


def deploy_fund_me():
    account = get_account_fund_me()
    fund_me = FundMe.deploy({"from": account})
    print(f"Contract deployd to {fund_me.address}")


def main():
    deploy_fund_me()
