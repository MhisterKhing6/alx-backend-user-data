#!/usr/bin/env python3
""" 
Logging in python obsecuring specific user data input
"""
import logging
import re
from mysql import connector
from typing import List
import os

PID_FIELDS = ("name", "ssn", "phone", "ip", "email")


def filter_datum(fields : List[str], redaction : str, message : str, seperator : str) -> str:
    """ Obsecure specific fields in message"""
    for field in fields:
        message = re.sub(r'(?<={}=).+?(?={})'.format(field, seperator), redaction, message)
    return message

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields = []):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields



    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        

def get_logger() -> logging.Logger:
    """Get a logger """
    user_data = logging.getLogger("user_data")
    StreamHandler = logging.StreamHandler()
    user_data.setLevel(logging.INFO)
    StreamHandler.setFormatter(RedactingFormatter.FORMAT)
    user_data.propagate = False
    user_data.addHandler(StreamHandler)
    return user_data

def get_connetor() -> connector:
    """ Connect to a secure database """
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    user = os.environ.get('PERSONAL_DATA_DB_USERNAME')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD')
    host = os.environ.get('PERSONAL_DATA_DB_HOST')
    return connector.connect(database=db_name, user=user, 
                            password=password, host=host)

def main() -> None:
    """ main code that obsecure certain fields"""
    form = '[Holberton] %(name)s %(levelname)s %(asctime)s: %(message)s'
    hanler = get_logger()
    db = get_connetor().cursor()
    query =('SELECT * from users')
    result = db.execute(query)

    for (name, email, phone, ssn, ip,last_login, user_agent) in result:
        message = 'name={}; email={}; phone={}; \
         ssn={}; password={}; ip={}; last_login={}; user_agent={};'.format(
            name, email, phone, ssn, ip, last_login, user_agent
         )
        log_record = logging.LogRecord("user_data", logging.INFO, None, None, message, None, None)
        RedactingFormatter(['email', 'phone', 'password', 'ssn', 'name']).format(log_record)
