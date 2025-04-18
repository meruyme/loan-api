from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from loans.models import Bank


class Command(BaseCommand):
    help = "Create initial data to test the API locally"

    def handle(self, *args, **options):
        Bank.objects.get_or_create(name="First Bank")
        if not User.objects.filter(username="usuario1_teste").exists():
            User.objects.create_user(
                username="usuario1_teste",
                password="123456",
                first_name="Usuário 1",
                last_name="Teste",
            )
        if not User.objects.filter(username="usuario2_teste").exists():
            User.objects.create_user(
                username="usuario2_teste",
                password="123456",
                first_name="Usuário 2",
                last_name="Teste",
            )
