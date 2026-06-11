import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create the dashboard admin user'

    def handle(self, *args, **options):
        username = os.getenv('DASHBOARD_USERNAME', 'Clinton')
        email = os.getenv('DASHBOARD_EMAIL', 'clinton,amponsah001@gmail.com')
        password = os.getenv('DASHBOARD_PASSWORD', 'Kunte100@@@@').rstrip('.')

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'is_staff': True, 'is_superuser': True, 'email': email},
        )
        user.set_password(password)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created dashboard user: {username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated password for: {username}'))
