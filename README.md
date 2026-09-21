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