import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from boto3.session import Session
from chalice import Chalice
from chalice import WebsocketDisconnectedError, Response
# import .database_handler as dh
import os
from chalicelib.database_handler import  DynamoStorage

app = Chalice(app_name='test-websockets')
app.experimental_feature_flags.update([
    'WEBSOCKETS',
])
app.websocket_api.session = Session()

# dynamo_handler = dh.DynamoStorage(os.environ.get('CONNECTIONS_TABLE', ''), os.environ.get('RECORDS_TABLE', ''))

dynamo_handler = DynamoStorage("ws-cpm-guildathon-WSPlaygroundConnectionsB3497657-N5E0FPEH7XZM", "ws-cpm-guildathon-WSPlaygroundRecords99A7CB0F-1687NPRAAHO57")

records_table_name = os.environ.get('RECORDS_TABLE_NAME')
connections_table_name = os.environ.get('CONNECTIONS_TABLE_NAME')


@app.on_ws_connect()
def connect(event):
    dynamo_handler.store_connection(event.connection_id)


@app._create_registration_function(handler_type="on_ws_message", name=None, registration_kwargs={'route_key': 'test'})
def message(event):
    try:
        dynamo_handler.store_record(event.connection_id, event.body)
        app.websocket_api.send(
            connection_id=event.connection_id,
            message="Record has been sent",
        )

        list_conn = dynamo_handler.list_connections()

        for conn in list_conn:
            if (event.connection_id != conn['connection_id']):
                app.websocket_api.send(
                    connection_id=conn['connection_id'],
                    message=f'Push notification ==> {event.body}',
                )

    except WebsocketDisconnectedError as e:
        dynamo_handler.delete_connection(event.connection_id)


@app.route('/list', methods=['GET'])
def list_connections():
    list_conn = dynamo_handler.list_connections()

    return Response(body=list_conn, status_code=200)


@app.on_ws_disconnect()
def disconnect(event):
    dynamo_handler.delete_connection(event.connection_id)
