import os

from shortly.settings import API_NAME, TABLE_NAME
from shortly.utils import get_client

BASEDIR = os.path.dirname(os.path.abspath(__file__))
VERSION = open(os.path.join(BASEDIR, 'VERSION')).read().strip()

apig = get_client('apigateway', 'client')
ddb = get_client('dynamodb')


def get_api():
    apis = apig.get_rest_apis()
    for api in apis.get('items', []):
        if api.get('name') == API_NAME:
            return api
    return False


def table_exists():
    for table in ddb.tables.all():
        if table.name == TABLE_NAME:
            return True
    return False


if not table_exists():
    # create the table
    table = ddb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'url',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'url',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)


if not get_api():
    response = apig.create_rest_api(
        name=API_NAME,
        description='A simple URL shortening service.',
        version=VERSION
    )

print('-' * 60)
print('DynamoDB:')
print(ddb.meta.client.describe_table(TableName=TABLE_NAME))
print('-' * 60)
print('APIGateway:')
print(get_api())
