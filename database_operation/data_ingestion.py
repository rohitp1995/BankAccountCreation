import logging
import os
import sys
import argparse 
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from database_operation.mongo_operation import MongodbOperations
from src.utils.common import read_config
import json

class insertdata:

    def __init__(self, record, config_path):

        self.record = record
        self.config = read_config(config_path)
        self.db_ops = MongodbOperations(self.config['database']['username'], self.config['database']['pwd'])
        
    def check_duplicate_and_insert(self):

        try:
            if self.db_ops.CheckCollectionExistence(self.config['database']['db_name'], self.config['database']['collection']):
                query = { 'number': self.record['number'] }
                exist = self.db_ops.FindOneRecord(self.config['database']['db_name'], self.config['database']['collection'], query)
                if exist:
                    message = 5
                    return message
                else:
                    message = 3
                    self.db_ops.InsertOneRecord(self.config['database']['db_name'], self.record, self.config['database']['collection'])    
                    return message

        except Exception as e:
            self.logger.error('Error while inserting the data: ' + str(e))
            sys.exit(1)
     

