import time
from get_client import client, OPERATOR_ID, OPERATOR_KEY, config_user_client
from create_account import HederaAccount
from hedera import (
    TopicCreateTransaction,
    TopicMessageQuery,
    TopicMessageSubmitTransaction,
    PyConsumer,
	)

class Topic:
    '''
    Create a new topic
    '''
    def __init__(self, **kwargs):
        self.memo = kwargs.get("memo", "N/A")   
    def create(self):
        topic = TopicCreateTransaction(
            ).setTopicMemo(self.memo
            ).execute(client)

        time.sleep(5)
        return topic


#Used to pick up response form Mirror node and print to console
def show_message(*args):
    print( f'time: {args[0]}, received: {args[2]}')


class Subscribe:
    '''
    Used to create a new client and subscribe to the new topic
    '''
    def __init__(self, **kwargs):
        self.topic = kwargs.get("topic")
        self.topic_id = self.topic.getReceipt(client).topicId

        new_acc = HederaAccount().create_new_account()
        
        self.cust_acc_id = new_acc["acc_id"]
        self.cust_public_key = new_acc["public_key"]
        self.cust_private_key = new_acc["private_key"]

        #this is the new client
        self.client = config_user_client(
            acc_id = self.cust_acc_id,
            private_key = self.cust_private_key
            )

        sub = TopicMessageQuery(
            ).setTopicId(self.topic_id
            ).subscribe(self.client, PyConsumer(show_message))

class Message:

    def __init__(self, **kwargs):
        self.topic = kwargs.get("topic")
        self.topic_id = self.topic.getReceipt(client).topicId
        self.message = kwargs.get("message")

    def send(self):
        msg = TopicMessageSubmitTransaction(
            ).setTopicId(self.topic_id
            ).setMessage(self.message
            ).execute(client)

        receipt = msg.getReceipt(client)
        status = receipt.status.toString()
        if status == "SUCCESS":
            message = f'Well done, You have sent a message "{self.message}"'
            print(message)

        else:
            message = "Something went wrong"
            print(message)
        


class ManageMessage:

    def __init__(self, *args, **kwargs):

        self.topic = kwargs.get("topic")
        self.message = kwargs.get("message")
        self.memo = kwargs.get("memo")
        
        msg = Message(
            topic = self.topic,
            message = self.message)
        
        #send message
        msg.send()
