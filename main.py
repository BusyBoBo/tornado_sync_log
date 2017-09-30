# coding=utf-8
import os
import time
import signal

import tornado.web
import tornado.ioloop
import tornado.httpserver
from mylog.mylogger import my_logger

from util.options import define, options
from biz_handlers.LogAddHandler import LogAddHandler


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            login_url="/backend/login/",
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            compiled_template_cache=False,
        )

        # URL Mapping
        handlers = [
            (r"/log/", LogAddHandler),
        ]

        def write_error(self, stat, **kw):
            self.write('!!!!Something is wrong!!!!')

        tornado.web.RequestHandler.write_error = write_error

        # Init
        super(Application, self).__init__(handlers, **app_settings)


def main():
    # 配置main.py的命令
    define("port", default=None, help="Run server on a specific port, mast input",
           type=int)

    # start from cmd
    options.parse_command_line()
    try:
        if options.port == None:
            options.print_help()
            return
    except:
        print 'Usage: python main.py --port=8000'
        return

    # 信号监听
    def sig_handler(sig, frame):
        my_logger.warning('Caught signal: %s', sig)
        tornado.ioloop.IOLoop.instance().add_callback(shutdown)

    # 关闭服务器
    def shutdown():
        my_logger.info('Stopping http server')
        http_server.stop()

        io_loop = tornado.ioloop.IOLoop.instance()

        deadline = time.time() + 1

        def stop_loop():
            now = time.time()
            if now < deadline and (io_loop._callbacks or io_loop._timeouts):
                io_loop.add_timeout(now + 1, stop_loop)
            else:
                io_loop.stop()
                my_logger.info('Shutdown')

        stop_loop()

    global http_server
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    # 按Ctrl+C退出程序
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    # start server
    tornado.ioloop.IOLoop.instance().start()
    my_logger.info('Exit Master')


if __name__ == '__main__':
    main()
