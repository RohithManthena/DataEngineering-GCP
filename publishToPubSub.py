# # from proto import message
# from requests import session
# from os import environ
# from time import sleep
# import logging
# from concurrent import futures
# from google.cloud.pubsub_v1 import PublisherClient
# from google.cloud.pubsub_v1.publisher.futures import Future
# import os
# from requests.sessions import Session 
# import utils

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:\Data Engineering\DataEngg-StreamApiDatatoGCS\gcpServiceAccountkey.json"


# from google.cloud import pubsub_v1
# root = logging.getLogger()
# root.setLevel(logging.DEBUG)


# class publishToPubSub:
#     def __init__(self) -> None:
#         self.project_id=utils.project_id
#         self.topic_id=utils.topic_id
#         self.publisher_client=PublisherClient()
#         self.topic_path=self.publisher_client.topic_path(self.project_id,self.topic_id)
#         self.publish_futuers=[]

#     def get_crypto_ticker_data(self) -> str:
#         params={
#             "key":utils.api_key,   
#             "convert":"USD",
#             "interval":'1d',
#             "per-page":'100',
#             "page":"1"
#         }
#         print("working")
#         ses =Session()
#         res = ses.get("https://api.nomics.com/v1/currencies/ticker",params=params,stream=True)

#         if 200<= res.status_code <400:
#             #logging.info(f"Response - {res.status_code}: {res.text}")
#             return res.text
#         else:
#             raise Exception(f"failed to fetch api data - {res.status_code}: {res.text}")

#     def get_callback(self, publish_future: Future, data: str) -> callable:
#         def callback(publish_future):
#             try:
#                 # wait for 60 seconds for the publish call to succeed
#                 logging.info(publish_future.result(timeout=60))
#             except futures.TimeoutError:
#                 logging.error(f"publishing {data} timed out") 

#         return callback

#     def publish_message_to_topic(self, message: str)-> None:

#         # when you publish a message the client returns a future
#         publish_future=self.publisher_client.publish(self.topic_path,message.encode('utf-8'))

#         # non blocking. publish failures are handled in the callback function.
#         publish_future.add_done_callback(self.get_callback(publish_future,message))
#         self.publish_futuers.append(publish_future)
 
#         #wait for all the publish futures to resolve before exciting.
#         futures.wait(self.publish_futuers, return_when=futures.ALL_COMPLETED)
#         logging.info(f"published messages with error handling to {self.topic_path}")


# if __name__=="__main__":
#     #init_logging()

#     svc=publishToPubSub()

#     message = svc.get_crypto_ticker_data()
#     svc.publish_message_to_topic(message)





# import tweepy

# auth = tweepy.OAuthHandler('wjTlLK7qrYCfc5O97p3EdsqPE', 'OGAB6ypsCxyla99WdxpQ1dXSIdrOFVbFQXh9qRHu2oDdnZTGI7')
# auth.set_access_token('1407699584-3c5JBK3zyfFQrQ9eZFonKyrmQzfyAOUQQd2t7n4', 'Lk1Au1174i3PLFBbD8ekYsWgT1Z95zpi0YnQ05oBSlzp2')

# api=tweepy.API(auth)

# class StreamListener(tweepy.StreamListener):
#     # def on_status(self, status):
#     #     print(status.text)

#     def on_error(self, status_code):
#         if status_code == 420:
#             return False





# from proto import message
from requests import session
from os import environ
from time import sleep
import logging
from concurrent import futures
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.publisher.futures import Future
import os
from requests.sessions import Session 
import utils
import tweepy
from tweepy import API

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:\Data Engineering\DataEngg-StreamApiDatatoGCS\gcpServiceAccountkey.json"


from google.cloud import pubsub_v1
root = logging.getLogger()
root.setLevel(logging.DEBUG)

auth = tweepy.OAuthHandler('wjTlLK7qrYCfc5O97p3EdsqPE', 'OGAB6ypsCxyla99WdxpQ1dXSIdrOFVbFQXh9qRHu2oDdnZTGI7')
auth.set_access_token('1407699584-3c5JBK3zyfFQrQ9eZFonKyrmQzfyAOUQQd2t7n4', 'Lk1Au1174i3PLFBbD8ekYsWgT1Z95zpi0YnQ05oBSlzp2')

api=tweepy.API(auth)

class publishToPubSub(tweepy.StreamListener):
    def __init__(self) -> None:
        self.project_id=utils.project_id
        self.topic_id=utils.topic_id
        self.publisher_client=PublisherClient()
        self.topic_path=self.publisher_client.topic_path(self.project_id,self.topic_id)
        self.publish_futuers=[]
        self.api = api or API()

    def on_status(self, status):
        self.publish_message_to_topic(status.text)



    def get_callback(self, publish_future: Future, data: str) -> callable:
        def callback(publish_future):
            try:
                # wait for 60 seconds for the publish call to succeed
                logging.info(publish_future.result(timeout=60))
            except futures.TimeoutError:
                logging.error(f"publishing {data} timed out") 

        return callback

    def publish_message_to_topic(self, message: str)-> None:

        # when you publish a message the client returns a future
        publish_future=self.publisher_client.publish(self.topic_path,message.encode('utf-8'))

        # non blocking. publish failures are handled in the callback function.
        publish_future.add_done_callback(self.get_callback(publish_future,message))
        self.publish_futuers.append(publish_future)
 
        #wait for all the publish futures to resolve before exciting.
        futures.wait(self.publish_futuers, return_when=futures.ALL_COMPLETED)
        logging.info(f"published messages with error handling to {self.topic_path}")


if __name__=="__main__":
    #init_logging()

    svc=publishToPubSub()

    # message = svc.get_crypto_ticker_data()
    # svc.publish_message_to_topic(message)

    stream_listener = publishToPubSub()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=["trump", "clinton", "hillary clinton", "donald trump"])