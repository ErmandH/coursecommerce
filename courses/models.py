from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime, timedelta

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Kategori Adı')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'

class Course(models.Model):
    name = models.CharField(max_length=200, verbose_name='Kurs Adı')
    description = RichTextField(verbose_name='Açıklama')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses', verbose_name='Kategori')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Fiyat')
    is_active = models.BooleanField(default=True, verbose_name='Aktif mi?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'

class RandevuSaati(models.Model):
    saat = models.TimeField(verbose_name='Saat')
    bitis_saati = models.TimeField(verbose_name='Bitiş Saati')

    def __str__(self):
        return f"{self.saat.strftime('%H:%M')}-{self.bitis_saati.strftime('%H:%M')}"

    class Meta:
        verbose_name = 'Randevu Saati'
        verbose_name_plural = 'Randevu Saatleri'
        ordering = ['saat']

    @classmethod
    def create_time_slots(cls):
        # Mevcut tüm saatleri temizle
        cls.objects.all().delete()

        # Başlangıç ve bitiş saatlerini belirle (09:00-17:00 arası)
        current_time = datetime.strptime('09:00', '%H:%M')
        end_time = datetime.strptime('17:00', '%H:%M')

        while current_time < end_time:
            end_slot = current_time + timedelta(minutes=45)
            cls.objects.create(
                saat=current_time.time(),
                bitis_saati=end_slot.time()
            )
            current_time += timedelta(minutes=60)  # 45 dk ders + 15 dk ara

class RandevuSlot(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Kurs')
    tarih = models.DateField(verbose_name='Tarih')
    randevu_saatleri = models.ManyToManyField(RandevuSaati, verbose_name='Randevu Saatleri')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')

    def __str__(self):
        return f"{self.course.name} - {self.tarih}"

    class Meta:
        verbose_name = 'Randevu Slotu'
        verbose_name_plural = 'Randevu Slotları'
        ordering = ['tarih']
        unique_together = ['course', 'tarih']

    @classmethod
    def create_slots_for_date(cls, course, tarih, saat_listesi=None):
        """
        Belirli bir tarih için randevu slotları oluşturur.
        
        Args:
            course: Kurs objesi
            tarih: datetime.date objesi
            saat_listesi: RandevuSaati id listesi (None ise tüm saatler kullanılır)
        """
        slot, created = cls.objects.get_or_create(
            course=course,
            tarih=tarih
        )
        
        if saat_listesi is None:
            saatler = RandevuSaati.objects.all()
        else:
            saatler = RandevuSaati.objects.filter(id__in=saat_listesi)
        
        slot.randevu_saatleri.set(saatler)
        return slot

class Randevu(models.Model):
    slot = models.ForeignKey(RandevuSlot, on_delete=models.CASCADE, verbose_name='Randevu Slotu')
    randevu_saati = models.ForeignKey(RandevuSaati, on_delete=models.CASCADE, verbose_name='Randevu Saati')
    ad_soyad = models.CharField(max_length=100, verbose_name='Ad Soyad')
    telefon = models.CharField(max_length=15, verbose_name='Telefon')
    not_bilgisi = models.TextField(verbose_name='Not', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')

    def save(self, *args, **kwargs):
        # Randevu kaydedildiğinde seçilen saati slot'tan kaldır
        super().save(*args, **kwargs)
        self.slot.randevu_saatleri.remove(self.randevu_saati)

    def __str__(self):
        return f"{self.ad_soyad} - {self.slot.course.name} - {self.slot.tarih} {self.randevu_saati}"

    class Meta:
        verbose_name = 'Randevu'
        verbose_name_plural = 'Randevular'
        ordering = ['-created_at']

class BilgiTalebi(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Kurs')
    ad_soyad = models.CharField(max_length=100, verbose_name='Ad Soyad')
    telefon = models.CharField(max_length=15, verbose_name='Telefon')
    not_bilgisi = models.TextField(verbose_name='Not', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')

    def __str__(self):
        return f"{self.ad_soyad} - {self.course.name}"

    class Meta:
        verbose_name = 'Bilgi Talebi'
        verbose_name_plural = 'Bilgi Talepleri'
        ordering = ['-created_at']
