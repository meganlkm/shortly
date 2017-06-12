import os

from shortly.settings import API_NAME, ROLE_NAME, TABLE_NAME
from shortly.utils import get_client

BASEDIR = os.path.dirname(os.path.abspath(__file__))
VERSION = open(os.path.join(BASEDIR, 'VERSION')).read().strip()

lam = get_client('lambda', 'client')


# DynamoDB --------------------------------------
print('-' * 60)
print('DynamoDB:')

ddb = get_client('dynamodb')


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

print(ddb.meta.client.describe_table(TableName=TABLE_NAME))


# APIGateway ------------------------------------
print('-' * 60)
print('APIGateway:')

apig = get_client('apigateway', 'client')


def get_api():
    apis = apig.get_rest_apis()
    for api in apis.get('items', []):
        if api.get('name') == API_NAME:
            return api
    return False


if not get_api():
    response = apig.create_rest_api(
        name=API_NAME,
        description='A simple URL shortening service.',
        version=VERSION
    )

print(get_api())


# IAM -------------------------------------------
print('-' * 60)
print('IAM:')

iam = get_client('iam', 'client')


def get_role():
    for role in iam.list_roles().get('Roles'):
        if role['RoleName'] == ROLE_NAME:
            return role
    return False


iam_role = get_role()
if not iam_role:
    response = iam.create_role(
        RoleName=ROLE_NAME,
        AssumeRolePolicyDocument='{"Version": "2012-10-17","Statement":[{"Action":"sts:AssumeRole","Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"}}]}'
    )
    iam_role = response.get('Role')

print(iam_role)


# Lambda ----------------------------------------
print('-' * 60)
print('Lambda:')
response = lam.create_function(
    FunctionName='shortly-create',
    Runtime='python2.7',
    Role=iam_role.get('Arn'),
    Handler='shortly.create',
    Code={
        'S3Bucket': 'ds.io-builds',
        'S3Key': 'shortly/v0.0.1.zip'
    },
    Description='Create a url alias',
    Timeout=30,
    MemorySize=128,
    Publish=True
)

print(response)
