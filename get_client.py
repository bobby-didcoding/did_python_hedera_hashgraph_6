import os
from hedera import Client, AccountId, PrivateKey

OPERATOR_ID = AccountId.fromString(os.environ["OPERATOR_ID"])
OPERATOR_KEY = PrivateKey.fromString(os.environ["OPERATOR_KEY"])

client = Client.forTestnet()
client.setOperator(OPERATOR_ID, OPERATOR_KEY)


def config_user_client(*args, **kwargs):

	acc_id = kwargs.get("acc_id")
	private_key = kwargs.get("private_key")

	OPERATOR_ID = AccountId.fromString(acc_id)
	OPERATOR_KEY = PrivateKey.fromString(private_key)
	client = Client.forTestnet()
	return client.setOperator(OPERATOR_ID, OPERATOR_KEY)
