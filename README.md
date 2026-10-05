Nama : Keisha Janice Maulina Napitupulu

NPM : 2506551232

Kelas : PBP A

### Tugas 1

1. Saya menggunakan elemen semantik HTML5 seperti `<header>`, `<main>`, `<section>`, `<article>`, dan `<footer>`. Elemen-elemen tersebut membantu membagi struktur website menjadi bagian yang jelas, seperti profile dan experiences. Penggunaan elemen semantik juga membuat kode lebih teratur, mudah dipahami, dan mendukung aksesibilitas.

2. Tantangan utama dalam membuat tampilan responsive adalah menyesuaikan layout dua kolom pada desktop menjadi satu kolom pada mobile. Saya memprioritaskan nama dan identitas di bagian atas, kemudian foto, deskripsi, dan informasi lainnya. Saya menggunakan media query untuk mengatur ukuran font, jarak antar elemen, ukuran foto, serta mencegah terjadinya horizontal scrolling.

3. Karena website ini masih berupa static web, informasi profile dan experiences masih ditulis langsung di dalam HTML. Perubahan data harus dilakukan secara manual dan website belum memiliki database maupun fitur pengelolaan konten. Pada iterasi berikutnya, saya ingin menambahkan model database untuk menyimpan profile, experiences, dan projects, serta menggunakan Django Admin untuk mengelola data tersebut secara dinamis.

### AI Disclosure

Saya menggunakan GitHub Copilot untuk membantu memberikan saran mengenai struktur HTML, styling CSS, responsive layout, dan penyelesaian masalah horizontal scrolling. Saya tetap menyesuaikan kode secara manual berdasarkan hasil tampilan dan kebutuhan website. Beberapa saran AI juga perlu diperbaiki, terutama terkait aturan CSS yang terduplikasi dan penyesuaian static file Django.

### Tugas 2

1. Ketika pengguna membuka halaman `/skills/`, request dari browser akan masuk ke `myportofolio/urls.py` terlebih dahulu, lalu diteruskan ke `main/urls.py`. Setelah itu, URL tersebut akan memanggil view `show_skill` yang mengambil data dari model `Skill` di database. Data tersebut kemudian dikirim ke template `skill.html` melalui context. Template akan menampilkan data tersebut menggunakan Django Template Language, lalu hasilnya dikirim kembali ke browser.

2. Data portfolio sebaiknya disimpan di model agar tidak perlu ditulis satu per satu di dalam template. Dengan begitu, kalau ingin menambah atau mengubah data, saya cukup mengubah data di database tanpa harus mengubah HTML. Hal ini membuat website lebih mudah dirawat dan dikembangkan jika datanya semakin banyak.

3. `makemigrations` digunakan untuk membuat file yang mencatat perubahan pada model, sedangkan `migrate` digunakan untuk menerapkan perubahan tersebut ke database. Contohnya, saat saya menambahkan model `Skill` dengan field `name`, `description`, dan `level`, saya menjalankan kedua perintah tersebut agar model `Skill` bisa dibuat di database. Hal yang sama dilakukan saat saya menambahkan field `organization` pada model `Experience`.

### AI Disclosure

Saya menggunakan ChatGPT dan GitHub Copilot selama pengerjaan tugas ini. ChatGPT saya gunakan untuk membantu memahami konsep Django dan menjelaskan langkah pengerjaan, seperti hubungan antara model, view, URL, dan template, serta membantu mengecek error pada kode dan testing. Saya juga menggunakan ChatGPT untuk berdiskusi mengenai struktur model `Skill`, pembuatan halaman `/skills/`, dan penulisan unit test. GitHub Copilot digunakan sebagai bantuan saat menulis dan melengkapi beberapa bagian kode. Setelah mendapatkan saran dari AI, saya menyesuaikan kembali kode dengan struktur project yang saya buat dan menjalankan testing sendiri untuk memastikan hasilnya sesuai. 

### Tugas 3

1. `ModelForm` digunakan agar form yang dibuat terhubung langsung dengan model Django. Dengan `ModelForm`, field pada form dapat dibuat berdasarkan field yang ada di model, sehingga saya tidak perlu membuat setiap input HTML dan validasinya secara manual. Pada tugas ini, saya menggunakan `ExperienceForm` yang terhubung dengan model `Experience`, sehingga data yang dimasukkan melalui form dapat langsung disimpan ke database. Sementara itu, `{% csrf_token %}` digunakan pada form dengan method `POST` untuk melindungi website dari serangan Cross-Site Request Forgery (CSRF). Token ini membantu Django memastikan bahwa request yang dikirim berasal dari form yang valid pada website.

2. JSON lebih banyak digunakan dalam pengembangan web modern karena formatnya sederhana, ringan, dan mudah dibaca oleh manusia maupun program. JSON juga mudah digunakan untuk mengirim data antara server dan client karena strukturnya mirip dengan object yang umum digunakan dalam JavaScript. Dibandingkan XML, JSON memiliki penulisan yang lebih singkat karena tidak membutuhkan tag pembuka dan penutup untuk setiap data. Oleh karena itu, JSON lebih praktis digunakan untuk pertukaran data dalam aplikasi web.

3. Ketika view `get_experiences_json` dipanggil, Django mengambil data `Experience` dari database menggunakan `Experience.objects.all()`. Data tersebut kemudian diubah menjadi JSON menggunakan `serializers.serialize("json", experiences)` dan dikembalikan kepada client menggunakan `HttpResponse` dengan `content_type="application/json"`. Setelah itu, pada view `show_experience`, data JSON tersebut diambil kembali dan diproses menggunakan `serializers.deserialize()`. Hasilnya berupa object Django yang kemudian dimasukkan ke dalam context dan ditampilkan pada `experience.html`. Serialization diperlukan karena data yang diambil dari database masih berupa object/model Django dan tidak dapat langsung dikirim dalam format JSON. Dengan serialization, data tersebut diubah menjadi format JSON sehingga dapat dikirim melalui HTTP dan diproses kembali oleh aplikasi..
   
### AI Disclosure

Saya menggunakan ChatGPT dan GitHub Copilot selama pengerjaan Tugas 3. ChatGPT membantu saya memahami requirement tugas dan menjelaskan konsep seperti ModelForm, CSRF token, serialization, dan deserialization. ChatGPT juga membantu saya mengecek dan memperbaiki bagian views.py, urls.py, serta template HTML, terutama saat membuat fitur Create, Update, Delete, dan JSON Data Delivery. GitHub Copilot saya gunakan untuk membantu menulis dan melengkapi beberapa bagian kode. Setelah mendapatkan bantuan dari AI, saya tetap menyesuaikan kode dengan struktur project saya dan mencoba memahami setiap perubahan yang dilakukan. Saya juga melakukan testing secara langsung menggunakan python manage.py runserver, termasuk mencoba menambah, mengubah, dan menghapus data Experience, membuka endpoint JSON, melakukan filtering berdasarkan judul Experience, serta memastikan data JSON dapat di-deserialize dan ditampilkan kembali di halaman Experience.

### Tugas 4

Pada Tugas 4, saya menambahkan fitur authentication, session, cookies, authorization, role Editor, dan fitur star pada website portfolio.

1. Saya menggunakan sistem authentication bawaan Django untuk membuat fitur registrasi, login, dan logout. Pengguna yang belum login masih dapat melihat data portfolio, tetapi harus login untuk melakukan aksi yang membutuhkan akun. Saya juga menggunakan session untuk menyimpan status login dan cookie `last_login` untuk menyimpan waktu login terakhir.

2. Saya menerapkan pembagian hak akses berdasarkan role. Pengguna biasa hanya dapat melihat data dan memberikan atau membatalkan star. Editor dapat melakukan hal yang sama dan juga dapat mengubah data, tetapi tidak dapat membuat atau menghapus data. Sementara itu, superuser dapat membuat, mengubah, dan menghapus data. Role Editor dibuat menggunakan Django Group/Permission.

3. Pembatasan akses tidak hanya dilakukan pada template dengan menyembunyikan tombol yang tidak boleh digunakan, tetapi juga dilakukan pada view. Dengan begitu, pengguna yang tidak memiliki izin tetap tidak dapat menjalankan aksi tersebut meskipun mencoba mengakses URL secara langsung.

4. Saya menambahkan fitur star yang hanya dapat digunakan oleh pengguna yang sudah login. Fitur ini menggunakan `ManyToManyField` dengan model User sehingga satu pengguna tidak dapat memberikan lebih dari satu star pada data yang sama. Pengguna juga dapat membatalkan star dan melihat jumlah total star serta status star mereka. Proses star menggunakan method `POST` dan dilindungi dengan `{% csrf_token %}`.

5. Endpoint JSON dari Tugas 3 tetap dipertahankan dan dapat digunakan tanpa menampilkan informasi sensitif. Saya juga memastikan project dapat dijalankan menggunakan `python manage.py runserver` dan melakukan testing pada fitur login, logout, pembagian role, CRUD, star, dan endpoint JSON.

### AI Disclosure

Pada Tugas 4, saya menggunakan ChatGPT dan GitHub Copilot sebagai bantuan selama proses pengerjaan. ChatGPT saya gunakan untuk memahami konsep authentication, session, cookies, authorization, Django Group/Permission, dan `ManyToManyField`, serta membantu ketika saya menemukan error pada kode.

Saya biasanya memberikan potongan kode atau error yang saya temui, kemudian meminta penjelasan mengenai penyebabnya dan bagian yang perlu diperbaiki. ChatGPT juga membantu saya saat mengerjakan bagian `models.py`, `views.py`, `urls.py`, dan template untuk fitur login, role Editor, pembatasan akses, dan star.

GitHub Copilot saya gunakan untuk memberikan saran dan melengkapi beberapa bagian kode. Namun, kode dari AI tidak langsung saya gunakan. Saya tetap menyesuaikannya dengan struktur project yang saya buat dan mengecek kembali apakah hasilnya sudah sesuai dengan requirement tugas.

Setelah melakukan perubahan, saya menjalankan project dan mencoba fitur-fiturnya secara langsung. Beberapa saran dari AI juga perlu saya ubah karena tidak selalu sesuai dengan struktur kode yang saya gunakan. Jadi, AI saya gunakan sebagai bantuan untuk memahami konsep, mencari solusi saat menemukan masalah, dan membantu proses coding, sedangkan implementasi dan testing akhirnya saya lakukan sendiri.

### Tugas 5

Pada Tugas 5, saya menerapkan AJAX pada halaman Experience dan Skills untuk memuat data, melakukan pencarian, dan menambahkan data melalui modal tanpa me-reload halaman.

1. Debouncing adalah teknik untuk menunda pemanggilan fungsi sampai pengguna berhenti melakukan aktivitas selama waktu tertentu. Pada pencarian, saya menggunakan jeda 300 milidetik setelah pengguna berhenti mengetik. Jika pengguna mengetik lagi, timer sebelumnya dibatalkan. Teknik ini mengurangi request yang tidak diperlukan karena pencarian tidak dijalankan untuk setiap karakter.

2. `await` digunakan untuk menunggu Promise selesai sebelum menjalankan baris berikutnya dalam fungsi async. `await fetch()` menghasilkan objek Response, sedangkan `await response.json()` menghasilkan data JSON yang sudah dibaca. Tanpa `await`, hasilnya masih berupa Promise sehingga tidak bisa langsung diperlakukan sebagai Response atau data JSON. Promise juga dapat ditangani menggunakan `.then()`.

3. XSS adalah serangan yang menyisipkan kode berbahaya agar dijalankan oleh browser pengguna. Django melakukan autoescaping pada template secara default, sedangkan data JSON yang dimasukkan melalui `innerHTML` harus di-escape sendiri. Saya menggunakan `escapeHtml()` untuk teks pada kartu dan `textContent` untuk pesan toast. Di sisi server, `strip_tags()` membersihkan tag HTML melalui method `clean_<field>` pada ModelForm, kemudian field wajib yang menjadi kosong ditolak.

#### Implementasi

- Halaman daftar merender kerangka, lalu mengambil data menggunakan `fetch()`. JSON disusun secara manual dengan `JsonResponse`, termasuk jumlah star dan status star pengguna.
- Halaman menyediakan kondisi loading, data kosong, dan error. Pencarian menggunakan debounce 300 milidetik serta pembatalan request sebelumnya dengan `AbortController`.
- Form tambah data berada dalam modal dan dikirim menggunakan `FormData` beserta token CSRF. Server memvalidasi input menggunakan ModelForm dan mengembalikan status 201, 400, atau 403.
- Setelah data ditambahkan, daftar diperbarui melalui AJAX. Toast menampilkan keberhasilan atau pesan kesalahan dari server.
- Hak akses tetap diperiksa di view. Editor dan superuser dapat mengedit data, sedangkan penambahan dan penghapusan hanya dapat dilakukan oleh superuser.
- Pengunjung dapat melihat jumlah star. Aksi Star/Unstar membutuhkan login.

#### Pengujian

Pengecekan Django dan tes otomatis dijalankan dengan:

```powershell
python manage.py check
python manage.py test main
```

Tes mencakup akses halaman, endpoint JSON, pencarian, validasi input, sanitasi HTML, hak akses, CSRF, edit Skill, dan fitur star.

Pengujian browser mencakup loading, pencarian, modal, toast, serta tampilan untuk setiap peran. Kondisi error diperiksa menggunakan mode Offline pada DevTools. Perlindungan XSS diperiksa dengan input `<img src="x" onerror="alert('XSS!')">`, yang harus ditolak pada field wajib setelah sanitasi dan tidak boleh memunculkan alert.

#### AI Disclosure

Dalam pengerjaan Tugas 5, saya menggunakan ChatGPT untuk berdiskusi mengenai penerapan AJAX dan membantu meninjau beberapa bagian kode. Pembahasan mencakup validasi form, respons JSON, pencarian dengan debounce, hak akses, pengujian, dan dokumentasi. Saya memberikan potongan kode atau pesan error sebagai konteks untuk mendapatkan penjelasan dan saran perbaikan.

Penjelasan dan saran kode tersebut saya sesuaikan dengan struktur proyek sebelum diterapkan. Beberapa saran memerlukan penyesuaian karena tidak langsung sesuai dengan implementasi yang sudah ada. Perubahan dilakukan secara bertahap dan dicatat melalui commit yang menjelaskan masing-masing perubahan.