from brownie import accounts, config, SimpleStorage, network
import os


#brownie already knows whether to call or transact
#brownie run scripts/deploy.py
#bvvvvjhgsajghav - password

def deploy_simple_storage():
  account = get_account()
  simple_storage= SimpleStorage.deploy({"from": account})#deploy your contract from an account
   #account = accounts.load("splintrider-account")
   #print(account)
   # or
   #account = accounts.add(os.getenv("PRIVATE_KEY")) for getting key from .env file
   # account = accounts.add(config["wallets"]["from_key"]) 
   #account#use the variable again in env if its undefined
  stored_value = simple_storage.retrieve()
  print(stored_value)
  transaction = simple_storage.store(15, { "from": account})
  transaction.wait(1)#how many blocks we want to wait
  updated_stored_value = simple_storage.retrieve()
  print(updated_stored_value)


  
  
def get_account():
  if network.show_active() == "development":
    return accounts[0]
  else:
      return accounts.add(config["wallets"["from_key"]])
  

  


def main(): 
  deploy_simple_storage()