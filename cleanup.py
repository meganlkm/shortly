from shortly.settings import API_NAME, ROLE_NAME, TABLE_NAME
from shortly.utils import get_client


try:
    table = get_client('dynamodb').Table(TABLE_NAME)
    table.meta.client.delete_table(TableName=TABLE_NAME)
    table.meta.client.get_waiter('table_not_exists').wait(TableName=TABLE_NAME)
except:
    pass


apig = get_client('apigateway', 'client')

api = None
apis = apig.get_rest_apis()
for _ai in apis.get('items', []):
    if _ai.get('name') == API_NAME:
        api = _ai

if api:
    try:
        print(apig.delete_rest_api(restApiId=api['id']))
    except:
        pass


try:
    print(get_client('lambda', 'client').delete_function(FunctionName='shortly-create'))
except:
    pass


try:
    print(get_client('iam', 'client').delete_role(RoleName=ROLE_NAME))
except:
    pass
