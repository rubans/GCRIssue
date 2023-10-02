import glob, os, sys, io, re
import requests
import json
from .logging_helper import request_logging_helper

class prisma_helper:
    class PrismaContext:
        base_url = ""
        user = ""
        token = ""
        authorized_header = ""

    class ProcessSummary:
        def __init__(self):
            self.noOfUsersCreated = 0
            self.noOfUsersRemoved = 0
            self.NoOfUsersRolesUpdated = 0
            self.noOfUsersRolesRemoved = 0

    def __init__(self, context, dryRunOnly=False):
        self.context = context
        self.dryRunOnly = dryRunOnly
        self.summary = self.ProcessSummary()
        self.logger = request_logging_helper().get_logger()
        self.init()

    def init(self):
        # Full URL
        if self.context.base_url == "":
            self.logger.warning("base_url not set!")
            return
        
        if self.dryRunOnly:
            self.logger.warning("DRY RUN ONLY - PRISMA Will not be updated !")
        self.login()
    
    def login(self):
        login_url = self.context.base_url + '/login'
        try:
            self.logger.debug("Attempt PRISMA login...")
            response = requests.post(
                    url=login_url,
                    data=json.dumps({"username": self.context.user, "password": self.context.token}),
                        headers={
                            'Content-Type': 'application/json;charset=UTF-8',
                            'Accept': 'application/json;charset=UTF-8'
                        })
            if not response.ok:
                self.logger.error("error:"+response.text)
                raise RuntimeError('Error!','Unable to login to PRISMA.') 
        except Exception as e:
            raise RuntimeError("An error while trying to login.\nOriginal Exception:%s",e) from e  

        auth_token = response.json()['token']
        self.authorized_header = {
            "accept": "application/json; charset=UTF-8",
            "content-type": "application/json; charset=UTF-8",
            "x-redlock-auth": auth_token
        }