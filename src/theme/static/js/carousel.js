(() => {
    const carousel = document.getElementById('carousel');
    const indicators = document.getElementById('indicators').children;
    const totalSlides = carousel.children.length;
    let currentIndex = 0;

    function updateCarousel() {
        carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
        for (let i = 0; i < indicators.length; i++) {
            indicators[i].classList.toggle('opacity-75', i === currentIndex);
            indicators[i].classList.toggle('opacity-50', i !== currentIndex);
        }
    }

    document.getElementById('prev').onclick = () => {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateCarousel();
    };

    document.getElementById('next').onclick = () => {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateCarousel();
    };

    // Clique nos indicadores para navegar direto
    for (let i = 0; i < indicators.length; i++) {
        indicators[i].onclick = () => {
            currentIndex = i;
            updateCarousel();
        };
    }

    // Auto play (opcional)
    setInterval(() => {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateCarousel();
    }, 5000);

    updateCarousel();
})();
