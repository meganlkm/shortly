from botocore.exceptions import ClientError

from shortly.utils import get_client


def get_table():
    ddb = get_client('dynamodb', 'resource')
    return ddb.Table('shortly-urls')


def lookup(url):
    """input: url
        - find id for url
        - return id or False
    """


def get(id):
    """input: id
        - find url for id
        - return url or False
    """
    table = get_table()
    print(table.item_count)


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
