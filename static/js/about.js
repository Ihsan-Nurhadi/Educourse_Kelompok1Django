$(document).ready(function () {
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top < window.innerHeight &&
            rect.bottom > 0 &&
            rect.left >= 0 &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    function checkVisibility() {
        $('.fade-in').each(function () {
            if (isElementInViewport(this)) {
                $(this).addClass('visible');
            } else {
                $(this).removeClass('visible'); 
            }
        });
    }

    // Initial check
    checkVisibility();

    let timeout;
    $(window).on('scroll', function () {
        clearTimeout(timeout);
        timeout = setTimeout(checkVisibility, 200); 
    });
});
