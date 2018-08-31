import logging
import os

DATA_SAVE_DIR = 'app/static/images'
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
SFTP_HOST_11 = '10.167.64.11'
SFTP_PORT_11 = 22
TIMEOUT_11 = 30
SFTP_USER_11 = 'root'
SFTP_PWD_11 = 'r00tme11'

SFTP_HOST_10 = '10.167.64.10'
SFTP_PORT_10 = 22
TIMEOUT_10 = 30
SFTP_USER_10 = 'ironic'
SFTP_PWD_10 = 'r00tme10'

# PORN_URL = 'http://10.167.64.11:8080/resnet/predict'
PORN_URL = 'http://10.167.64.11:5000/detect_porn?data=%s'
POLITICS_URL = 'http://10.167.64.10:5000/detect?data=%s'
TEXT_CHECK_URL = 'http://10.167.64.33:8888/lookfor?cont=%s'
