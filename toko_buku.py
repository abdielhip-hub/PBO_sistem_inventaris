"""
Tugas Praktikum Mandiri
Mata Kuliah : Pemrograman Berorientasi Objek
Topik       : Property Visibility & Enkapsulasi di Python
Tema        : Sistem Inventaris Toko Buku
"""


# =====================================================
#                      CLASS
# =====================================================
class Book:

    def __init__(self, title: str, author: str, price: int, stock: int):
        self.title = title          
        self.author = author        
        self.__price = 0            
        self.__stock = 0            
        self.price = price          
        self.stock = stock          

    @property
    def price(self) -> int:
        return self.__price

    @price.setter
    def price(self, value: int):
        if value <= 0:
            raise ValueError("Harga buku harus lebih dari 0!")
        self.__price = value

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, value: int):
        if value < 0:
            raise ValueError("Stok tidak boleh negatif!")
        self.__stock = value

    def __str__(self) -> str:
        return f"'{self.title}' - {self.author} | Rp{self.price:,} | stok: {self.stock}"


class Account:

    def __init__(self, owner: str, balance: int = 0):
        self.owner = owner
        self.__balance = 0
        self.balance = balance

    @property
    def balance(self) -> int:
        return self.__balance

    @balance.setter
    def balance(self, amount: int):
        if amount < 0:
            raise ValueError("Saldo tidak boleh negatif!")
        self.__balance = amount

    def top_up(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Jumlah top up harus lebih dari 0!")
        self.balance = self.__balance + amount

    def purchase_product(self, book: Book, qty: int = 1) -> None:
        """Validasi dulu (tipe, qty, stok, saldo), baru ubah data."""
        if not isinstance(book, Book):
            raise TypeError("Hanya objek Book yang bisa dibeli!")
        if qty <= 0:
            raise ValueError("Jumlah pembelian harus lebih dari 0!")
        if qty > book.stock:
            raise ValueError(f"Stok '{book.title}' tidak cukup (sisa {book.stock})!")

        total = book.price * qty
        if total > self.__balance:
            raise ValueError(
                f"Saldo tidak cukup! Butuh Rp{total:,}, saldo Rp{self.__balance:,}"
            )

        self.__balance -= total
        book.stock -= qty
        print(f"{self.owner} membeli {qty}x '{book.title}' (Rp{total:,})")


class Employee:

    def __init__(self, name: str, position: str, salary: int):
        self.name = name
        self.position = position
        self.__salary = 0
        self.salary = salary

    @property
    def salary(self) -> int:
        return self.__salary

    @salary.setter
    def salary(self, value: int):
        if value <= 0:
            raise ValueError("Gaji harus lebih dari 0!")
        self.__salary = value

    def __str__(self) -> str:
        return f"{self.name} ({self.position}) - Rp{self.salary:,}"


class Company:
    """Toko Buku: mengelola karyawan & inventaris secara terenkapsulasi."""

    def __init__(self, name: str):
        self.name = name
        self.__employees = []       
        self.__inventory = []       

    # ---------- Karyawan ----------
    def add_employee(self, employee) -> None:
        if not isinstance(employee, Employee):      
            raise TypeError("Hanya objek Employee yang boleh ditambahkan!")
        self.__employees.append(employee)
        print(f"Karyawan ditambahkan: {employee.name}")

    def list_employees(self) -> list:
        """Kembalikan salinan agar list asli tidak bisa dimodifikasi dari luar."""
        return list(self.__employees)

    def __calculate_payroll(self) -> int:
        """Private method: hanya bisa dipanggil dari dalam class."""
        return sum(emp.salary for emp in self.__employees)

    def get_payroll_report(self) -> str:
        """Public method sebagai 'pintu resmi' ke __calculate_payroll()."""
        total = self.__calculate_payroll()
        return (
            f"Total gaji {len(self.__employees)} karyawan "
            f"di {self.name}: Rp{total:,}"
        )

    # ---------- Inventaris ----------
    def add_book(self, book) -> None:
        if not isinstance(book, Book):
            raise TypeError("Hanya objek Book yang boleh masuk inventaris!")
        self.__inventory.append(book)
        print(f"Buku ditambahkan: {book.title}")

    def get_books(self) -> list:
        """Kembalikan salinan list buku."""
        return list(self.__inventory)

    def show_inventory(self) -> None:
        print(f"\n=== Inventaris {self.name} ===")
        if not self.__inventory:
            print("(kosong)")
        for i, book in enumerate(self.__inventory, start=1):
            print(f"{i}. {book}")


# =====================================================
#                   HELPER INPUT
# =====================================================
def input_teks(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input tidak boleh kosong!")


def input_angka(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Masukkan angka bulat yang valid!")


# =====================================================
#                   FITUR MENU
# =====================================================
def menu_tambah_buku(toko: Company) -> None:
    print("\n--- Tambah Buku ---")
    judul = input_teks("Judul   : ")
    penulis = input_teks("Penulis : ")
    harga = input_angka("Harga   : Rp")
    stok = input_angka("Stok    : ")
    toko.add_book(Book(judul, penulis, harga, stok))


def menu_tambah_karyawan(toko: Company) -> None:
    print("\n--- Tambah Karyawan ---")
    nama = input_teks("Nama    : ")
    jabatan = input_teks("Jabatan : ")
    gaji = input_angka("Gaji    : Rp")
    toko.add_employee(Employee(nama, jabatan, gaji))


def menu_lihat_karyawan(toko: Company) -> None:
    print(f"\n=== Karyawan {toko.name} ===")
    karyawan = toko.list_employees()
    if not karyawan:
        print("(belum ada karyawan)")
    for i, emp in enumerate(karyawan, start=1):
        print(f"{i}. {emp}")


def buat_akun_pelanggan() -> Account:
    print("\nBelum ada akun pelanggan, buat dulu.")
    nama = input_teks("Nama pelanggan : ")
    saldo = input_angka("Saldo awal      : Rp")
    return Account(nama, saldo)


def menu_beli_buku(toko: Company, sesi: dict) -> None:
    print("\n--- Beli Buku ---")
    if sesi["akun"] is None:
        sesi["akun"] = buat_akun_pelanggan()
    akun = sesi["akun"]

    buku = toko.get_books()
    if not buku:
        print("Inventaris masih kosong.")
        return

    toko.show_inventory()
    print(f"\nPelanggan: {akun.owner} | Saldo: Rp{akun.balance:,}")
    nomor = input_angka("Nomor buku yang dibeli : ")
    if not 1 <= nomor <= len(buku):
        print("Nomor buku tidak valid!")
        return
    jumlah = input_angka("Jumlah                 : ")
    akun.purchase_product(buku[nomor - 1], jumlah)
    print(f"Sisa saldo: Rp{akun.balance:,}")


def menu_top_up(sesi: dict) -> None:
    print("\n--- Top Up Saldo ---")
    if sesi["akun"] is None:
        sesi["akun"] = buat_akun_pelanggan()
    akun = sesi["akun"]
    jumlah = input_angka("Jumlah top up : Rp")
    akun.top_up(jumlah)
    print(f"Saldo {akun.owner} sekarang: Rp{akun.balance:,}")


def demo_enkapsulasi() -> None:
    """Menunjukkan bahwa atribut private tidak bisa diakses langsung."""
    print("\n--- Demo Enkapsulasi ---")
    buku = Book("Demo Book", "Penulis", 50_000, 5)
    akun = Account("Demo", 100)
    toko = Company("Demo")

    try:
        print(akun.__balance)
    except AttributeError as e:
        print(f"1. Akses langsung __balance -> AttributeError: {e}")

    try:
        akun.balance = -50
    except ValueError as e:
        print(f"2. Setter menolak saldo negatif -> {e}")

    try:
        buku.price = 0
    except ValueError as e:
        print(f"3. Setter menolak harga 0 -> {e}")

    try:
        toko.__calculate_payroll()
    except AttributeError as e:
        print(f"4. Private method dari luar -> AttributeError: {e}")

    try:
        toko.add_employee("Bukan Employee")
    except TypeError as e:
        print(f"5. isinstance menolak objek salah -> {e}")


def data_awal(toko: Company) -> None:
    """Data contoh supaya menu tidak kosong saat pertama dijalankan."""
    toko.add_employee(Employee("Sari", "Kasir", 3_000_000))
    toko.add_employee(Employee("Budi", "Penjaga Gudang", 2_800_000))
    toko.add_book(Book("Laskar Pelangi", "Andrea Hirata", 85_000, 10))
    toko.add_book(Book("Bumi Manusia", "Pramoedya Ananta Toer", 110_000, 5))
    toko.add_book(Book("Cantik Itu Luka", "Eka Kurniawan", 95_000, 3))


# =====================================================
#                    PROGRAM UTAMA
# =====================================================
MENU = """
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
"""


def main() -> None:
    toko = Company("Toko Buku Nusantara")
    sesi = {"akun": None}         

    print("Memuat data awal...")
    data_awal(toko)

    while True:
        print(MENU)
        pilihan = input("Pilih menu: ").strip()

        try:
            if pilihan == "1":
                toko.show_inventory()
            elif pilihan == "2":
                menu_tambah_buku(toko)
            elif pilihan == "3":
                menu_lihat_karyawan(toko)
            elif pilihan == "4":
                menu_tambah_karyawan(toko)
            elif pilihan == "5":
                print("\n" + toko.get_payroll_report())
            elif pilihan == "6":
                menu_beli_buku(toko, sesi)
            elif pilihan == "7":
                menu_top_up(sesi)
            elif pilihan == "8":
                demo_enkapsulasi()
            elif pilihan == "0":
                print("Terima kasih, sampai jumpa!")
                break
            else:
                print("Pilihan tidak tersedia, coba lagi.")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
