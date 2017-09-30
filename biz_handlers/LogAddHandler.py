# coding=utf-8
import re
import json
import logging

import tornado.web
from mylog.mylogger import my_logger


class LogAddHandler(tornado.web.RequestHandler):
    tuple_reg = re.compile("^\([^\(\)]*\)$")
    float_reg = re.compile("^\d*\.\d+$")
    int_reg = re.compile("^\d+$")

    def _extract(self, string):
        '''
        由于通过request.arguments的值join起来的仍然是个字符串，这里我们需要将其转化为Python对象
        通过分析，我们可以知道这个对象只能是tuple、float和int
        简单的来说，这个地方可以使用eval方法，但是通常情况下，"eval is evil"
        所以这里通过正则的方法进行解析
        '''
        if self.tuple_reg.match(string):
            # 这里用json.loads来加载一个JS的数组方式来解析Python元组，将前后的括号专为方括号
            # JS里的None为null，这样得到一个Python list，再转化为元组
            return tuple(json.loads('[%s]' % string[1: -1].replace('None', 'null')))
        elif self.float_reg.match(string):
            return float(string)
        elif self.int_reg.match(string):
            return int(string)
        return string

    def post(self):
        '''
        原始的self.request.arguments如下：
        import pprint
        original_args = dict(
            [(k, v) for (k, v) in self.request.arguments.iteritems()]
        )
        pprint.pprint(original_args)

        {'args': ['()'],
         'created': ['1506738449.32'],
         'exc_info': ['None'],
         'exc_text': ['None'],
         'filename': ['GetUserProfileFromThird.py'],
         'funcName': ['run'],
         'levelname': ['ERROR'],
         'levelno': ['40'],
         'lineno': ['78'],
         'module': ['GetUserProfileFromThird'],
         'msecs': ['315.39106369'],
         'msg': ["['x1', 'yyy']"],
         'name': ['monitor'],
         'pathname': ['/Users/ouyang/PycharmProjects/myApp/biz_handlers/third_party/GetUserProfileFromThird.py'],
         'process': ['98843'],
         'processName': ['MainProcess'],
         'relativeCreated': ['57897774.2171'],
         'thread': ['140736844747712'],
         'threadName': ['MainThread']
         }

        '''

        args = dict(
            [(k, self._extract(''.join(v))) for (k, v) in self.request.arguments.iteritems()]
        )
        '''
        import pprint
        pprint.pprint(args)
        结果：
        {
            'threadName': 'MainThread',
            'name': 'monitor',
            'thread': 140736060957632,
            'created': 1506739312.87,
            'process': 1520,
            'args': (),
            'msecs': 872.350931168,
            'filename': 'GetUserProfileFromThird.py',
            'levelno': 40,
            'processName': 'MainProcess',
            'lineno': 78,
            'pathname': '/Users/ouyang/PycharmProjects/myApp/biz_handlers/third_party/GetUserProfileFromThird.py',
            'module': 'GetUserProfileFromThird',
            'exc_text': 'None',
            'exc_info': 'None',
            'funcName': 'run',
            'relativeCreated': 259876.040936,
            'levelname': 'ERROR',
            'msg': "['x1', 'yyy']"
        }
        '''

        '''
        因为和client端约定好，他们那边用如下格式传递过来
            from logclient import client_logger
            logs = ["x1","yyy"]
            client_logger.error(logs)
        所以这边要先还原msg_lst = ['x1', 'yyy']
        '''
        msg_lst = args['msg'].replace('[', '').replace(']', '').replace('\'', '').split(',')
        msg_lst = [v.strip() for v in msg_lst]

        '''
        替换'None'为None，否则会引发如下日志：
        2017-09-30 11:09:10,625 - GetUserProfileFromThird.run.78 - ERROR - x1
        None
        2017-09-30 11:09:10,625 - GetUserProfileFromThird.run.78 - ERROR - yyy
        None
        '''
        for key, value in args.iteritems():
            if value == 'None':
                args[key] = None

        for msg in msg_lst:
            # 每一次只写msg_lst中的一条记录
            args['msg'] = msg

            #import pdb
            #pdb.set_trace()

            # makeLogRecord接受一个字典作为参数
            record = logging.makeLogRecord(args)
            my_logger.handle(record)