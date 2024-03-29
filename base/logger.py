import os, logging, sys
from datetime import datetime
from .settings import env, BASE_DIR

# logging configuration


logging_environment = env('LOGGING', default='STREAM_HANDLER')
if logging_environment == 'FILE_HANDLER':
    LOGS_DIR = os.path.join(BASE_DIR, 'logs/')
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
        print("Log directory created.")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'info': {
            'format': "[%(asctime)s] => | LOG STATUS - %(levelname)-5s"
                      " | METHOD - %(method)-4s"
                      " | URL - %(url)s"
                      " | MESSAGE - %(message)s"
                      " |"
        },
        'request': {
            'format': "[%(asctime)s] => | LOG STATUS - %(levelname)-5s"
                      " | STATUS - %(status)-7s"
                      " | METHOD - %(method)-4s"
                      " | FETCH_URL - %(url)s"
                      " | REQUEST_DATA - %(request_data)s"
                      " | USER - %(user)s"
                      " | RESPONSE - %(response_data)s"
                      " | MESSAGE - %(message)s"
                      " |"
        },
        'error': {
            'format': "[%(asctime)s] => | LOG STATUS - %(levelname)-5s"
                      " | METHOD - %(method)-4s"
                      " | FETCH_URL - %(url)s"
                      " | REQUEST_DATA - %(request_data)s"
                      " | USER - %(user)s"
                      " | MESSAGE - %(message)s"
                      " | TYPE - %(exc_type)s"
                      " | FILE_NAME - %(exc_file_name)s"
                      " | LINE_NO - %(exc_line_no)s"
                      " |"
        },
    },
    'handlers': {},
    'loggers': {
        'info': {
            'level': 'INFO',
            'handlers': ['info']
        },
        'request': {
            'level': 'INFO',
            'handlers': ['request']
        },
        'error': {
            'level': 'ERROR',
            'handlers': ['error']

        }
    }
}

if logging_environment == 'FILE_HANDLER':
    LOGGING['handlers']['info'] = {
        'formatter': 'info',
        'class': 'logging.FileHandler',
        'filename': str(LOGS_DIR) + 'info_log__{}.log'.format(datetime.now().strftime("%Y_%m_%d")),
    }
    LOGGING['handlers']['request'] = {
        'formatter': 'request',
        'class': 'logging.FileHandler',
        'filename': str(LOGS_DIR) + 'request_log__{}.log'.format(datetime.now().strftime("%Y_%m_%d")),
    }
    LOGGING['handlers']['error'] = {
        'formatter': 'error',
        'class': 'logging.FileHandler',
        'filename': str(LOGS_DIR) + 'error_log__{}.log'.format(datetime.now().strftime("%Y_%m_%d")),
    }

elif logging_environment == 'STREAM_HANDLER':
    LOGGING['handlers']['info'] = {
        'class': 'logging.StreamHandler',
        'formatter': 'info',
    }
    LOGGING['handlers']['request'] = {
        'class': 'logging.StreamHandler',
        'formatter': 'request',
    }
    LOGGING['handlers']['error'] = {
        'class': 'logging.StreamHandler',
        'formatter': 'error',
    }

elif logging_environment == 'LOGSTASH_HANDLER':
    LOGGING['handlers']['info'] = {
        'class': 'logstash.TCPLogstashHandler',
        'host': env('LOGSTASH_HOST'),
        'port': env('LOGSTASH_PORT', default=5959),
        'formatter': 'error',
    }
    LOGGING['handlers']['request'] = {
        'class': 'logstash.TCPLogstashHandler',
        'host': env('LOGSTASH_HOST'),
        'port': env('LOGSTASH_PORT', default=5959),
        'formatter': 'request',
    }
    LOGGING['handlers']['error'] = {
        'class': 'logstash.TCPLogstashHandler',
        'host': env('LOGSTASH_HOST'),
        'port': env('LOGSTASH_PORT', default=5959),
        'formatter': 'error',
    }


info_logger = logging.getLogger('info')
error_logger = logging.getLogger('error')


def info_log(request, message: str) -> None:
    data = {
        'method': request.method,
        'url': request.path
    }
    info_logger.info(message, extra=data)


def error_log(request, message: str = None) -> None:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    data = {
        'method': request.method,
        'url': request.path,
        'request_data': request.data,
        'user': request.user,
        'exc_type': exc_type.__name__,
        'exc_file_name': exc_traceback.tb_frame.f_code.co_filename,
        'exc_line_no': exc_traceback.tb_lineno}
    if message:
        exc_value = message + ": " + str(exc_value)
    error_logger.error(exc_value, extra=data)
