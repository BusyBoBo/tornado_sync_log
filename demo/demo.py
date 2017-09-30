# coding=utf-8
import logging
import logging.handlers

logging_host = '127.0.0.1'
logging_port = 8888
logging_add_url = '/log/'


def get_logger():
    logger = logging.getLogger('monitor')
    http_handler = logging.handlers.HTTPHandler(
        '%s:%s' % (logging_host, logging_port),
        logging_add_url,
        method='POST'
    )
    http_handler.setLevel(logging.ERROR)
    logger.addHandler(http_handler)

    return logger

client_logger = get_logger()


def main():
    client_logger.error(['the first line', 'the second line...'])


if __name__ == '__main__':
    main()