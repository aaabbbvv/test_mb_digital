from faker import Faker
from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import User, Group, Membership


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            User.objects.create_superuser(
                username=settings.DEFAULT_ADMIN_NAME,
                email=settings.DEFAULT_ADMIN_EMAIL,
                password=settings.DEFAULT_ADMIN_PASSWORD,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'*' * 4} Admin with email {settings.DEFAULT_ADMIN_EMAIL} has been created! {'*' * 4}"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'*'*4} Admin with such email {settings.DEFAULT_ADMIN_EMAIL} already exists! {'*'*4}"
                )
            )

        fake = Faker()

        groups = []
        for _ in range(10):
            group = Group.objects.create(name=fake.company())
            groups.append(group)

        for _ in range(30):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='qwerty123456!'
            )

            for group in groups:
                if fake.boolean(chance_of_getting_true=25):
                    Membership.objects.create(user=user, group=group)

        self.stdout.write(self.style.SUCCESS(f"{'*'*4} Successfully generated fake data! {'*'*4}"))
