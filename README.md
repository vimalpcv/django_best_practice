
# Django Best Practice

This project serves as a comprehensive guide and blueprint for creating strong and scalable web APIs with Django and 
Django Rest Framework (DRF). It provides detailed instructions for organizing code, implementing authentication and 
authorization, efficient logging, popular database connection choices, secure encryption and decryption techniques 
using the best Cipher mechanism, and comprehensive documentation. 
When starting a Django project, this resource is your confident jumpstart for API development.

## Getting Started

Follow the instructions in the documentation to get started with this project and leverage the best practices it offers.

## Usage

Use this project as a foundation for your Django-based API development. Simply clone or fork it to kickstart your project with the best practices already in place.

## Contribution

Contributions are welcome! If you have ideas to improve this project or want to fix issues, please follow our contribution guidelines.


## Technologies Used

<p align="left">
<a href="https://www.python.org" target="_blank" rel="noreferrer"> 
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> 
</a> 
<a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> 
	<img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> 
</a>
<a>
    <img src="https://resources.jetbrains.com/storage/products/company/brand/logos/PyCharm_icon.svg" alt="django" width="40" height="40" />
</a>
<a>
    <img src="https://code.visualstudio.com/assets/images/code-stable.png" alt="django" width="40" height="40" />
</a>
<a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> 
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> 
</a>
 <a href="https://www.mysql.com/" target="_blank" rel="noreferrer"> 
	<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" alt="mysql" width="40" height="40"/> 
</a> 
<a href="https://mariadb.org/" target="_blank" rel="noreferrer"> 
	<img src="https://www.vectorlogo.zone/logos/mariadb/mariadb-icon.svg" alt="mariadb" width="40" height="40"/> 
</a>
<a href="https://www.oracle.com/" target="_blank" rel="noreferrer">
 <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/oracle/oracle-original.svg" alt="oracle" width="40" height="40"/>
</a>
<a href="https://www.sqlite.org/" target="_blank" rel="noreferrer"> 
  <img src="https://www.vectorlogo.zone/logos/sqlite/sqlite-icon.svg" alt="sqlite" width="40" height="40"/> 
 </a>

<a href="https://postman.com" target="_blank" rel="noreferrer"> 
    <img src="https://www.vectorlogo.zone/logos/getpostman/getpostman-icon.svg" alt="postman" width="40" height="40"/> 
</a>
</p>



| Parameter                 | Technology                                          | Version     |
| :------------------------ |:----------------------------------------------------| :-----------|
| `Programming Language`    | `Python`                                            | v3.11       |
| `Framework`               | `Django`                                            | v4.2        |
| `IDE`                     | `PyCharm, Visual Studio Code`                       |             |
| `Database`                | `PostgreSQL`, `MySQL`, `MariaDB`,`Oracle`, `SQLite` |             |
| `Storage`                 | `S3`                                                |             |
| `Email Service`           | `Sendgrid`                                          |             |
| `Payment`                 | `Stripe`                                            |             |
| `Documentation`           | `Postman`,`Swagger, Redoc`                          |             |

## Setup


Follow these steps to set up and run the "Django Best Practice" project on your local development environment:

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

## Supported Databases

In this project, we've implemented support for various databases, providing you with the flexibility to choose the one that best suits your needs. The supported databases are as follows:

1. **SQLite**
2. **PostgreSQL**
3. **MySQL**
4. **MariaDB**
5. **Oracle**

### Setup Instructions

To configure your project to use a specific database, follow these steps:

1. Open the `environment/base.py` file.

2. Locate the database settings section, and you'll find different database objects for each supported database type.

3. Uncomment the database object that corresponds to the database you wish to use. For example, if you want to use MySQL, uncomment the MySQL database object.

4. Ensure that you've installed the required database packages by checking the `requirements.txt` file.

5. Set the database credentials such as `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` in the `.env` file or as environment variables. Replace these placeholders with your actual database connection details.

   For example, if you're using MySQL, your `.env` file might look like this:

   ```plaintext
   DB_ENGINE=mysql
   DB_HOST=your_mysql_host
   DB_PORT=3306
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
    ```

## Authentication

In this project, we've implemented the authentication system using the `dj-rest-auth[with_social]` package. There are two types of authentication methods available:

1. **JSON Web Token (JWT)**
2. **Token-Based**

For JWT implementation, we utilize the additional module `djangorestframework-simplejwt`. Each authentication method has its own configuration.

### To Use JWT

1. Set the `JWT_AUTHENTICATION_ENABLED` environment variable in the `environment/base.py` to `True`. By default, it is set to `True`.

2. Run a migration command.

#### Login - /auth/login/
- Provide the necessary data (either username or email) along with the password. 
- This endpoint will return both the `access` and `refresh` tokens, as well as the user details.

#### Token Expiration
- When the `access` token expires, you can generate a new one using the `refresh` token (before it expires). 
- Use the `auth/refresh/` endpoint to obtain a fresh `access` token.
- You can adjust the token expiration time by modifying the values of `ACCESS_TOKEN_LIFETIME` and `REFRESH_TOKEN_LIFETIME` within the `environment/base.py` file under the `SIMPLE_JWT` configuration.

#### Logout - /auth/logout/
- This effectively invalidates the `refresh` token, requiring users to log in again for authentication.

### To Use Token-Based

1. Set the `JWT_AUTHENTICATION_ENABLED` environment variable in the `environment/base.py` to `False`. By default, it is set to `True`.

#### Login - /auth/login/
- Provide the necessary data (either username or email) along with the password. 
- This endpoint will return a token 'key', as well as the user details.

#### Expiration
- Set the token expiration by adjusting the `TOKEN_LIFETIME` variable in the `environment/base.py` file.

#### Logout - /api/logout/
- This will immediately invalidate the token key, requiring users to log in again for authentication.

### Authentication Method
- You can change the authentication method by modifying the `ACCOUNT_AUTHENTICATION_METHOD` setting. 
- Choose between using `email`, `username`, or both `username_email` for authentication.

### Linking Social Accounts

The process of linking social accounts is the same for both authentication methods:

- You can link an existing account to social logins from platforms like Google, Facebook, Twitter, Apple, GitHub, Microsoft, and more. Currently, we've implemented Google login, but you can enable other social providers as well.

  - To connect a Google account, use the `/auth/connect/google/` endpoint along with a Google access code. 
  - You can connect multiple social accounts to a single user account.
  - You can configure whether the user's email and Google email should be the same or different by setting the `SOCIAL_SAME_EMAIL_CONNECT` variable; the default is true.
  - To view the list of social accounts linked to an account, use the `auth/social-accounts/` endpoint. 
  - Additionally, you can disconnect social accounts at any time by using `auth/social-accounts/1/disconnect/`.

### Testing Social Logins

For testing purposes, follow these steps:

- Create an app in the Google Console: [https://console.cloud.google.com/](https://console.cloud.google.com/).

- Create a Google token by using the following URL: 
    [Google Token Creation](https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://127.0.0.1&prompt=consent&response_type=code&client_id=<your_client_id>&scope=openid%20email%20profile&access_type=offline).

- Decode the code using a URL decoder like this: [URL Decoder](https://meyerweb.com/eric/tools/dencoder/). 
- Please note that the method for testing may vary for each social provider.

This authentication system provides both standard and social login capabilities while offering flexibility in token expiration, authentication methods, and social account linking. Customize these settings to align with your project's specific requirements.

## Authorization

In this project, we manage authorization by setting the `permission_classes` attribute on the API class declarations. The available permission classes are as follows:

1. **AllowAny**: This permission class does not require authentication. It allows unrestricted access to the API endpoint.

2. **IsAuthenticated**: This permission class requires valid user authentication. Only authenticated users can access the API endpoint.

3. **IsAllowedUser**: This custom permission class verifies whether the authorized user's role has permission to make the request.

   ### Example Implementation
      ```python

      from rest_framework.permissions import AllowAny, IsAuthenticated
      from base.permissions import IsAllowedUser, method_permission_classes
      from base.constants import SUPER_ADMIN, ADMIN

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
        "properties": {"code": {"type": "string"}, },
        "required": ["code"]
    }
},

# responses
from base.error import ERROR_SCHEMA

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

## Cipher / Request Body Encryption and Decryption

In this project, we have implemented request body encryption using the `AES GCM` mode. 
You can enable or disable this feature by setting the `ENCRYPT` environment variable.

- To enable encryption, set `ENCRYPT=True` in your environment.
- To disable encryption, set `ENCRYPT=False` in your environment.

### Secret Key

To configure the encryption process, you can specify the secret key by setting the 
`ENCRYPTION_KEY` environment variable. 
It's crucial to keep this key secure as it's used for both encryption and decryption.

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

## Backend Management Commands

In this project, we've added a custom management command to help you set up the backend for "Django Best Practice." This command streamlines backend-related tasks to ensure a smooth setup. Here are the available commands and their descriptions:

- **Setup Backend**: To set up the backend for your project, use the following commands:

   - `all`: This command will execute all backend commands to prepare the environment effectively.

   - `create_superuser_and_organization`: Use this command to create both a superuser and an admin organization, which is often a key step in initializing a new Django project.

To execute these commands, navigate to your project directory and run them as follows:

```bash
python manage.py setup_backend <command_name>

# Example
python manage.py setup_backend all

# Help
python manage.py setup_backend --help
```

## Logging

In this project, we have implemented a comprehensive logging system that covers request and response logs, error logs, and info logs. The logging system offers three types of handlers to suit your needs:

1. **FILE_HANDLER**: When the `FILE_HANDLER` is set up, log files are stored in the `/logs` directory. This handler is ideal for persistent log storage.

2. **STREAM_HANDLER**: The `STREAM_HANDLER` is configured to print logs on the console. It provides real-time visibility of log entries and is particularly useful for debugging during development.

3. **LOGSTASH_HANDLER**: With the `LOGSTASH_HANDLER`, logs are written to a Logstash server. This option is valuable for centralized log management and analysis.

### Configuration

You can configure the logging handler by setting the `LOGGING` environment variable. By default, it is set to `STREAM_HANDLER`. You can adjust it to your preferred handler as follows:

- To enable `FILE_HANDLER`, set `LOGGING=FILE_HANDLER`.
- For `STREAM_HANDLER`, set `LOGGING=STREAM_HANDLER`.

- If you choose to use the `LOGSTASH_HANDLER`, you need to set the following additional environment variables:

  - `LOGSTASH_HOST`: Set this variable to the hostname or IP address of your Logstash server.
  - `LOGSTASH_PORT`: Set this variable to the port number on which Logstash is listening.





