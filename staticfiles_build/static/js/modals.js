function openModal(courseId, modalType = 'randevu') {
    if (modalType === 'randevu') {
        document.getElementById("courseId").value = courseId;
        document.getElementById("randevuModal").classList.remove("hidden");
        // Form ve seçimleri sıfırla
        document.getElementById("randevuForm").reset();
        document.getElementById("selectedSlotId").value = '';
        document.getElementById("selectedSaatId").value = '';
        document.getElementById("randevuSaati").innerHTML = '<option value="">Önce tarih seçiniz</option>';
    } else {
        document.getElementById("bilgiCourseId").value = courseId;
        document.getElementById("bilgiModal").classList.remove("hidden");
        document.getElementById("bilgiForm").reset();
    }
}

function closeModal(modalType = 'randevu') {
    if (modalType === 'randevu') {
        document.getElementById("randevuModal").classList.add("hidden");
        document.getElementById("randevuForm").reset();
        document.getElementById("selectedSlotId").value = '';
        document.getElementById("selectedSaatId").value = '';
        document.getElementById("randevuSaati").innerHTML = '<option value="">Önce tarih seçiniz</option>';
    } else {
        document.getElementById("bilgiModal").classList.add("hidden");
        document.getElementById("bilgiForm").reset();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Randevu formu işlemleri
    document.getElementById("randevuTarihi").addEventListener("change", function(e) {
        const date = e.target.value;
        const courseId = document.getElementById("courseId").value;

        fetch("/get-available-slots/", {
            method: "POST",
            body: new URLSearchParams({
                date: date,
                course_id: courseId,
            }),
        })
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById("randevuSaati");
            select.innerHTML = '<option value="">Randevu saati seçiniz</option>';

            if (data.success && data.slots.length > 0) {
                // Slot ID'sini kaydet
                document.getElementById("selectedSlotId").value = data.slots[0].id;
                
                data.slots.forEach(slot => {
                    const option = document.createElement("option");
                    option.value = slot.saat_id;
                    option.textContent = slot.time;
                    select.appendChild(option);
                });
            } else {
                Swal.fire({
                    icon: 'warning',
                    title: 'Uyarı!',
                    text: data.error || 'Seçilen tarihte uygun randevu saati bulunmamaktadır.',
                    confirmButtonText: 'Tamam'
                });
            }
        });
    });

    // Randevu saati seçildiğinde
    document.getElementById("randevuSaati").addEventListener("change", function(e) {
        document.getElementById("selectedSaatId").value = e.target.value;
    });

    // Randevu formu gönderimi
    document.getElementById("randevuForm").addEventListener("submit", function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch("/save-appointment/", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Başarılı!',
                    text: data.message,
                    confirmButtonText: 'Tamam'
                }).then(() => {
                    closeModal('randevu');
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Hata!',
                    text: data.error,
                    confirmButtonText: 'Tamam'
                });
            }
        });
    });

    // Bilgi formu gönderimi
    document.getElementById("bilgiForm").addEventListener("submit", function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch("/save-info-request/", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Başarılı!',
                    text: data.message,
                    confirmButtonText: 'Tamam'
                }).then(() => {
                    closeModal('bilgi');
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Hata!',
                    text: data.error,
                    confirmButtonText: 'Tamam'
                });
            }
        });
    });

    // Bugünden önceki tarihleri seçmeyi engelle
    const today = new Date().toISOString().split('T')[0];
    document.getElementById("randevuTarihi").min = today;
}); 