# Common error codes
ERROR_SCHEMA = {
    "type": "object",
    "example": {
        "code": "string",
        "message": "string",
        "detail": "string | dict",
    }
}

INTERNAL_SERVER_ERROR = {
    'status_code': '500',
    'error': {
        'code': 'INTERNAL_SERVER_ERROR',
        'message': 'Internal Server Error'
    }
}

INVALID_CONTENT_TYPE = {
    'status_code': '400',
    'error': {
        'code': 'INVALID_CONTENT_TYPE',
        'message': "The request Content-Type should be 'application/json'."
    }
}

INVALID_PARAMETERS = {
    'status_code': '400',
    'error': {
        'code': 'INVALID_PARAMETERS',
        'message': 'Invalid Parameters'
    }
}

BAD_REQUEST = {
    'status_code': '400',
    'error': {
        'code': 'BAD_REQUEST',
        'message': 'Bad Request'
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

# Error Codes for Authentication

INVALID_REFRESH_TOKEN = {
    'status_code': '400',
    'error': {
        'code': 'INVALID_REFRESH_TOKEN',
        'message': 'Refresh Token is invalid or expired'
    }
}

INVALID_PASSWORD = {
    'status_code': '400',
    'error': {
        'code': 'INVALID_PASSWORD',
        'message': 'Invalid Password'
    }
}

ACCOUNT_NOT_FOUND = {
    'status_code': '404',
    'error': {
        'code': 'ACCOUNT_NOT_FOUND',
        'message': 'Account not found'
    }
}

# Error Codes for Authorization
UNAUTHORIZED = {
    'status_code': '401',
    'error': {
        'code': 'UNAUTHORIZED',
        'message': 'Unauthorized access'
    }
}

USER_NOT_FOUND = {
    'status_code': '404',
    'error': {
        'code': 'USER_NOT_FOUND',
        'message': 'User not found'
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




