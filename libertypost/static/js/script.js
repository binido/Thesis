document.addEventListener('DOMContentLoaded', () => {
    const burgerMenu = document.querySelector('.burger-menu');
    const mobileMenu = document.querySelector('.mobile-menu');
    const scrollTopButton = document.querySelector('.scroll-top');
    const body = document.body;
    const header = document.querySelector('header');
    let lastScroll = 0;

    burgerMenu.addEventListener('click', (e) => {
        e.stopPropagation();
        mobileMenu.classList.toggle('active');
        burgerMenu.classList.toggle('active');
    });

    document.addEventListener('click', (e) => {
        if (!mobileMenu.contains(e.target) && !burgerMenu.contains(e.target)) {
            mobileMenu.classList.remove('active');
            burgerMenu.classList.remove('active');
        }
    });

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 300) {
            scrollTopButton.classList.add('visible');
        } else {
            scrollTopButton.classList.remove('visible');
        }

        if (currentScroll > lastScroll && currentScroll > 60) {
            header.style.transform = 'translateY(-100%)';
        } else {
            header.style.transform = 'translateY(0)';
        }

        lastScroll = currentScroll;
    });

    scrollTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    const textarea = document.querySelector('textarea[name="comment"]');
    const submitButton = document.querySelector('input[type="submit"]');

    if (textarea && submitButton) {
        textarea.addEventListener('input', function() {
            submitButton.disabled = this.value.length < 10;
        });
    }

    const fileInput = document.getElementById('file-upload');
    const fileName = document.querySelector('.file-name');

    if (fileInput && fileName) {
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                fileName.textContent = this.files[0].name;
            } else {
                fileName.textContent = '';
            }
        });
    }
});

function copyLink(link) {
    const tempInput = document.createElement('input');
    tempInput.value = link;
    document.body.appendChild(tempInput);
    
    tempInput.select();
    document.execCommand('copy');
    
    document.body.removeChild(tempInput);
    
    const toast = document.querySelector('.toast');
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 2000);
} 
