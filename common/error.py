DECRYPTION_ERROR = {
    'code': 'DECRYPTION_ERROR',
    'status': '400',
    'message': 'Decryption Error'
}

ENCRYPTION_NOT_ENABLED = {
    'code': 'ENCRYPTION_NOT_ENABLED',
    'status': '400',
    'message': 'Encrypted data found on the request body but encryption is not enabled'
}

ENCRYPTION_ENABLED = {
    'code': 'ENCRYPTION_ENABLED',
    'status': '400',
    'message': 'Encryption is enabled but no encrypted data found on the request body'
}


INVALID_PARAMETERS = {
    'code': 'INVALID_PARAMETERS',
    'status': '400',
    'message': 'Invalid Parameters'
}

INTERNAL_SERVER_ERROR = {
    'code': 'INTERNAL_SERVER_ERROR',
    'status': '500',
    'message': 'Internal Server Error'
}