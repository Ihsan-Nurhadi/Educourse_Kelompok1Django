$(document).ready(function() {
    // Ketika input box mendapat fokus
    $("input").focus(function() {
        $(this).addClass("input-active");
    });

    // Ketika input box kehilangan fokus
    $("input").blur(function() {
        $(this).removeClass("input-active");
    });

    // Fungsi untuk memecah teks menjadi huruf per huruf dan menampilkannya satu per satu
    function animateHeading() {
        var heading = $("#heading");
        var text = "Create Your Account!"; // Teks yang ingin ditampilkan
        heading.html(""); // Kosongkan teks h2 sebelum animasi dimulai

        // Loop untuk menampilkan huruf satu per satu
        $.each(text.split(""), function(index, letter) {
            setTimeout(function() {
                heading.append(letter); // Tambahkan huruf ke dalam h2
            }, index * 150); // Atur delay 150ms antara setiap huruf
        });
    }

    // Flag untuk memeriksa apakah animasi sudah dijalankan
    var isAnimated = false;

    // Pastikan animasi hanya dijalankan sekali, setelah mouse masuk ke dalam form
    $('.signup-form-container').hover(
        function() {
            // Saat mouse masuk: Tambahkan efek hover dan animasi h2
            $(this).css('transform', 'scale(1.05)');
            $(this).css('box-shadow', '0 4px 15px rgba(0, 0, 0, 0.3)');
            
            // Cek apakah animasi sudah dijalankan, jika belum jalankan
            if (!isAnimated) {
                animateHeading(); // Jalankan animasi pada heading
                isAnimated = true; // Tandai bahwa animasi sudah dijalankan
            }
        }, 
        function() {
            // Saat mouse keluar: Hapus efek hover
            $(this).css('transform', 'scale(1)');
            $(this).css('box-shadow', 'none');
        }
    );
});
