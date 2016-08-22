from ots2 import OTSClient
from hwserver.config import OTS


class HomeworkHelper(object):
    def __init__(self):
        self.ots_client = OTSClient(OTS['instance_endpoint'],
                                    OTS['access_key_id'],
                                    OTS['access_key_secret'],
                                    'homework',
                                    logger_name='table_store.log')

    def list_table(self):
        print self.ots_client.list_table()



