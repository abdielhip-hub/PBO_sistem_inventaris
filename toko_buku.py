"""
Tugas Praktikum Mandiri - Minggu Ke-5
Mata Kuliah : Pemrograman Berorientasi Objek
Topik       : Property Visibility & Enkapsulasi di Python 3.12
Tema        : Sistem Inventaris Toko Buku
"""


class Book:
    """Produk: buku. Harga & stok dilindungi (private) dan diakses via @property."""

    def __init__(self, title: str, author: str, price: int, stock: int):
        self.title = title          # public
        self.author = author        # public
        self.__price = 0            # private
        self.__stock = 0            # private
        self.price = price          # lewat setter -> tervalidasi
        self.stock = stock          # lewat setter -> tervalidasi

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
    """Akun pelanggan. Saldo private, tidak boleh negatif."""

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

        # Semua validasi lolos -> aman memodifikasi data
        self.__balance -= total
        book.stock -= qty
        print(f"{self.owner} membeli {qty}x '{book.title}' (Rp{total:,})")


class Employee:
    """Karyawan toko. Gaji private dan divalidasi lewat @property."""

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
        self.__employees = []       # private (wajib sesuai tugas)
        self.__inventory = []       # private

    # ---------- Karyawan ----------
    def add_employee(self, employee) -> None:
        if not isinstance(employee, Employee):       # validasi dengan isinstance
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

    def show_inventory(self) -> None:
        print(f"\n=== Inventaris {self.name} ===")
        for i, book in enumerate(self.__inventory, start=1):
            print(f"{i}. {book}")


# ======================= DEMO =======================
if __name__ == "__main__":
    toko = Company("Toko Buku Nusantara")

    # 1) Tambah karyawan (valid)
    toko.add_employee(Employee("Sari", "Kasir", 3_000_000))
    toko.add_employee(Employee("Budi", "Penjaga Gudang", 2_800_000))

    # 2) Validasi isinstance: objek bukan Employee ditolak
    try:
        toko.add_employee("Bukan Employee")
    except TypeError as e:
        print(f"Error: {e}")

    # 3) Tambah buku ke inventaris
    toko.add_book(Book("Laskar Pelangi", "Andrea Hirata", 85_000, 10))
    toko.add_book(Book("Bumi Manusia", "Pramoedya Ananta Toer", 110_000, 5))
    try:
        toko.add_book(Employee("Salah", "Objek", 1_000_000))
    except TypeError as e:
        print(f"Error: {e}")

    toko.show_inventory()

    # 4) Laporan payroll lewat public method
    print("\n" + toko.get_payroll_report())

    # 5) Method private tidak bisa dipanggil dari luar
    try:
        toko.__calculate_payroll()
    except AttributeError as e:
        print(f"Error (private method): {e}")

    # 6) Pembelian oleh pelanggan
    print()
    novel = Book("Cantik Itu Luka", "Eka Kurniawan", 95_000, 3)
    pelanggan = Account("Noval", 200_000)
    pelanggan.purchase_product(novel, 2)
    print(f"Sisa saldo: Rp{pelanggan.balance:,} | Sisa stok: {novel.stock}")

    try:
        pelanggan.purchase_product(novel, 1)   # saldo tidak cukup
    except ValueError as e:
        print(f"Error: {e}")

    try:
        pelanggan.balance = -50                # setter menolak nilai negatif
    except ValueError as e:
        print(f"Error: {e}")
