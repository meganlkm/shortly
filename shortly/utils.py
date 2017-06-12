from random import choice
from string import ascii_lowercase, ascii_uppercase, digits

import boto3

from shortly.settings import ID_LENGTH


def get_client(service_name, client_type='resource', region='us-east-1'):
    fn = getattr(boto3, client_type)
    return fn(service_name, region_name=region)


def generate_id():
    return ''.join(choice(ascii_lowercase + ascii_uppercase + digits) for _ in range(ID_LENGTH))
