import os

from .Config import *
from .common import *
import paramiko


class SFTP:
    def __init__(self):
        self.module = self.__class__.__name__
        self.sftp = None
        self.handle = None

    def get_connection(self):
        """
        获取连接
        :return:
        """
        if not self.sftp:
            try:
                self.handle = paramiko.Transport((SFTP_HOST, SFTP_PORT))
                self.handle.connect(username=SFTP_USER, password=SFTP_PWD)
                self.sftp = paramiko.SFTPClient.from_transport(self.handle)
                self.debug("connection success")
            except Exception as e:
                self.sftp = None
                self.error("connection fail, reason:{0}".format(e))
        return self.sftp

    def close_connection(self):
        if self.handle:
            self.debug('STFP关闭')
            self.handle.close()

    def upload_file(self, remote_dir, local_paths):
        """
        传送文件
        :param sftp:
        :param remote_dir:
        :param local_paths:
        :return:
        """
        if self.get_connection():
            try:
                # 是否需要建立目录
                try:
                    self.sftp.chdir(remote_dir)
                except Exception as e:
                    self.error(str(e), get_current_func_name())
                    self.sftp.mkdir(remote_dir)
                for local_path in local_paths:
                    local_path = os.path.join(os.path.abspath('.'), local_path)
                    file_name = os.path.basename(local_path)
                    remote_path = os.path.join(remote_dir, file_name)
                    self.sftp.put(local_path, remote_path)
                    self.debug('文件上传成功：%s' % remote_path)
                self.close_connection()
                return True
            except Exception as e:
                self.error(str(e), get_current_func_name())
                return False

    @staticmethod
    def write_file_log(msg, module='', level='error'):
        filename = os.path.split(__file__)[1]
        if level == 'debug':
            logging.getLogger().debug('File:' + filename + ', ' + module + ': ' + msg)
        elif level == 'warning':
            logging.getLogger().warning('File:' + filename + ', ' + module + ': ' + msg)
        else:
            logging.getLogger().error('File:' + filename + ', ' + module + ': ' + msg)

    # 调试日志
    def debug(self, msg, func_name=''):
        module = "%s.%s" % (self.module, func_name)
        self.write_file_log(msg, module, 'debug')

    # 错误日志
    def error(self, msg, func_time=''):
        module = "%s.%s" % (self.module, func_time)
        self.write_file_log(msg, module, 'error')
