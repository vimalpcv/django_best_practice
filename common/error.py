ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "code": {"type": "string", },
        "message": {"type": "string"},
        "detail": {"type": "string"}
    }
}

INTERNAL_SERVER_ERROR = {
    'status_code': '500',
    'error': {
        'code': 'INTERNAL_SERVER_ERROR',
        'message': 'Internal Server Error'
    }
}

INVALID_PARAMETERS = {
    'status_code': '400',
    'error': {
        'code': 'INVALID_PARAMETERS',
        'message': 'Invalid Parameters'
    }
}

# Error Codes for Cipher/Decipher
DECRYPTION_ERROR = {
    'status_code': '400',
    'error': {
        'code': 'DECRYPTION_ERROR',
        'message': 'Decryption Error'
    }
}

ENCRYPTION_NOT_ENABLED = {
    'status_code': '400',
    'error': {
        'code': 'ENCRYPTION_NOT_ENABLED',
        'message': 'Encrypted data found on the request body but encryption is not enabled'
    }
}

ENCRYPTION_ENABLED = {
    'status_code': '400',
    'error': {
        'code': 'ENCRYPTION_ENABLED',
        'message': 'Encryption is enabled but no encrypted data found on the request body'
    }
}

INVALID_REFRESH_TOKEN = {
    'status_code': '400',
    'error': {
        'code': 'INVALID_REFRESH_TOKEN',
        'message': 'Refresh Token is invalid or expired'
    }
}


USER_NOT_FOUND = {
    'status_code': '404',
    'error': {
        'code': 'USER_NOT_FOUND',
        'message': 'User not found'
    }
}

INVALID_PASSWORD = {
    'status_code': '400',
    'error': {
        'code': 'INVALID_PASSWORD',
        'message': 'Invalid Password'
    }
}

USER_INACTIVE = {
    'status_code': '400',
    'error': {
        'code': 'USER_INACTIVE',
        'message': 'User is inactive'
    }
}

ORGANIZATION_INACTIVE = {
    'status_code': '400',
    'error': {
        'code': 'ORGANIZATION_INACTIVE',
        'message': 'Organization is inactive'
    }
}

UNAUTHORIZED = {
    'status_code': '401',
    'error': {
        'code': 'UNAUTHORIZED',
        'message': 'Unauthorized access'
    }
}