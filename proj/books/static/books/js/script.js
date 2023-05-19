
  const prevButton = document.querySelector('#prev-button');
  const nextButton = document.querySelector('#next-button');
  const carousel = document.querySelector('.main_carousel');

  let currentIndex = 0;

  const images = [
        'https://simg.marwin.kz/media/wysiwyg/dynamic/23/blagosolovenie-nebozhitelej-4-2.jpg',
        'https://simg.marwin.kz/media/wysiwyg/dynamic/23/monopoliya-igra-stavshaya-legendoj2.jpg',
        'https://simg.marwin.kz/media/wysiwyg/dynamic/23/40-na-assortiment-populyarnogo-non-fikshna2.jpg',
        'https://simg.marwin.kz/media/wysiwyg/dynamic/23/kvartiranti2.jpg'
  ];

  prevButton.addEventListener('click', () => {
    currentIndex--;

    if (currentIndex < 0) {
      currentIndex = images.length - 1;
    }

    carousel.querySelector('img').src = images[currentIndex];
  });

  nextButton.addEventListener('click', () => {
    currentIndex++;

    if (currentIndex >= images.length) {
      currentIndex = 0;
    }

    carousel.querySelector('img').src = images[currentIndex];
  });
