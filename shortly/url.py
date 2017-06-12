from shortly.ddb import get, put
from shortly.settings import SHORT_BASE_URL
from shortly.utils import generate_id


def _new_id():
    tmp = True
    while tmp:
        tmpid = generate_id()
        tmp = get(tmpid)
    return tmpid


def lookup(url):
    """input: url
        - find id for url
        - return id or False
    """


def retrieve(id):
    """input: id
        - find url for id
        - forward request to url
        - 404 if id is not found
    """
    obj = get(id)
    if obj:
        return 'FORWARDING TO {}'.format(obj['url'])
    return '404'


def create(url):
    """input: url
        - generate id
        - ensure uniqueness
        - validate url
        - store id & url in ddb
        - return short url
    """
    obj = put(_new_id(), url)
    return SHORT_BASE_URL + obj['id']
