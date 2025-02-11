from django.core.management.base import BaseCommand
from courses.models import RandevuSaati

class Command(BaseCommand):
    help = 'Randevu saatlerini oluşturur'

    def handle(self, *args, **options):
        RandevuSaati.create_time_slots()
        self.stdout.write(self.style.SUCCESS('Randevu saatleri başarıyla oluşturuldu.')) 