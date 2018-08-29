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

    def list_data(self, page_size, page_number):
        """
        按照页数和每页数量查找数据
        :param page_size:
        :param page_number:
        :return:
        """
        result = self.db['image'].find({}).sort([('upload_time', pymongo.DESCENDING)]).skip((page_number - 1) * page_size).limit(page_size)
        result = list(result)
        for data in result:
            del data['_id']
        return result

    def count(self):
        """
        获取总数
        :return:
        """
        count = self.db['image'].find().count()
        return count
