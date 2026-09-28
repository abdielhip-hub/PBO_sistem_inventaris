# Sistem Inventaris Toko Buku

Tugas Praktikum Mandiri — **Pemrograman Berorientasi Objek**
Topik: *Property Visibility & Enkapsulasi di Python*

| | |
|---|---|
| Nama | Abdielnaham d'Revan Zhee |
| NIM | 250211060076 |

## Deskripsi

Program CLI (command line) interaktif untuk mengelola sebuah toko buku: inventaris buku, karyawan, penggajian, dan pembelian oleh pelanggan. Fokus utama program adalah penerapan **enkapsulasi**: data penting disembunyikan (private) dan hanya bisa diubah lewat jalur resmi yang tervalidasi.

## Fitur

- Melihat dan menambah buku di inventaris
- Melihat dan menambah karyawan
- Laporan total gaji karyawan (payroll)
- Membeli buku (validasi stok dan saldo)
- Top up saldo pelanggan
- Demo enkapsulasi (menunjukkan atribut private tidak bisa diakses langsung)

## Konsep OOP yang Digunakan

| Konsep | Penerapan |
|---|---|
| Atribut private (`__`) | `Book.__price`, `Book.__stock`, `Account.__balance`, `Employee.__salary`, `Company.__employees`, `Company.__inventory` |
| `@property` dan setter | Harga, stok, saldo, dan gaji divalidasi (tidak boleh negatif / nol) |
| Private method | `Company.__calculate_payroll()` hanya bisa dipanggil dari dalam class, diakses lewat `get_payroll_report()` |
| `isinstance()` | `add_employee()` hanya menerima `Employee`, `add_book()` hanya menerima `Book` |
| Getter aman | `list_employees()` dan `get_books()` mengembalikan salinan list, bukan list aslinya |

## Struktur Class

```
Company ──┬── Employee   (nama, jabatan, __salary)
          └── Book       (judul, penulis, __price, __stock)

Account      (pemilik, __balance) ──► membeli Book lewat purchase_product()
```

## Cara Menjalankan

Pastikan Python 3.12 (atau yang lebih baru) sudah terpasang.

```bash
git clone https://github.com/USERNAME/tugas-pbo-minggu5.git
cd tugas-pbo-minggu5
python toko_buku.py
```

## Contoh Tampilan

```
==============================
  SISTEM INVENTARIS TOKO BUKU
==============================
1. Lihat inventaris buku
2. Tambah buku
3. Lihat karyawan
4. Tambah karyawan
5. Laporan gaji (payroll)
6. Beli buku
7. Top up saldo pelanggan
8. Demo enkapsulasi
0. Keluar

Pilih menu: 6
Nama pelanggan : Noval
Saldo awal      : Rp200000
...
Noval membeli 2x 'Laskar Pelangi' (Rp170,000)
Sisa saldo: Rp30,000
```

## Catatan

Program menyediakan data awal (3 buku dan 2 karyawan) supaya menu langsung bisa dicoba. Data disimpan di memori, sehingga hilang saat program ditutup.
