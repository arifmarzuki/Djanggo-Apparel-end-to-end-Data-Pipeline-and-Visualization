# Project Brief Template Data Engineering

## 💻 Technical Brief

## Contraints

- Data terpisah berasal dari multiple source seperti db, excel, dan data source yg lain.
- Constraint setiap problem akan spesifik ditentukan pada bagian project description.

### Requirements

- Melakukan pengambilan data, include orchestration, transformation. i.e., ETL) (Mandatory)
- Melakukan pengambilan data agregasi dari db + excel (Mandatory)
- Melakukan penerapan replication & sharding (Poin plus)
- Mengambil data secara real time (Poin plus)
- Membuat visualisasi (Poin plus)

### Project Description and Expected Delivereble

#### Background

Django Apparel adalah sebuah clothing online store yang sedang berkembang, memiliki tujuan untuk meningkatkan penjualan produk dan memperluas pangsa pasar. Fokus utama perusahaan adalah mengoptimalkan strategi pemasaran koleksi pakaian dengan memanfaatkan data preferensi pelanggan dan tren industri fashion sebagai kunci yang penting.

Melalui platform online, Django Apparel telah mengumpulkan data tentang preferensi pembelian pelanggan, popularitas produk, dan tren industri fashion. Tantangan utama adalah bagaimana memanfaatkan data tersebut secara efektif.

Oleh karena itu, fokus utama Django Apparel saat ini adalah memaksimalkan strategi pemasaran dan penjualan. Dengan memanfaatkan data yang telah terkumpul, perusahaan berharap dapat merancang strategi yang lebih terarah dan efisien. Hal ini meliputi peningkatan penempatan produk, ekspansi ke pasar yang lebih luas untuk meningkatkan revenue, serta memberikan pengalaman belanja yang baik untuk pelanggan setia di platform Django Apparel.

#### Expected Deliverable

1. Create DAG's untuk ingest [data ini](/dataset/) ke postgres menggunakan Airflow
2. Ekspetasi data yang di ingest terbuat sebanyak 7 table
3. Transform data untuk membuat kimball data modeling dengan requirements sebagai berikut
    - Dimension layer
        - dim_products
        - dim_customers
        - dim_locations
    - Fact layer
        - fct_transactions
    - Datamart layer
        - dm_perfomance_product_by_cities
        - dm_revenue_by_months

#### Success Criteria

1. Sukses ingest data dari beberapa format file ke database menggunakan airflow.
2. Berhasil membuat layering data model dengan joinan table yang tepat.
3. Berhasil menyajikan isi data dalam data modeling sesuai requirements.

#### Documentation

Link referensi untuk kimball data modelling https://www.youtube.com/watch?v=gRE3E7VUzRU&t=653s

#### Assest

[Dataset untuk di ingest](/dataset/)

## 📆 Schedule Meeting and Format Mentoring

### Schedule Mentoring

- Mentoring dilakukan 3x dalam sepekan dengan alokasi 60 menit mentoring tiap sesi.
- Jadwal Mentoring dapat menyesuaikan jadwal mentor dan disepakati bersama dengan team, jika ada perubahan mentor dan tim terkait bisa langsung mengkomunikasikan.
- Mentoring bisa dilakukan hari senin-jumat atau sabtu-minggu sesuai availability mentor dan team.

### Mentoring Alocation

| Mentoring | Allocation Time | Agenda                                                      |
| --------- | --------------- | ----------------------------------------------------------- |
| Part 1    | 15 minutes      | Update Team in General                                      |
|           |                 | Update Every Member of The Team                             |
|           |                 | Showing Progress Based On Project Management Tools (Trello) |
| Part 2    | 45 minutes      | Discussion topics according to the problem at hand          |

## ⚠️ General Rules

### Hal-hal yang harus dilakukan oleh Mentees dan Team

- Setiap individu wajib berkontribusi & aktif berkomunikasi dalam team (yang tidak berkontribusi maka tidak mendapatkan nilai, nilai diberikan kenapa yang berkontribusi aktif).
- Setiap team wajib memiliki group komunikasi (membuat group telegram).
- Setiap team wajib menggunakan trello untuk management task & membagi task dg proporsional setiap member.
- Setiap team wajib mengadakan daily meeting setiap hari untuk berkoordinasi.

### Tindakan yang dianggap sebagai pelanggaran bagi Mentees dan Team

- Individu yang tidak aktif atau slow response dalam berkomunikasi dg tim (tidak membalas komunikasi team lebih dari 2 jam saat jam aktif: 9 am - 9 pm).
- Individu tidak ikut berkontribusi dalam mengerjakan task.
- Tim yang tidak membuat group komunikasi.
- Tim tidak menggunakan trello.
- Tim tidak melakukan pembagian tugas.
- Tim yang tidak mengadakan daily meeting.
