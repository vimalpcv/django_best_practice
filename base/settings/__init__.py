import os, environ
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()


def set_environment():
    if env('DJANGO_ENVIRONMENT', default=None) is None:
        env_path = os.path.join(BASE_DIR, '.env')
        env.read_env(env_path)

    environment = env('DJANGO_ENVIRONMENT', default='local')
    if environment == 'production':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.production')
    elif environment == 'staging':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.staging')
    elif environment == 'development':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.development')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.local')

