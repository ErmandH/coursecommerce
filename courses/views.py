from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Course, Category, Randevu, RandevuSlot, BilgiTalebi, RandevuSaati
from datetime import datetime

def home(request):
    # Ücretsiz kursları al
    free_category = Category.objects.filter(name='Ücretsiz').first()
    free_courses = Course.objects.filter(category=free_category, is_active=True) if free_category else []
    
    # Diğer kategorileri al (Ücretsiz hariç)
    other_categories = Category.objects.exclude(name='Ücretsiz')
    
    # Her kategori için kursları al
    category_courses = {
        category: Course.objects.filter(category=category, is_active=True)
        for category in other_categories
    }
    
    context = {
        'free_courses': free_courses,
        'category_courses': category_courses,
        'categories': other_categories,
    }
    
    return render(request, 'courses/home.html', context)

@csrf_exempt
@require_POST
def get_available_slots(request):
    try:
        date_str = request.POST.get('date')
        course_id = request.POST.get('course_id')
        
        # Tarihi parse et
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Müsait slotu bul veya oluştur
        slot = RandevuSlot.objects.filter(
            course_id=course_id,
            tarih=selected_date
        ).first()

        if not slot:
            # Slot yoksa yeni oluştur
            course = Course.objects.get(id=course_id)
            slot = RandevuSlot.create_slots_for_date(course, selected_date)

        # Müsait saatleri döndür
        formatted_slots = [
            {
                'id': slot.id,
                'saat_id': saat.id,
                'time': str(saat)
            }
            for saat in slot.randevu_saatleri.all()
        ]

        if not formatted_slots:
            return JsonResponse({
                'success': False,
                'error': 'Bu tarih için müsait randevu saati bulunmamaktadır.'
            })
        
        return JsonResponse({
            'success': True,
            'slots': formatted_slots
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@csrf_exempt
@require_POST
def save_appointment(request):
    try:
        # Form verilerini al
        slot_id = request.POST.get('slot_id')
        saat_id = request.POST.get('saat_id')
        ad_soyad = request.POST.get('ad_soyad')
        telefon = request.POST.get('telefon')
        not_bilgisi = request.POST.get('not_bilgisi')
        
        # Slotu ve saati kontrol et
        slot = RandevuSlot.objects.get(id=slot_id)
        saat = RandevuSaati.objects.get(id=saat_id)
        
        if saat not in slot.randevu_saatleri.all():
            raise ValueError('Seçilen saat bu slot için geçerli değil.')
        
        # Randevuyu kaydet
        randevu = Randevu.objects.create(
            slot=slot,
            randevu_saati=saat,
            ad_soyad=ad_soyad,
            telefon=telefon,
            not_bilgisi=not_bilgisi
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Randevunuz başarıyla oluşturuldu.'
        })
        
    except RandevuSlot.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Randevu slotu bulunamadı.'
        })
    except RandevuSaati.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Seçilen saat bulunamadı.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@csrf_exempt
@require_POST
def save_info_request(request):
    try:
        # Form verilerini al
        course_id = request.POST.get('course_id')
        ad_soyad = request.POST.get('ad_soyad')
        telefon = request.POST.get('telefon')
        not_bilgisi = request.POST.get('not_bilgisi')
        
        # Kursu kontrol et
        course = Course.objects.get(id=course_id)
        
        # Bilgi talebini kaydet
        bilgi_talebi = BilgiTalebi.objects.create(
            course=course,
            ad_soyad=ad_soyad,
            telefon=telefon,
            not_bilgisi=not_bilgisi
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Bilgi talebiniz başarıyla alındı. En kısa sürede sizinle iletişime geçeceğiz.'
        })
        
    except Course.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Kurs bulunamadı.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
