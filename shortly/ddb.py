from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

from shortly.utils import get_client


def get_table():
    ddb = get_client('dynamodb', 'resource')
    return ddb.Table('shortly-urls')


def get(value, key='id'):
    """input: id
        - find url for id
        - return url or False
    """
    table = get_table()
    response = table.query(
        KeyConditionExpression=Key(key).eq(value)
    )
    try:
        return response['Items'][0]
    except IndexError:
        return False


def put(id, url):
    """Create a new url object."""
    table = get_table()
    try:
        table.put_item(
            Item={
                'id': id,
                'url': url
            }
        )
        return True
    except ClientError:
        raise
