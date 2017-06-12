import boto3


def get_client(service_name, client_type='client', region='us-east-1'):
    fn = getattr(boto3, client_type)
    return fn(service_name, region_name=region)
