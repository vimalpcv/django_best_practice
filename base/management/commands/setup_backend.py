from django.core.management.base import BaseCommand
from user.models import User, Organization
from base.constants import SUPER_ADMIN
from argparse import RawTextHelpFormatter


class Command(BaseCommand):
    """
    This command will create a superuser and an admin organization.
    """

    help = '\033[1mSetup backend for Django Best Practice\033[0m\n' \
           'Please use one of the following commands:\n' \
           '\033[1m\033[3mall\033[0m                                : ' \
           'This command will execute all backend commands \n' \
           '\033[1m\033[3mcreate_superuser_and_organization\033[0m  : ' \
           'This command will create both a superuser and an admin organization \n' \

    # /033[1m is used for bold text and /033[3m is used for italic text
    # /033[0m is used to reset the text to default

    def create_parser(self, *args, **kwargs):
        parser = super(Command, self).create_parser(*args, **kwargs)
        parser.formatter_class = RawTextHelpFormatter
        return parser

    def add_arguments(self, parser):
        parser.add_argument("setup", nargs="+", type=str)

    def create_superuser_and_organization(self):
        username = 'admin'
        email = 'admin@domain_name.com'
        password = 'admin'
        if not User.objects.filter(username=username).exists():
            admin = User.objects.create_superuser(username=username, email=email, password=password,
                                                  first_name='Super', last_name='Admin', role=SUPER_ADMIN)
            self.stdout.write(
                self.style.SUCCESS(f'Superuser created with username: '
                                   f'"{username}", email: "{email}" and password: "{password}".'
                                   f' Please change the password for {username} as soon as possible.'))
        else:
            admin = User.objects.get(username=username)
            self.stdout.write(self.style.SUCCESS(f'Superuser already exists with username: {username}.'))

        name = 'Admin Organization'
        description = 'This is the admin organization'
        if not Organization.objects.filter(name=name).exists():
            organization = Organization.objects.create(name=name, description=description)
            self.stdout.write(self.style.SUCCESS(f'Organization created with name: {name}.'))
        else:
            organization = Organization.objects.get(name=name)
            self.stdout.write(self.style.SUCCESS(f'Organization already exists with name: {name}.'))

        admin.organization = organization
        admin.save()

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting setup for backend of Django Best Practice. Please wait...'))
        setup = options['setup'][0]
        if setup == 'create_superuser_and_organization':
            self.create_superuser_and_organization()
            self.stdout.write(self.style.SUCCESS('Successfully setup backend for Django Best Practice.'))
        elif setup == 'all':
            self.create_superuser_and_organization()
            self.stdout.write(self.style.SUCCESS('Successfully setup backend for Django Best Practice.'))
        else:
            self.stdout.write(self.style.ERROR('Invalid setup command'))
            self.stdout.write(self.style.ERROR('Please use one of the following commands:'))
            self.stdout.write(self.style.ERROR('1. all'))
            self.stdout.write(self.style.ERROR('2. create_superuser_and_organization'))
