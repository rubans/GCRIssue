import glob, os, sys, io, re
import json
import tempfile, datetime
import time
import msal, base64
from modules import common_helper
from modules.aad_helper import aad_helper
from modules.prisma_helper import prisma_helper
from modules.logging_helper import request_logging_helper
from flask import Flask, request
from werkzeug.exceptions import HTTPException, default_exceptions

def handle_error(e):
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.content_type = "application/json"
    response.data = json.dumps({
        "error": {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    })
    print("e:",e.__dict__)
    # if hasattr(e,original_exception):
    try:
        origExceptionMessage = e.original_exception
        logger.error("App Exception Thrown !/n Message: %s",origExceptionMessage)
    except AttributeError:
         logger.error("App Exception Thrown !/n %s",e.__dict__)
    logger.exception("Exception Detail")
    return response

# init app
logger = request_logging_helper().get_logger()
app = Flask(__name__)
for exc in default_exceptions:
    app.register_error_handler(exc, handle_error)

@app.route("/test",methods = ['POST', 'GET'])
def test_app():
    delay = request.args.get('delay')
    if not delay is None:
        logger.info.debug("using delay of :"+delay)
        time.sleep(int(delay))
        logger.info.debug("finished delay!")
    logger.info("request test endpoint!")
    return "Test of main endpoint ok\n"

# Delete this method
@app.route("/debug",methods = ['POST', 'GET'])
def debug_app():
    logger.debug("in debug app")
    prismaContext = common_helper.createPrismaContext(prisma_helper.PrismaContext)
    common_helper.setHttpProxy()  
    _prisma_helper = prisma_helper(context=prismaContext)
    return "", 201
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)