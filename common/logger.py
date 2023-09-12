import os, logging, sys, json
from datetime import datetime
from environment import env, BASE_DIR

# logging configuration
LOGS = '/logs/'
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

logging_environment = env('LOGGING', default='file')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'info': {
            'format': "[%(asctime)s] => | LOG STATUS - %(levelname)s"
                      " | METHOD - %(method)-4s"
                      " | URL - %(url)s"
                      " | MESSAGE - %(message)s"
                      " |"
        },
        'success': {
            'format': "[%(asctime)s] => | LOG STATUS - %(levelname)s"
                      " | METHOD - %(method)-4s"
                      " | FETCH_URL - %(url)s"
                      " | REQUEST_DATA - %(request_data)s"
                      " | USER - %(user)s"
                      " | STATUS - %(status)s"
                      " | RESPONSE - %(response_data)s"
                      " | MESSAGE - %(message)s"
                      " |"
        },
        'error': {
            'format': "[%(asctime)s] => | LOG STATUS - %(levelname)s"
                      " | METHOD - %(method)s"
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
        'success': {
            'level': 'INFO',
            'handlers': ['success']
        },
        'error': {
            'level': 'ERROR',
            'handlers': ['error']

        }
    }
}

if logging_environment == 'file':
    LOGGING['handlers']['info'] = {
        'formatter': 'info',
        'class': 'logging.FileHandler',
        'filename': str(BASE_DIR) + LOGS + 'info_log_response__{}.log'.format(datetime.now().strftime("%Y_%m_%d")),
    }
    LOGGING['handlers']['success'] = {
        'formatter': 'success',
        'class': 'logging.FileHandler',
        'filename': str(
            BASE_DIR) + LOGS + 'success_log_response__{}.log'.format(datetime.now().strftime("%Y_%m_%d")),
    }
    LOGGING['handlers']['error'] = {
        'formatter': 'error',
        'class': 'logging.FileHandler',
        'filename': str(BASE_DIR) + LOGS + 'error_log_response__{}.log'.format(datetime.now().strftime("%Y_%m_%d")),
    }

elif logging_environment == 'streamHandler':
    LOGGING['handlers']['info'] = LOGGING['handlers']['success'] = LOGGING['handlers']['error'] = {
        'class': 'logging.StreamHandler'
    }

elif logging_environment == 'logstash':
    LOGGING['handlers']['info'] = LOGGING['handlers']['success'] = LOGGING['handlers']['error'] = {
        'class': 'logstash.TCPLogstashHandler',
        'host': 'logstash',
        'port': 5959,  # default : 5959
    }


info_logger = logging.getLogger('info')
error_logger = logging.getLogger('error')


def info_log(request, message) -> None:
    data = {
        'method': request.method,
        'url': request.path
    }
    info_logger.info(message, extra=data)


def error_log(request) -> None:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    data = {'method': request.method, 'url': request.path,
            'request_data': json.loads(request.body).get('data', None) if request.body else None,
            'user': request.user,
            'exc_type': exc_type.__name__,
            'exc_file_name': exc_traceback.tb_frame.f_code.co_filename,
            'exc_line_no': exc_traceback.tb_lineno}
    error_logger.error(exc_value, extra=data)
