import boto3

from shortly.settings import TABLE_NAME


ddb = boto3.resource('dynamodb')

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

# Print out some data about the table.
print(table.item_count)
