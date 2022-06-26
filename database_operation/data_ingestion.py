import logging
import os
import sys
import argparse 
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from database_operation.mongo_operation import MongodbOperations
from src.utils.common import read_config
from log.logger import Logger
import json

class insertdata:

    try:

        def __init__(self, record, config_path):

            self.record = record
            self.config = read_config(config_path)
            self.log_obj = Logger('Generatedlogs')
            self.logger = self.log_obj.logging()
            self.db_ops = MongodbOperations(self.config['database']['username'], self.config['database']['pwd'])
            
        def check_duplicate(self):

            try:
                self.logger.info('Started checking for duplicates')
                if self.db_ops.CheckCollectionExistence(self.config['database']['db_name'], self.config['database']['collection']):
                    query = { 'number': self.record['number'] }
                    exist = self.db_ops.FindOneRecord(self.config['database']['db_name'], self.config['database']['collection'], query)
                    if exist:
                        self.message = 5
                        return self.message
                    else:
                        self.message = 3
                        return self.message

            except Exception as e:
                self.logger.error('Error while checking for duplicates: ' + str(e))
                sys.exit(1)

        def insert(self):
            try:
                self.logger.info('started inserting data')
                if self.message == 3:
                    self.db_ops.InsertOneRecord(self.config['database']['db_name'], self.record, self.config['database']['collection'])    

            except Exception as e:
                self.logger.error('Error while inserting the data: ' + str(e))
                sys.exit(1)

    except Exception as e:
        self.logger.error('Error while data ingestion: ' + str(e))
        sys.exit(1)


