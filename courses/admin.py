from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from unfold.admin import ModelAdmin
from .models import Category, Course, Randevu, RandevuSlot, RandevuSaati, BilgiTalebi

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 20
    ordering = ('name',)

@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'description', 'category')
        }),
        ('Fiyatlandırma ve Durum', {
            'fields': ('price', 'is_active')
        }),
        ('Tarih Bilgileri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(RandevuSaati)
class RandevuSaatiAdmin(ModelAdmin):
    list_display = ('saat', 'bitis_saati')
    ordering = ('saat',)

    def has_add_permission(self, request):
        return False  # Manuel eklemeyi engelle

    def has_delete_permission(self, request, obj=None):
        return False  # Manuel silmeyi engelle

    def has_change_permission(self, request, obj=None):
        return False  # Manuel değiştirmeyi engelle

class RandevuSlotBulkAddForm(admin.helpers.ActionForm):
    class Meta:
        model = RandevuSlot
        fields = ['course', 'tarih']

@admin.register(RandevuSlot)
class RandevuSlotAdmin(ModelAdmin):
    list_display = ('course', 'tarih', 'get_randevu_saatleri')
    list_filter = ('course', 'tarih')
    search_fields = ('course__name',)
    ordering = ('tarih',)
    list_per_page = 20
    filter_horizontal = ('randevu_saatleri',)

    def get_randevu_saatleri(self, obj):
        return ", ".join([str(saat) for saat in obj.randevu_saatleri.all()])
    get_randevu_saatleri.short_description = 'Randevu Saatleri'

    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('course', 'tarih')
        }),
        ('Randevu Saatleri', {
            'fields': ('randevu_saatleri',),
            'description': 'Birden fazla saat seçmek için CTRL tuşuna basılı tutarak seçim yapabilirsiniz.'
        })
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-add/', self.bulk_add_view, name='courses_randevuslot_bulk_add'),
        ]
        return custom_urls + urls

    def bulk_add_view(self, request):
        if request.method == 'POST':
            course_id = request.POST.get('course')
            tarih = request.POST.get('tarih')
            saat_listesi = request.POST.getlist('saatler')

            if course_id and tarih and saat_listesi:
                course = Course.objects.get(id=course_id)
                RandevuSlot.create_slots_for_date(course, tarih, saat_listesi)
                self.message_user(request, 'Randevu slotları başarıyla oluşturuldu.')
                return HttpResponseRedirect('../')

        # Form sayfasını göster
        courses = Course.objects.filter(is_active=True)
        saatler = RandevuSaati.objects.all()
        
        context = {
            'courses': courses,
            'saatler': saatler,
            'title': 'Toplu Randevu Slotu Ekle',
            'site_title': self.admin_site.site_title,
            'site_header': self.admin_site.site_header,
            'site_url': self.admin_site.site_url,
            'has_permission': self.has_add_permission(request),
        }
        
        return render(request, 'admin/courses/randevuslot/bulk_add.html', context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_bulk_add_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Randevu)
class RandevuAdmin(ModelAdmin):
    list_display = ('ad_soyad', 'get_course', 'get_tarih', 'randevu_saati', 'telefon', 'created_at')
    list_filter = ('slot__course', 'slot__tarih', 'randevu_saati')
    search_fields = ('ad_soyad', 'telefon', 'not_bilgisi')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 20

    def get_course(self, obj):
        return obj.slot.course.name
    get_course.short_description = 'Kurs'
    get_course.admin_order_field = 'slot__course__name'

    def get_tarih(self, obj):
        return obj.slot.tarih
    get_tarih.short_description = 'Tarih'
    get_tarih.admin_order_field = 'slot__tarih'

    def has_add_permission(self, request):
        return False  # Randevular sadece frontend'den eklenebilir

@admin.register(BilgiTalebi)
class BilgiTalebiAdmin(ModelAdmin):
    list_display = ('ad_soyad', 'course', 'telefon', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('ad_soyad', 'telefon', 'not_bilgisi')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 20

    def has_add_permission(self, request):
        return False  # Bilgi talepleri sadece frontend'den eklenebilir
