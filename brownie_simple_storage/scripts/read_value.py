from brownie import SimpleStorage, accounts, config


def read_contract():
    simple_storage = SimpleStorage[-1]
    #take index one less than length
    #ABI
    #address
    print(simple_storage.retrieve())