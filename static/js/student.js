function filterContent(category) {
    // Ambil semua elemen dengan class "card"
    const cards = document.querySelectorAll('.card');
  
    // Loop melalui setiap elemen card
    cards.forEach(card => {
      // Cek kategori dari data-category setiap card
      if (category === 'All' || card.getAttribute('data-category') === category) {
        // Tampilkan card jika kategorinya cocok atau "Semua" dipilih
        card.classList.remove('hidden');
      } else {
        // Sembunyikan card jika kategorinya tidak cocok
        card.classList.add('hidden');
      }
    });
  }
  window.onload = () =>{
    filterProduct("All");
}
const teachers = [
  {
      name: "Sarifudin",
      subject: "Kimia",
      img: "img/teacher1.jpg",
      schedule: "Senin - Jumat, 09:00 - 16:00",
      lastUpdated: "3 mins ago"
  },
  {
      name: "Sarah",
      subject: "Biologi",
      img: "img/teacher2.jpeg",
      schedule: "Senin - Jumat, 10:00 - 17:00",
      lastUpdated: "4 mins ago"
  },
  {
      name: "Bunga",
      subject: "Fisika",
      img: "img/teacher3.jpg",
      schedule: "Senin - Jumat, 08:00 - 18:00",
      lastUpdated: "3 mins ago"
  },
  {
      name: "Bella",
      subject: "Matematika",
      img: "img/teacher4.jpg",
      schedule: "Senin - Jumat, 09:00 - 18:00",
      lastUpdated: "3 mins ago"
  },
  {
      name: "Andi",
      subject: "Matematika",
      img: "img/teacher5.jpg",
      schedule: "Senin - Jumat, 15:00 - 21:00",
      lastUpdated: "20 mins ago"
  },
  {
      name: "Florensia",
      subject: "Kimia",
      img: "img/teacher6.jpg",
      schedule: "Senin - Jumat, 16:00 - 21:00",
      lastUpdated: "8 mins ago"
  },
  {
      name: "Margareta",
      subject: "Biologi",
      img: "img/teacher7.jpg",
      schedule: "Senin - Jumat, 14:00 - 20:00",
      lastUpdated: "10 mins ago"
  },
  {
      name: "Fransiska",
      subject: "Fisika",
      img: "img/teacher8.jpg",
      schedule: "Senin - Jumat, 08:00 - 17:00",
      lastUpdated: "20 mins ago"
  },
  {
      name: "Bryant",
      subject: "Matematika",
      img: "img/teacher9.jpg",
      schedule: "Senin - Jumat, 09:00 - 19:00",
      lastUpdated: "4 mins ago"
  },
  {
      name: "Steven",
      subject: "Fisika",
      img: "img/teacher10.jpg",
      schedule: "Senin - Jumat, 08:00 - 16:00",
      lastUpdated: "8 mins ago"
  },
  {
      name: "Aliya",
      subject: "Biologi",
      img: "img/teacher11.jpeg",
      schedule: "Senin - Jumat, 15:00 - 21:00",
      lastUpdated: "8 mins ago"
  },
  {
      name: "Nathania",
      subject: "Kimia",
      img: "img/teacher12.jpeg",
      schedule: "Senin - Jumat, 08:00 - 18:00",
      lastUpdated: "8 mins ago"
  }
];

const teacherListElement = document.getElementById('teacher-list');

teachers.forEach(teacher => {
  const card = `
      <div class="card mb-3" style="max-width: 1080px;" data-category="${teacher.subject}">
          <div class="row g-0">
              <div class="col-md-4">
                  <img src="${staticUrl}${teacher.img}" class="img-fluid rounded" alt="${teacher.name}">
              </div>
              <div class="col-md-8">
                  <div class="card-body">
                      <h5 class="card-title">${teacher.name}</h5>
                      <p class="card-text">Saya Adalah Guru ${teacher.subject}</p>
                      <p class="card-text"><small class="text-body-secondary">Last updated ${teacher.lastUpdated}</small></p>
                      <p class="card-text">Jadwal Tersedia: ${teacher.schedule}</p>
                      <button class="btn btn-primary mt-2">Pesan Guru</button>
                  </div>
              </div>
          </div>
      </div>
  `;
  teacherListElement.innerHTML += card;
});