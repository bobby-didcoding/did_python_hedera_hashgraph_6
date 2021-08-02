import os
from get_client import client, OPERATOR_ID, OPERATOR_KEY, config_user_client
from create_account import HederaAccount, HederaData
from hedera import (
	PrivateKey,
	AccountId,
	AccountCreateTransaction,
	Hbar,
	AccountBalanceQuery,
	TransferTransaction
	)



class Transfer:

	def __init__(self, **kwargs):

		self.amount = kwargs.get("amount")
		self.description = kwargs.get("description")

		self.cust_acc_id = kwargs.get("cust_acc_id")
		self.cust_private_key = kwargs.get("cust_private_key")

		#this is the new client
		self.client = config_user_client(
			acc_id = self.cust_acc_id,
			private_key = self.cust_private_key
			)

	def create(self):

		#convert millibar to tinybar
		tinybar_conversion = int(self.amount) * 100_000_000

		amount = Hbar.fromTinybars(int(tinybar_conversion))
		acc_id = AccountId.fromString(self.cust_acc_id)

		our_start_balance = HederaData(acc_id =os.environ["OPERATOR_ID"], client=client).balance()
		cust_start_balance = HederaData(acc_id = self.cust_acc_id, client=self.client).balance()
		
		receipt = TransferTransaction(
		       ).addHbarTransfer(acc_id, amount.negated()
		       ).addHbarTransfer(OPERATOR_ID, amount
		       ).setTransactionMemo(self.description
		       ).execute(self.client) # notice that we are using self.client from __init_ the transaction must have the sender signiture!!

		status = receipt.getReceipt(self.client).status.toString()

		tran_id = receipt.getRecord(self.client).transactionId

		if status == "SUCCESS":
			tran_id = tran_id.toString()
			our_end_balance = HederaData(acc_id = os.environ["OPERATOR_ID"], client=client).balance()
			
			cust = HederaData(acc_id = self.cust_acc_id, client=self.client)
			cust_end_balance = cust.balance()
			cust_cost = cust.get_cost()

			cust_cost = f'{(float(cust_start_balance.split(" ")[0]) - float(cust_end_balance.split(" ")[0]))/100_000_000} tiny bar'
			print('The transaction was a success')
			print(f'Transaction ID: {tran_id}')
			print(f'The customer HBAR balance went down from {cust_start_balance} to {cust_end_balance}')
			print(f'The customer transaction fee was {cust_cost}')
			print(f'Our HBAR balance went up from {our_start_balance} to {our_end_balance}')

		else:
			message = "Something went wrong"
			print(message)

		
class ManageTransfer:

	def __init__(self, *args, **kwargs):

		self.amount = kwargs.get("amount")
		self.description = kwargs.get("description")

		new_acc = HederaAccount().create_new_account()

		self.cust_acc_id = new_acc["acc_id"]
		self.cust_public_key = new_acc["public_key"]
		self.cust_private_key = new_acc["private_key"]

	def make_transfer(self):

		transfer = Transfer(

				amount=self.amount,
				description=self.description,
				cust_acc_id = self.cust_acc_id,
				cust_private_key = self.cust_private_key
			)

		transfer.create()
