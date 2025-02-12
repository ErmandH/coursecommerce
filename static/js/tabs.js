function switchTab(tabId) {
    // Tüm tab içeriklerini gizle
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.classList.add('hidden');
    });

    // Tüm tab butonlarından aktif sınıfı kaldır
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.classList.remove('bg-indigo-500', 'text-white');
        button.classList.add('bg-white', 'text-gray-700');
    });

    // Seçilen tab'ı göster
    const selectedTab = document.getElementById(tabId);
    if (selectedTab) {
        selectedTab.classList.remove('hidden');
    }

    // Seçilen tab butonunu aktif yap
    const selectedButton = document.querySelector(`[onclick="switchTab('${tabId}')"]`);
    if (selectedButton) {
        selectedButton.classList.remove('bg-white', 'text-gray-700');
        selectedButton.classList.add('bg-indigo-500', 'text-white');
    }
}

function toggleDescription(descriptionId) {
    const descriptionContainer = document.getElementById(descriptionId);
    const descriptionText = descriptionContainer.querySelector('.description-text');
    const descriptionGradient = descriptionContainer.querySelector('.description-gradient');
    const toggleButton = descriptionContainer.querySelector('.toggle-button');

    if (descriptionText.classList.contains('line-clamp-2')) {
        // Açıklama kapalıysa aç
        descriptionText.classList.remove('line-clamp-2');
        descriptionGradient.style.display = 'none';
        toggleButton.innerHTML = '<i class="fas fa-chevron-up"></i>';
        
        // Scroll varsa gradient'i göster
        if (descriptionText.scrollHeight > 300) {
            descriptionText.style.maxHeight = '300px';
            descriptionGradient.style.display = 'block';
            descriptionGradient.style.background = 'linear-gradient(to bottom, transparent 70%, white)';
            descriptionGradient.style.bottom = '0';
        } else {
            descriptionText.style.maxHeight = descriptionText.scrollHeight + 'px';
        }
    } else {
        // Açıklama açıksa kapat
        descriptionText.classList.add('line-clamp-2');
        descriptionText.style.maxHeight = '3rem';
        descriptionGradient.style.display = 'block';
        descriptionGradient.style.background = 'linear-gradient(to bottom, transparent, white)';
        toggleButton.innerHTML = '<i class="fas fa-chevron-down"></i>';
    }
} 