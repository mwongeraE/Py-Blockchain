from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account, "gas_price": 10})
    starting_value = simple_storage.retrieve()
    expected = 0
    # Assert
    assert starting_value == expected


def test_updating_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account, "gas_price": 10})
    # Act
    expected = 15
    simple_storage.store(expected, {"from": account, "gas_price": 10})
    # Assert
    assert expected == simple_storage.retrieve()
