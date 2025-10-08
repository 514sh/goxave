import os

from pymongo import MongoClient

from goxave.api.service_layer import unit_of_work

DB_NAME = os.environ["DB_NAME"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_REPLICASET = os.environ["DB_REPLICASET"]

REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_HOST = os.environ["REDIS_HOST"]
FIREBASE_AUTH_PROJECT_ID = os.environ["FIREBASE_AUTH_PROJECT_ID"]
PROXY_URL = os.environ["PROXY_URL"]


_client = None


def get_database_client():
    global _client
    if _client is None:
        _client = MongoClient(host=DB_HOST, port=int(DB_PORT), replicaSet=DB_REPLICASET)
    return _client


def create_session(client=get_database_client()):
    return client.start_session()


uow = unit_of_work.UnitOfWork(get_database_client(), DB_NAME)
