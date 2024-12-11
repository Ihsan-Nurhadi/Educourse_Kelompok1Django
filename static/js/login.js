$(document).ready(function() {
    // Fungsi untuk memecah teks menjadi huruf per huruf dan menampilkannya satu per satu
    function animateHeading() {
        var heading = $("#heading");
        var text = "Login Your Account!"; // Setel teks langsung yang ingin ditampilkan
        heading.html(""); // Kosongkan konten sebelumnya

        // Loop untuk menampilkan huruf satu per satu
        $.each(text.split(""), function(index, letter) {
            setTimeout(function() {
                heading.append(letter); // Menambahkan huruf ke dalam elemen h2
            }, index * 100); // Jeda 100ms antara setiap huruf
        });
    }

    // Menjalankan animasi saat halaman dimuat
    animateHeading();

    // Ketika input box mendapat fokus
    $("input").focus(function() {
        $(this).addClass("input-active");
    });

    // Ketika input box kehilangan fokus
    $("input").blur(function() {
        $(this).removeClass("input-active");
    });

    // Efek hover pada form
    $('.login-form-container').hover(
        function() {
            // Saat mouse masuk
            $(this).css('transform', 'scale(1.05)');
            $(this).css('box-shadow', '0 4px 15px rgba(0, 0, 0, 0.3)');
        }, 
        function() {
            // Saat mouse keluar
            $(this).css('transform', 'scale(1)');
            $(this).css('box-shadow', 'none');
        }
    );
});
