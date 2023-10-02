import uuid
from datetime import datetime
import logging
import os
import flask

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class logging_helper():
    def __init__(self):
        self.logger = logging.getLogger( __class__.__name__)
        log_level = os.environ.get('LOG_LEVEL','WARNING').upper()
        self.logger.setLevel(log_level)
        sh = logging.StreamHandler()
        log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        sh.setFormatter(log_formatter)
        self.logger.addHandler(sh)
        self.logger.debug("initialise standard logger Name:"+ __class__.__name__)

    def get_logger(self):
        return self.logger

class request_logging_helper(metaclass=Singleton):
    
    def __init__(self):
        self.logger = logging.getLogger(__class__.__name__)
        self.logger.debug("initialise request logger Name:"+__class__.__name__)
        self.init()

    def init(self):
        logPath = ""
        fileName = '{:%Y-%m-%d}.log'.format(datetime.now())
        logLevel = os.environ.get('LOG_LEVEL','WARNING').upper()
        self.logger.setLevel(logLevel)

        # # Note: the "req_id" param name must be the same as in
        # # RequestIdFilter.filter
        logFormatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - ID: %(req_id)s - %(message).1000s"
        )

        # # logs in the console
        streamHandler = logging.StreamHandler()
        streamHandler.addFilter(self.RequestIdFilter(self))

        # log to file
        fileHandler = logging.FileHandler("{0}".format(fileName))
        
        streamHandler.setFormatter(logFormatter)
        fileHandler.setFormatter(logFormatter)
        self.logger.addHandler(streamHandler)
        self.logger.addHandler(fileHandler)

    def get_request_id(self):
        if getattr(flask.g, 'request_id', None):
            return flask.g.request_id

        new_uuid = uuid.uuid4().hex[:10]
        flask.g.request_id = new_uuid

        return new_uuid

    def get_logger(self):
        return self.logger

    class RequestIdFilter(logging.Filter):
        # This is a logging filter that makes the request ID available for use in
        # the logging format. Note that we're checking if we're in a request
        # context, as we may want to log things before Flask is fully loaded.
        def __init__(self, parent_instance):
            self.parent = parent_instance

        def filter(self, record):
            # try:
            record.req_id = self.parent.get_request_id() if flask != flask.has_request_context() else 'No Request Context Found'
            # except NameError:
            #     record.req_id = "NA"
            return True