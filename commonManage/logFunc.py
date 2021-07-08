import logging
import os
from time import strftime

class loggerConf():
    def __init__(self):
        #创建一个Logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)               #设置总日志级别

    def getLogger(self):
        if not self.logger.handlers:
            # 创建一个handler,用于输出到控制台
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.ERROR)  # 设置控制台输出日志级别

            # 定义handler的输出格式
            log_format = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

            # 获取当前py所在的父目录（不包括当前文件）
            fileParPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            logFileDir = os.path.join(fileParPath, "log")

            # 不存在目录则新建
            if not os.path.exists(logFileDir):
                os.mkdir('log')

            # logFile = '\debug' + strftime('%Y%m%d_%H%M%S') + '.log'
            logFile = '\debug' + '.log'
            logFileDir = logFileDir + logFile
            # 创建一个handler,用于将日志写入文件
            file_handler = logging.FileHandler(logFileDir, mode='a', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)  # 设置文件输出日志级别

            # 设置handler输出格式
            stream_handler.setFormatter(log_format)
            file_handler.setFormatter(log_format)

            # 给logger添加handler
            self.logger.addHandler(stream_handler)
            self.logger.addHandler(file_handler)

        return self.logger

