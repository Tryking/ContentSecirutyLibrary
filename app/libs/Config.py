import logging
import os

DATA_SAVE_DIR = 'datas'
# 线程池大小
TASK_THREAD_POOL_SIZE = 5

LOG_TYPE = logging.DEBUG

# Mongo配置
MONGODB_HOST = '172.30.140.252'
# MONGODB 端口号
MONGODB_PORT = 27017
# 数据库名称
MONGODB_DBNAME = 'content_security_test'
MONGODB_USER = ''
MONGODB_PWD = ''

# 现网部署修改
# REMOTE_SFTP_PATH = os.path.join('tmp', 'identify_images')
REMOTE_SFTP_PATH = '/tmp/identify_images'
SFTP_HOST = '172.30.140.251'
SFTP_PORT = 22
TIMEOUT = 30
SFTP_USER = 'root'
SFTP_PWD = 'zaqwsx'

GPU_URL = 'http://www.baidu.com'
