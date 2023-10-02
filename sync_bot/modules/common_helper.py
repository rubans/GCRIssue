import json
import os
from . import common_helper
from .logging_helper import request_logging_helper
# define constants
temp_folder = "temp/"
aad_user_data_file = temp_folder + "prepuserdata.json"
aad_role_data_file = temp_folder + "preproledata.json"
prisma_role_data_file = temp_folder + "prisma_id.json"  

logger = request_logging_helper().get_logger()

def setHttpProxy():
    if "DEFAULT_PROXY_URL" in os.environ:
        logger.debug("set proxy...")
        os.environ['http_proxy'] = os.environ['DEFAULT_PROXY_URL']
        os.environ['https_proxy'] = os.environ['DEFAULT_PROXY_URL']


def writedata(data,name):
    with open(name, "w+") as f:
        f.seek(0)
        json.dump(data, f, indent=2)

def jsdecode(filename):
    with open(filename, 'rb') as open_file:
        byte_content = open_file.read()
    base64_bytes = base64.b64decode(byte_content)
    test = json.loads(base64_bytes)
    return json.dumps(test, indent=2)

def decode(filename):
    with open(filename, 'rb') as open_file:
        byte_content = open_file.read()
    base64_bytes = base64.b64decode(byte_content)
    return base64_bytes

def createAADContext(createContextFunction):
    aadContext = createContextFunction()
    aadContext.base_url = os.environ.get('AAD_URL')
    aadContext.authority = os.environ.get('AAD_AUTHORITY')
    aadContext.client_id = json.loads(os.environ.get('AAD_CREDENTIAL')).get('AAD_CLIENT_ID') if os.environ.get('AAD_CREDENTIAL') else ''
    aadContext.private_key = json.loads(os.environ.get('AAD_CREDENTIAL')).get('AAD_PRIVATE_KEY') if os.environ.get('AAD_CREDENTIAL') else ''
    return aadContext

def createPrismaContext(createContextFunction):
    prismaContext = createContextFunction()
    prismaContext.base_url = os.environ.get('PRISMA_URL','')
    prismaContext.user = json.loads(os.environ.get('PRISMA_CREDENTIAL')).get('PRISMA_USER_NAME') if os.environ.get('PRISMA_CREDENTIAL') else ''
    prismaContext.token = json.loads(os.environ.get('PRISMA_CREDENTIAL')).get('PRISMA_TOKEN') if os.environ.get('PRISMA_CREDENTIAL') else ''
    return prismaContext