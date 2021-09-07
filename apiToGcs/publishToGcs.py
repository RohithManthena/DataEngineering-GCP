# from proto import message
from threading import Event
from google.cloud import storage
from google.cloud.client import Client
from requests import session
from os import environ, name
from time import sleep
import logging
import os
from pybase64 import b64decode
from pandas import DataFrame
from json import loads
from google.cloud.storage import bucket, Client


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:\Data Engineering\DataEngg-StreamApiDatatoGCS\gcpServiceAccountkey.json"

"""Publishes multiple messages to a Pub/Sub topic with an error handler."""
from concurrent import futures
from google.cloud import pubsub_v1


class cloudFunction:
    def __init__(self,event,context) -> None:
        self.project_id='dataengg-streamdatatogcs'
        self.topic_id='streamingApiData'
        self.event=event
        self.context=context
        self.gcsBucket="testingdemo-suryanarayana"

    def getData(self)-> str:
        logging.info(f"This function was triggered by messId {self.context.event_id} published at {self.context.timestamp} to {self.context.resource['name']}")
        if 'data' in self.event:
            pubsubMessage=b64decode(self.event['data']).decode("utf-8")
            logging.info(f"the decoded message is {pubsubMessage}")
            return pubsubMessage
        else:
            logging.error("No data received in the payload")
            return ""

    def dataTransformation(self,message:str) -> DataFrame:
        try:
            df=DataFrame(loads(message))
            if not df.empty:
                logging.info(f" created dataframe with {df.shape[0]} rows and {df.shape[1]} columns")
            else:
                logging.info(f"created empty dataframe.. check the data in event")
            return df
        except Exception as e:
            logging.error(f"encountered error while creating dataframe .. error message {str(e)}")
            raise

    def uploadToGCS(self, df:DataFrame, fileName:str='payload') -> None:
        storage_client=Client()
        bucket=storage_client.bucket(self.gcsBucket)
        blob=bucket.blob(f"{fileName}.csv")

        blob.upload_from_string(data=df.to_csv(index=False),content_type="text/csv")
        logging.info(f"file uploaded to {self.gcsBucket}")

def process(event,context):
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    sv=cloudFunction(event, context)

    message=sv.getData()

    df=sv.dataTransformation(message)
    payloadTimeStamp=df['price_timestamp'].unique().tolist()[0]

    sv.uploadToGCS(df,'crypto_data'+str(payloadTimeStamp))

if __name__=="__main__":
    process()

