# coding=utf-8
import os
import sys
import logging


# 创建一个全局的logger
def get_logger():
    print '#########Create a global logger#########'
    logger = logging.getLogger('server_logger')
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'my.log')
    handler = logging.FileHandler(filename)
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.ERROR)

    '''
    # logger.propagate = False 不要传递到父亲的参数
    # 默认为True，如果为True，那么root这个logger也会收到。到时候在控制台就会打印：
    2017-09-30 11:26:22,493-monitor-GetUserProfileFromThird.run.78 - ERROR - x1
    ERROR:monitor:x1
    2017-09-30 11:26:22,493-monitor-GetUserProfileFromThird.run.78 - ERROR - yyy
    ERROR:monitor:yyy

    控制代码在：logging的Logger类中1318行的callHandlers()：
        def callHandlers(self, record):
            """
            如果propagate=True，则会进去else分支，c = c.parent一直回溯到root，
            root也会打印到streamHandler控制台，导致重复输出。
            """
            c = self
            found = 0
            while c:
                for hdlr in c.handlers:
                    found = found + 1
                    if record.levelno >= hdlr.level:
                        hdlr.handle(record)
                if not c.propagate:
                    c = None    #break out
                else:
                    c = c.parent
            if (found == 0) and raiseExceptions and not self.manager.emittedNoHandlerWarning:
                sys.stderr.write("No handlers could be found for logger"
                                 " \"%s\"\n" % self.name)
                self.manager.emittedNoHandlerWarning = 1
    '''
    logger.propagate = False


    logger.addHandler(handler)

    # 同时输到屏幕，便于实施观察
    handle_for_screen = logging.StreamHandler(sys.stdout)
    handle_for_screen.setFormatter(formatter)
    logger.addHandler(handle_for_screen)
    return logger

my_logger = get_logger()

