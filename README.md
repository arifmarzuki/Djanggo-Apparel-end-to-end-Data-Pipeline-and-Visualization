# Project Brief Data Engineering

## 💻 Technical Brief

## Contraints

- Data terpisah berasal dari multiple source seperti db, excel, dan data source yg lain.
- Constraint setiap problem akan spesifik ditentukan pada bagian project description.

### Requirements

- Melakukan pengambilan data, include orchestration, transformation. i.e., ETL 
- Melakukan pengambilan data agregasi dari db + excel 
- Mengambil data secara real time 
- Membuat visualisasi

### Project Description and Expected Delivereble

#### Background

Django Apparel adalah sebuah clothing online store yang sedang berkembang, memiliki tujuan untuk meningkatkan penjualan produk dan memperluas pangsa pasar. Fokus utama perusahaan adalah mengoptimalkan strategi pemasaran koleksi pakaian dengan memanfaatkan data preferensi pelanggan dan tren industri fashion sebagai kunci yang penting.

Melalui platform online, Django Apparel telah mengumpulkan data tentang preferensi pembelian pelanggan, popularitas produk, dan tren industri fashion. Tantangan utama adalah bagaimana memanfaatkan data tersebut secara efektif.

Oleh karena itu, fokus utama Django Apparel saat ini adalah memaksimalkan strategi pemasaran dan penjualan. Dengan memanfaatkan data yang telah terkumpul, perusahaan berharap dapat merancang strategi yang lebih terarah dan efisien. Hal ini meliputi peningkatan penempatan produk, ekspansi ke pasar yang lebih luas untuk meningkatkan revenue, serta memberikan pengalaman belanja yang baik untuk pelanggan setia di platform Django Apparel.

#### Deliverable

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
