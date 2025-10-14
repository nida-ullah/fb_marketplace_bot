"""
Django management command to check if superuser exists, verify password, or create new one.
Usage: python manage.py check_superuser
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class Command(BaseCommand):
    help = 'Check if superuser exists, verify password, or create a new one'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username to check or create',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password to verify or set',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email for new superuser',
        )
        parser.add_argument(
            '--create',
            action='store_true',
            help='Create superuser if not exists',
        )
        parser.add_argument(
            '--verify',
            action='store_true',
            help='Verify superuser password',
        )

    def handle(self, *args, **options):
        username = options.get('username')
        password = options.get('password')
        email = options.get('email')
        create_flag = options.get('create')
        verify_flag = options.get('verify')

        # List all superusers
        superusers = User.objects.filter(is_superuser=True)

        if superusers.exists():
            self.stdout.write(self.style.SUCCESS(
                f'\n✓ Found {superusers.count()} superuser(s):'))
            for user in superusers:
                self.stdout.write(f'  - Username: {user.username}')
                self.stdout.write(f'    Email: {user.email}')
                self.stdout.write(f'    Active: {user.is_active}')
                self.stdout.write(f'    Staff: {user.is_staff}')
        else:
            self.stdout.write(self.style.WARNING(
                '\n✗ No superuser found in the database.'))

        # Verify password if requested
        if verify_flag and username and password:
            user = authenticate(username=username, password=password)

            if user is not None and user.is_superuser:
                self.stdout.write(self.style.SUCCESS(
                    f'\n✓ Password is correct for superuser "{username}"!'))
            else:
                self.stdout.write(self.style.ERROR(
                    f'\n✗ Authentication failed for "{username}". Password is incorrect or user is not a superuser.'))

        # Create superuser if requested
        elif create_flag and username and password:
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(
                    f'\n⚠ User "{username}" already exists.'))

                # Check if it's a superuser
                user = User.objects.get(username=username)
                if user.is_superuser:
                    self.stdout.write(self.style.WARNING(
                        f'  "{username}" is already a superuser.'))
                else:
                    # Promote to superuser
                    user.is_superuser = True
                    user.is_staff = True
                    user.save()
                    self.stdout.write(self.style.SUCCESS(
                        f'\n✓ User "{username}" promoted to superuser!'))
            else:
                try:
                    user = User.objects.create_superuser(
                        username=username,
                        email=email or f'{username}@example.com',
                        password=password
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f'\n✓ Superuser "{username}" created successfully!'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'\n✗ Error creating superuser: {e}'))

        # If no flags provided, show usage
        if not verify_flag and not create_flag and not superusers.exists():
            self.stdout.write(self.style.WARNING(
                '\nNo superusers found. Use --create to create one.'))
            self.stdout.write('\nExample:')
            self.stdout.write(
                '  python manage.py check_superuser --create --username admin --password yourpassword --email admin@example.com')
