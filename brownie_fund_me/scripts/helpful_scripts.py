from brownie import network, config, accounts


def get_account_fund_me():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
