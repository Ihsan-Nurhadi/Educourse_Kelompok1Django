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
          var text = heading.text().trim(); // teks h2
          heading.html(""); // Kosongkan h2

          // Loop untuk menampilkan huruf satu per satu
          $.each(text.split(""), function(index, letter) {
              setTimeout(function() {
                  heading.append(letter); // Tambahkan huruf ke dalam h2
              }, index * 100); // Atur delay 100ms antara setiap huruf
          });
      }

      // Efek hover pada form
      $('.login-form-container').hover(
          function() {
              // Saat mouse masuk: Tambahkan efek hover dan animasi h2
              $(this).css('transform', 'scale(1.05)');
              $(this).css('box-shadow', '0 4px 15px rgba(0, 0, 0, 0.3)');
              animateHeading(); // Jalankan animasi pada heading
          }, 
          function() {
              // Saat mouse keluar: Hapus efek hover
              $(this).css('transform', 'scale(1)');
              $(this).css('box-shadow', 'none');
          }
      );
  });