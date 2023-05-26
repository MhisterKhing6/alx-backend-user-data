#!/usr/bin/env python3
""" 
Logging in python obsecuring specific user data input
"""
import logging
import re
from mysql import connector
from typing import List, Any
import os

PID_FIELDS = ("name", "ssn", "phone", "ip", "email")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Obsecure specific fields in message"""
    for field in fields:
        message = re.sub(r'(?<={}=).+?(?={})'.format(
            field, seperator),
         redaction, message)
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
        """Return a formatted string """
        return filter_datum(
            self.fields, self.REDACTION, record.getMessage(), 
            self.SEPARATOR)
        
def get_logger() -> logging.Logger:
    """
    Returns a Logger object for handling Personal Data

    Returns:
        A Logger object with INFO log level and RedactingFormatter
        formatter for filtering PII fields
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a MySQLConnection object for accessing Personal Data database

    Returns:
        A MySQLConnection object using connection details from
        environment variables
    """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    cnx = mysql.connector.connection.MySQLConnection(user=username,
                                                     password=password,
                                                     host=host,
                                                     database=db_name)
    return cnx



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
