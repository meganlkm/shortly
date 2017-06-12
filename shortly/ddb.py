from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from shortly.settings import TABLE_NAME
from shortly.utils import get_client


def get_table():
    return get_client('dynamodb').Table(TABLE_NAME)


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
    item = {'id': id, 'url': url}
    try:
        table.put_item(Item=item)
        return item
    except ClientError:
        raise
