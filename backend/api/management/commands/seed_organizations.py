from django.core.management.base import BaseCommand
from api.models import Initiator


class Command(BaseCommand):
    help = 'Создаёт обязательные организации для статистики'

    def handle(self, *args, **options):
        orgs = [
            "МУВП ВПЭС",
            'КГУП "Приморский водоканал"',
            "Управляющие компании"
        ]

        created_count = 0
        for name in orgs:
            obj, created = Initiator.objects.get_or_create(
                initiator_name=name,
                defaults={'initiator_id': None}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Создана: {name}"))
            else:
                self.stdout.write(f"Уже существует: {name}")

        self.stdout.write(self.style.SUCCESS(f"Готово! Создано организаций: {created_count}"))