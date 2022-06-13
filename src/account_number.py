import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from database_operation.mongo_operation import MongodbOperations

class AccountNumber:

    try:

        def __init__(self, config_obj):

            self.config_obj = config_obj
            self.db_ops = MongodbOperations(self.config_obj['database']['username'], self.config_obj['database']['pwd'])

        def get_account_number(self):

            try:

                max_num = self.db_ops.getnextcount('bankaccount', 'acc_info', 'account_number')
                return max_num

            except Exception as e:
                self.logger.error('Error while getting max number: '+ str(e))
                sys.exit(1) 

    except Exception as e:
        self.logger.error('Error while getting account number: '+ str(e))
        sys.exit(1)


    