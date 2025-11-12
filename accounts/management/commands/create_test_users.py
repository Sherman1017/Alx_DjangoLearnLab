from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from datetime import date

class Command(BaseCommand):
    help = 'Create test users for the custom user model'

    def handle(self, *args, **options):
        # Create a regular user
        user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            date_of_birth=date(1990, 1, 1)
        )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created user: {user.email}')
        )

        # Create a superuser
        admin_user = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User'
        )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created admin user: {admin_user.email}')
        )
