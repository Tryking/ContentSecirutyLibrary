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

    def save_text_result(self, search_string, content):
        self.db['text'].insert_one({'search_string': search_string, 'result': content, 'upload_date': get_before_date(before_day=0),
                                    'upload_time': get_udpate_time(),
                                    'update_time': get_udpate_time()})

    def update_image_politics(self, file_path, cost, politics):
        """
        更新图像的涉政结果值
        """
        self.db['image'].update_one(filter={'path': file_path},
                                    update={
                                        '$set': {'politics': politics, 'politics_cost': cost, 'update_time': get_udpate_time(),
                                                 'has_identify': True}}
                                    )

    def update_image_porn(self, file_path, cost, porn, sexy, normal):
        """
        更新图像的鉴黄结果值
        """
        self.db['image'].update_one(filter={'path': file_path},
                                    update={
                                        '$set': {'porn': porn, 'sexy': sexy, 'normal': normal, 'porn_cost': cost, 'update_time': get_udpate_time(),
                                                 'has_identify': True}}
                                    )

    def update_image_porn_new(self, file_path, cost, porn):
        """
        更新图像的鉴黄结果值
        """
        self.db['image'].update_one(filter={'path': file_path},
                                    update={
                                        '$set': {'porn': porn, 'porn_cost': cost, 'update_time': get_udpate_time(),
                                                 'has_identify': True}}
                                    )

    def list_data(self, page_size, page_number):
        """
        按照页数和每页数量查找数据
        :param page_size:
        :param page_number:
        :return:
        """
        result = self.db['image'].find({'has_identify': True}).sort([('upload_time', pymongo.DESCENDING)]).skip(
            (page_number - 1) * page_size).limit(page_size)
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
