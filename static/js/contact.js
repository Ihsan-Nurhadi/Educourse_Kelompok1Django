$(document).ready(function(){
    $('.contact-form').on('submit', function(event) {
        event.preventDefault(); // Mencegah form dikirim secara default

        // Mengecek apakah semua input di form telah diisi
        var isValid = true;
        $('.contact-form input, .contact-form textarea').each(function() {
            if ($(this).val() === '') {
                isValid = false;
            }
        });

        if (isValid) {
            alert("Terima kasih atas partisipasinya");
            // Setelah menampilkan alert, Anda bisa mengirim form secara manual atau melakukan aksi lain.
            // Contoh: $(this).unbind('submit').submit(); // Mengirim form secara normal
        } else {
            alert("Harap isi semua field.");
        }
    });
});