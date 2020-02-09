from abc import ABC

import boto3
from boto3.dynamodb.conditions import Key
import functools
import abc

def singleton(cls):
    """Make a class a Singleton class (only one instance)"""
    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance
    wrapper_singleton.instance = None
    return wrapper_singleton


class Storage(object):
    def __init__(self):
        pass

    @abc.abstractmethod
    def store_connection(self, connection_id):
        pass

    @abc.abstractmethod
    def delete_connection(self, connection_id):
        pass

    @abc.abstractmethod
    def store_record(self, connection_id, record):
        pass


@singleton
class DynamoStorage(Storage, ABC):
    def __init__(self, connections_table_name, records_table_name):
        super().__init__()
        self.__connections_table = boto3.resource('dynamodb').Table(connections_table_name)
        self.__records_table = boto3.resource('dynamodb').Table(records_table_name)

    def store_connection(self, connection_id):
        self.__connections_table.put_item(
            Item={
                'connection_id': connection_id
            }
        )

    def delete_connection(self, connection_id):
        self.__connections_table.delete_item(
            Key={
                'connection_id': connection_id
            }
        )

    def store_record(self, connection_id, record):
        self.__records_table.put_item(
            Item={
                'connection_id': connection_id,
                'record': record
            }
        )