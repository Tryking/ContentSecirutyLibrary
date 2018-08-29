import pymongo

from .Config import *
from .common import *


class DbMonitor:
    def __init__(self):
        host = MONGODB_HOST
        port = MONGODB_PORT
        user = MONGODB_USER
        pwd = MONGODB_PWD
        db_name = MONGODB_DBNAME

        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client[db_name]
        if user and user != '':
            self.db.authenticate(name=user, password=pwd)

    def save_image(self, image_info):
        self.db['image'].update_one(filter={'path': image_info['path']},
                                    update={'$set': {'upload_date': get_before_date(before_day=0),
                                                     'upload_time': get_udpate_time(),
                                                     'update_time': get_udpate_time()}},
                                    upsert=True)

    def update_image(self, file_path, cost, porn, sexy, normal):
        """
        更新图像的结果值
        """
        self.db['image'].update_one(filter={'path': file_path},
                                    update={'$set': {'porn': porn, 'sexy': sexy, 'normal': normal, 'cost': cost, 'update_time': get_udpate_time()}}
                                    )
