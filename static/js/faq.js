function showFAQ(category) {
    // Hide all sections
    $('#faq-umum').hide();
    $('#faq-guru').hide();
    $('#faq-murid').hide();

    // Show selected category
    $('#faq-' + category).show();
}

$('.faq-question').on('click', function() {
    const answer = $(this).next();
    answer.stop(true, true).slideToggle(300);//animasi dropdown
});

