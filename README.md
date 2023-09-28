
# Django Best Practices

This project serves as a comprehensive guide and template for building robust and scalable web APIs using Django and Django Rest Framework (DRF). It embodies best practices for code organization, authentication methods, efficient logging, and thorough documentation. When embarking on a Django project, this resource will help to kickstart API development with confidence.

## Getting Started

Follow the instructions in the documentation to get started with this project and leverage the best practices it offers.

## Usage

Use this project as a foundation for your Django-based API development. Simply clone or fork it to kickstart your project with the best practices already in place.

## Contribution

Contributions are welcome! If you have ideas to improve this project or want to fix issues, please follow our contribution guidelines.


## Technologies Used


| Parameter                 | Technology                    | Version     |
| :------------------------ | :---------------------        | :-----------|
| `Programming Language`    | `Python`                      | v3.11       |
| `Framework`               | `Django`                      | v4.2        |
| `IDE`                     | `PyCharm, Visual Studio Code` |             |
| `Database`                | `PostgreSQL, MySQL, SQLite`   |             |
| `Storage`                 | `S3`                          |             |
| `Email Service`           | `Sendgrid`                    |             |
| `Payment`                 | `Stripe`                      |             |
| `Documentation`           | `Swagger, Redoc`              |             |


## Setup


Follow these steps to set up and run the "Django Best Practices" project on your local development environment:

### Prerequisites

- [Python](https://www.python.org/downloads/) (3.6 or higher)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) (recommended)

### Clone the Repository

```shell 
git https://github.com/vimalpcv/django_syntax.git 
```
### Create a Virtual Environment (Optional but Recommended)

```shell
# Navigate to the project directory
cd django-best-practices

# Create a virtual environment (replace 'envname' with your preferred name)
virtualenv envname

# Activate the virtual environment
source envname/bin/activate   # On Windows, use 'envname\Scripts\activate'
```

### Install Dependencies
```shell
pip install -r requirements.txt
```

### Create a .env File with Credentials
To configure your project, create a .env file with your credentials. Use the following command as a template, replacing placeholders with your actual values:
```shell
echo "DEBUG=True" >> .env
echo "SECRET_KEY=your_secret_key_here" >> .env
echo "DB_HOST=your_database_host" >> .env
echo "DB_PORT=your_database_port" >> .env
echo "DB_NAME=your_database_name" >> .env
echo "DB_USER=your_database_user" >> .env
echo "DB_PASSWORD=your_database_password" >> .env
```

## API documentation
Explore the documentation API using the following endpoints:


1. **Download Postman YAML**: To integrate the API with Postman, you can download the YAML file containing the API's specifications. Import this file into your Postman workspace to streamline testing and development.

   Endpoint: [/api/docs/schema](http://127.0.0.1:8001/api/docs/schema)

2. **Swagger Documentation**: Swagger provides a user-friendly interface to explore and interact with the API. Access the Swagger documentation to understand the available endpoints, request parameters, and response formats.

   Endpoint: [/api/docs/swagger/](http://127.0.0.1:8001/api/docs/swagger/)

3. **Redoc Documentation**: Redoc offers an alternative way to view the API documentation with a clean and modern interface. Use Redoc to quickly grasp the API's capabilities and structure.

   Endpoint: [/api/docs/redoc/](http://127.0.0.1:8001/api/docs/redoc/)

### API documentation Implementation
   In this project, we use the drf-spectacular module to generate API documentation effortlessly. 
   You can enhance the documentation for each endpoint by using the @extend_schema decorator. 
   Here's an example of how to use it:

```python
from drf_spectacular.utils import OpenApiParameter

class sampleClass(APIView):

  @extend_schema(tags=["User"])
  def post(self, request):
     ...
``` 

**Example Use cases**

```python
# The following code should be provided as keyword arguments on the `@extend_schema()` decorator."
# to disable the schema for an API
exclude = True

# tags
tags = ["User"]

# parameters
from drf_spectacular.utils import OpenApiParameter

parameters = [
    OpenApiParameter(name="name", type=str, description="Name of the user", required=True),
    OpenApiParameter(name="age", type=int, description="Age of the user", ),
    OpenApiParameter(name="dob", type=datetime,
                     description="Date of birth of the user (YYYY-MM-DD)", ),
    OpenApiParameter(name="sex", type=str, description="Sex of the user", enum=["Male", "Female", "Others"],
                     default='Male'),
    OpenApiParameter(name="device_type", location='header'),  # query(default), path, header, cookie
]

# request
request = InputSerializer(many=True)
request = {
   "application/json": {
       "type": "object",
       "properties": {"code": {"type": "string"},},
       "required": ["code"]
    }
},

# responses
from common.error import ERROR_SCHEMA

responses = {
    202: OutputSerializer,
    202: {
        "type": "object",
        "example": {
            "name": "John",
            "age": 25,
        }
    },
    400: ERROR_SCHEMA,
    404: ERROR_SCHEMA,
    500: ERROR_SCHEMA,
}
# Note: In this project we followed the same format error response,
# So, error_schema was implented on the common/error.py and used here
```
**We can also generate schema with the CLI:**
```shell
python manage.py spectacular --file schema.yml
```

## Authentication

For this project, we utilize the `dj-rest-auth[with_social]` package for both standard and social logins, 
and we implement JWT (JSON Web Token) authentication with the `djangorestframework-simplejwt` module. 
Here's how our authentication system works:


### Login: 
- Access the login endpoint at `/auth/login/`. 
- Provide the necessary data (either username or email) along with the password. 
- This endpoint will return both the `access` and `refresh` tokens, as well as the user details.

### Authentication Method
- You can change the authentication method by modifying the `ACCOUNT_AUTHENTICATION_METHOD` setting. 
- Choose between using `email`, `username`, or both `username_email` for authentication.

### Token Expiration
- When the `access` token expires, you can generate a new one using the `refresh` token (before it expires). 
- Simply use the `auth/refresh/` endpoint to obtain a fresh `access` token.

### Custom Token Expiration Time
- You have the flexibility to customize the expiration duration for both the `access` token and the `refresh` token 
    according to your specific needs. 
- This can be achieved by adjusting the values of `ACCESS_TOKEN_LIFETIME` and `REFRESH_TOKEN_LIFETIME` 
    within the `common/base.py` file under the `SIMPLE_JWT` configuration, 
    aligning them with your preferred token expiration policy."

### Logout Endpoint
- To log out, make a request to `/auth/logout/`. 
- This effectively invalidates the `refresh` token, requiring users to log in again for authentication.

### Linking Social Accounts
- You can link an existing account to social logins from platforms like 
    `Google, Facebook, Twitter, Apple, GitHub, Microsoft, and more`. 
- Currently, we've implemented Google login, but you can enable other social providers as well.

  - To connect a Google account, use the `/auth/connect/google/` endpoint along with a Google access code. 
     You can connect multiple social accounts to a single user account.
  - To view the list of social accounts linked to an account, use the `auth/social-accounts/` endpoint. 
  - Additionally, you can disconnect social accounts at any time by using `auth/social-accounts/1/disconnect/`.

### Testing Social Logins
- For testing purposes, you'll need to create an app in the Google 
      Console: [https://console.cloud.google.com/](https://console.cloud.google.com/).

- Create a Google token by using the following URL: 
    [Google Token Creation](https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://127.0.0.1&prompt=consent&response_type=code&client_id=<your_client_id>&scope=openid%20email%20profile&access_type=offline).

- You can decode the code using a URL decoder like this: [URL Decoder](https://meyerweb.com/eric/tools/dencoder/). 
- Note that the method may vary for each social provider.

This authentication system provides both standard and social login capabilities while offering flexibility in token expiration, authentication methods, and social account linking. Customize these settings to align with your project's specific requirements.


## Authorization

In this project, we manage authorization by setting the `permission_classes` attribute on the API class declarations. The available permission classes are as follows:

1. **AllowAny**: This permission class does not require authentication. It allows unrestricted access to the API endpoint.

2. **IsAuthenticated**: This permission class requires valid user authentication. Only authenticated users can access the API endpoint.

3. **IsAllowedUser**: This custom permission class verifies whether the authorized user's role has permission to make the request.

   ### Example Implementation
      ```python

      from rest_framework.permissions import AllowAny, IsAuthenticated
      from common.permissions import IsAllowedUser, method_permission_classes
      from common.constants import SUPER_ADMIN, ADMIN

      # AllowAny
      class SampleClass(APIView):
         permission_classes = (AllowAny,)
         
         def post(self, request):
            ...
      
      # IsAuthenticated
      class SampleClass(APIView):
         permission_classes = (IsAuthenticated,)
         
         def post(self, request):
            ...

      # IsAllowedUser
      class SampleClass(APIView):
         permission_classes = (partial(IsAllowedUser, SUPER_ADMIN),)
         
         def post(self, request):
            ...

      # To control access based on the HTTP request method
      class SampleClass(APIView):
         permission_classes = (AllowAny,)
         
         def get(self, request):
            ...

         @method_permission_classes((IsAuthenticated,))
         def post(self, request):
            ...

         ethod_permission_classes((partial(IsAllowedUser, SUPER_ADMIN),))
         def patch(self, request):
            ...
      ```

## Cipher / Request Body Encryption and Decryption

In this project, we have implemented request body encryption using the `AES GCM` mode. You can enable or disable this feature by setting the `ENCRYPT` environment variable.

- To enable encryption, set `ENCRYPT=True` in your environment.
- To disable encryption, set `ENCRYPT=False` in your environment.

### Secret Key

To configure the encryption process, you can specify the secret key by setting the `ENCRYPTION_KEY` environment variable. It's crucial to keep this key secure as it's used for both encryption and decryption.

Example:

```plaintext
ENCRYPT=True
ENCRYPTION_KEY=my_secret_encryption_key
```
or
```shell
echo "ENCRYPT=True" >> .env
echo "ENCRYPTION_KEY=my_secret_encryption_key" >> .env
```




