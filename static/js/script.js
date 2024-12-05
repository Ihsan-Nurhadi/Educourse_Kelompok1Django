// Fungsi yang akan dijalankan ketika halaman selesai dimuat
window.onload = function() {
//    alert ("Welcome to EduTech");
//     // Tampilkan prompt bawaan browser untuk meminta nama
//     var userName = prompt("Masukkan Nama Anda:");

//     // Jika pengguna memasukkan nama, tampilkan di navbar
//     if (userName) {
//         document.getElementById('userNameDisplay').innerText = "Hallo, " + userName + "!"; // Tampilkan nama di navbar
//        // document.getElementById('greetingMessage').innerText = "Selamat Datang, " + userName + "!"; // Ubah pesan ucapan
//     } else {
//         alert("Anda belum memasukkan nama!"); // Berikan peringatan jika nama kosong
//     }
    //animasi slide comany section
    function animate($element){
        const elementWidth = $element.outerWidth(); 
        const parentWidth = $element.parent().outerWidth(); 
        let flag = 0; 
  
        setInterval(function() {
            $element.css("margin-left", --flag + "px");
            //jika elemen sudah bergerak melawati batas kiri (diluar layar),reset ke kanan
            if (flag <= -elementWidth) {
                flag = parentWidth; //reset elemen ke sisi kanan parent
            }
        }, 5);//interval untuk mengatur animasi
    }
    const $company = $("#company");
    animate($company);
}
//menampilkan konten yang terembunyi
$(document).ready(function () {
    $('#btn').click(function () {
        //Cek apakah elemen '.secondary' terlihat atau tidak
        if ($('.secondary').is(':visible')) {
            $('.secondary').slideUp();//animasi naik untuk menyembunyikan
            $('#btn').text("Show More Details")//ubah tek tombol
        } else {
            $('.secondary').slideDown();//animassi turun untuk menampilkan
            $('#btn').text('Hide Content')//ubah teks tombol
        }
    })
})
//scrolling animation
const observer = new IntersectionObserver((entries)=>{
    entries.forEach((entry)=>{
        console.log(entry)
        if (entry.isIntersecting) {
            $(entry.target).addClass('show')
        }
    });
})

const hiddenElements = $(".container");
hiddenElements.each((i, el) => observer.observe(el));