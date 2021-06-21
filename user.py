import json
from faker import Faker
import secrets
from tgtg import TgtgClient
from tgtg import TgtgAPIError
from utils import print_api_error, log

def write_user(login, password):
    data = {}
    data['login']=login
    data['password']=password
    with open('credentials','w') as outfile:
        json.dump(data, outfile)
    
def read_user():
    with open('credentials','r') as infile:
        data = json.load(infile)
        return TgtgClient(email=data['login'], password=data['password'])

def create_account(debug):
    faker = Faker()
    #safe_email generates emails with fake domains
    mail = faker.ascii_safe_email()
    full_name = faker.name()
    passwd = secrets.token_hex(16)

    try :
        client = TgtgClient(email=mail, password=passwd)
        new_client = client.signup_by_email(email=mail, password=passwd, name=full_name)
    except TgtgAPIError as err:
        print_api_error(err)
        return None
    attrs = vars(new_client)
    log(', '.join("%s: %s" % item for item in attrs.items()), debug)
    write_user(mail,passwd)
    return client