import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/svc8ft"
sqs = boto3.client('sqs')

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

mymessages = []
myhandles = []

def get_message():
    for i in range(10):
        try:
            # Receive message from SQS queue. Each message has two MessageAttributes: order and word
         # You want to extract these two attributes to reassemble the message
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )
        # Check if there is a message in the queue or not
            if "Messages" in response:
                for message in response['Messages']:
                    # extract the two message attributes you want to use as variables
                    # extract the handle for deletion later
                    order = message['MessageAttributes']['order']['StringValue']
                    word = message['MessageAttributes']['word']['StringValue']
                    handle = message['ReceiptHandle']

                    mymessages.append({"order": order, "word": word})
                    myhandles.append(handle)

                # Print the message attributes - this is what you want to work with to reassemble the message

            # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
                exit(1)
            
        # Handle any errors that may occur connecting to SQS
        except ClientError as e:
            print(e.response['Error']['Message'])

# Trigger the function
if __name__ == "__main__":
    get_message()

print(mymessages)

def numerify(message):
    return int(message['order'])

decoded = sorted(mymessages, key=numerify)

phrase = [message['word'] for message in decoded]

print(phrase)

for handle in myhandles:
    delete_message(handle)