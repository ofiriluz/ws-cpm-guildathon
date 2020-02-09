import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from boto3.session import Session
from chalice import Chalice
from chalice import WebsocketDisconnectedError
# import .database_handler as dh
import os
from chalicelib.database_handler import  DynamoStorage

app = Chalice(app_name='test-websockets')
app.experimental_feature_flags.update([
    'WEBSOCKETS',
])
app.websocket_api.session = Session()

# dynamo_handler = dh.DynamoStorage(os.environ.get('CONNECTIONS_TABLE', ''), os.environ.get('RECORDS_TABLE', ''))

dynamo_handler = DynamoStorage("WSPlaygroundConnections", "WSPlaygroundRecords")



@app.on_ws_connect()
def connect(event):
    dynamo_handler.store_connection(event.connection_id)


@app.on_ws_message()
def message(event):
    try:
        dynamo_handler.store_record(event.connection_id, event.body)
        app.websocket_api.send(
            connection_id=event.connection_id,
            message="Record has been stored",
        )
    except WebsocketDisconnectedError as e:
        dynamo_handler.delete_connection(event.connection_id)


@app.on_ws_disconnect()
def disconnect(event):
    dynamo_handler.delete_connection(event.connection_id)
