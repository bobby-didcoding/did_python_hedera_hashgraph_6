from  get_client import client
from hedera import (
	PrivateKey,
	AccountId,
	AccountCreateTransaction,
	Hbar,
	AccountBalanceQuery
	)

class HederaAccount:

	def __init__(self, *args, **kwargs):

		self.private = PrivateKey.generate()
		self.public = self.private.getPublicKey()

		tran = AccountCreateTransaction()

		resp = tran.setKey(self.public).setInitialBalance(Hbar.fromTinybars(10_000_000_000)).execute(client)

		self.receipt = resp.getReceipt(client)


	def create_new_account(self):

		acc_id = self.receipt.accountId

		balance = AccountBalanceQuery().setAccountId(acc_id).execute(client)
		balance_text = balance.hbars.toString()

		return {
			'acc_id' : acc_id.toString(),
			'public_key' : self.public.toString(),
			'private_key' : self.private.toString(),
			'balance': balance_text,
			}


class HederaData:

	def __init__(self, *args, **kwargs):

		self.acc_id = kwargs.get("acc_id")
		self.client = kwargs.get("client")

	def balance(self):

		acc_id = AccountId.fromString(self.acc_id)
		balance = AccountBalanceQuery().setAccountId(acc_id).execute(self.client).hbars.toString()		
		return balance

	def get_cost(self):

		acc_id = AccountId.fromString(self.acc_id)
		cost = AccountBalanceQuery().setAccountId(acc_id).getCost(self.client)	
		return cost

