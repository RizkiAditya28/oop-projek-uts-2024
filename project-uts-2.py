from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import PrimaryKeyConstraint
import datetime

Base = declarative_base()

# User Table
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    level = Column(String, nullable=False)

# Data Barang Table
class DataBarang(Base):
    __tablename__ = 'data_barang'
    id_barang = Column(String, primary_key=True)
    nama_barang = Column(String, nullable=False)
    harga = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    id_jenis_barang = Column(String, ForeignKey('data_jenis.id_jenis_barang'), nullable=False)

# Data Jenis Table
class DataJenis(Base):
    __tablename__ = 'data_jenis'
    id_jenis_barang = Column(String, primary_key=True)
    nama_jenis = Column(String, nullable=False)

# Data Pelanggan Table
class DataPelanggan(Base):
    __tablename__ = 'data_pelanggan'
    id_pelanggan = Column(String, primary_key=True)
    nama = Column(String, nullable=False)
    alamat = Column(String, nullable=False)
    no_telp = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

# Data Transaksi Table
class DataTransaksi(Base):
    __tablename__ = 'data_transaksi'
    id_transaksi = Column(String, primary_key=True)
    id_pelanggan = Column(String, ForeignKey('data_pelanggan.id_pelanggan'), nullable=False)
    tanggal = Column(Date, nullable=False)
    total = Column(Integer, nullable=False)
    diskon = Column(Integer, nullable=False)
    bayar = Column(Integer, nullable=False)

# Data Detail Transaksi Table
class DataDetailTransaksi(Base):
    __tablename__ = 'data_detail_transaksi'
    id_pelanggan = Column(String, ForeignKey('data_pelanggan.id_pelanggan'), nullable=False)
    id_barang = Column(String, ForeignKey('data_barang.id_barang'), nullable=False)
    id_transaksi = Column(String, ForeignKey('data_transaksi.id_transaksi'), nullable=False)
    jumlah_beli = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)

    # Defining composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('id_pelanggan', 'id_barang', 'id_transaksi'),
    )

# SQLite Database setup
engine = create_engine('sqlite:///project-uts-2.db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()



def menu_awal():
    while True:
        print("\n===== Menu Awal =====")
        print("1. Masuk sebagai Admin")
        print("2. Masuk sebagai Pelanggan")
        print("3. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            menu_admin()
        elif pilihan == "2":
            menu_pelanggan()
        elif pilihan == "3":
            print("Terima kasih, program selesai.")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

# Menu Admin
def menu_admin():
    while True:
        print("\n===== Menu Admin =====")
        print("1. Lihat dan Edit Data Pelanggan")
        print("2. Lihat Detail Barang yang Dibeli")
        print("3. Kembali ke Menu Awal")
        pilihan = input("Pilih menu admin: ")

        if pilihan == "1":
            menu_pelanggan_admin()
        elif pilihan == "2":
            menu_barang_dibeli_admin()
        elif pilihan == "3":
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

# Admin hanya bisa melihat dan mengedit data pelanggan
def menu_pelanggan_admin():
    while True:
        print("\n===== Lihat dan Edit Data Pelanggan =====")
        print("1. Tampilkan Semua Pelanggan")
        print("2. Edit Pelanggan")
        print("3. Kembali ke Menu Admin")
        pilihan = input("Pilih menu pelanggan admin: ")

        if pilihan == "1":
            tampilkan_pelanggan()
        elif pilihan == "2":
            edit_pelanggan()
        elif pilihan == "3":
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

# Fungsi untuk menampilkan semua pelanggan
def tampilkan_pelanggan():
    pelanggan_list = session.query(DataPelanggan).all()
    
    if pelanggan_list:
        print("\n===== Daftar Pelanggan =====")
        for pelanggan in pelanggan_list:
            print(f"ID Pelanggan: {pelanggan.id_pelanggan}, Nama: {pelanggan.nama}, Alamat: {pelanggan.alamat}, No. Telepon: {pelanggan.no_telp}, Email: {pelanggan.email}")
    else:
        print("Belum ada pelanggan yang terdaftar.")

def edit_pelanggan():
    id_pelanggan = input("Masukkan ID Pelanggan yang akan diedit: ")
    pelanggan = session.query(DataPelanggan).filter_by(id_pelanggan=id_pelanggan).first()

    if pelanggan:
        nama_baru = input(f"Masukkan Nama baru ({pelanggan.nama}): ") or pelanggan.nama
        alamat_baru = input(f"Masukkan Alamat baru ({pelanggan.alamat}): ") or pelanggan.alamat
        no_telp_baru = input(f"Masukkan No. Telepon baru ({pelanggan.no_telp}): ") or pelanggan.no_telp
        email_baru = input(f"Masukkan Email baru ({pelanggan.email}): ") or pelanggan.email

        pelanggan.nama = nama_baru
        pelanggan.alamat = alamat_baru
        pelanggan.no_telp = no_telp_baru
        pelanggan.email = email_baru
        session.commit()
        print("Data pelanggan berhasil diperbarui.")
    else:
        print("Pelanggan tidak ditemukan.")

# Admin hanya bisa melihat detail barang yang telah dibeli
def menu_barang_dibeli_admin():
    while True:
        print("\n===== Lihat Detail Barang yang Dibeli =====")
        tampilkan_barang_dibeli()
        break

def tampilkan_barang_dibeli():
    detail_transaksi = session.query(DataDetailTransaksi).all()
    if detail_transaksi:
        for detail in detail_transaksi:
            pelanggan = session.query(DataPelanggan).filter_by(id_pelanggan=detail.id_pelanggan).first()
            barang = session.query(DataBarang).filter_by(id_barang=detail.id_barang).first()
            print(f"ID Transaksi: {detail.id_transaksi}, Nama Pelanggan: {pelanggan.nama}, Nama Barang: {barang.nama_barang}, Jumlah Beli: {detail.jumlah_beli}, Subtotal: {detail.subtotal}")
    else:
        print("Tidak ada detail transaksi yang ditemukan.")

# Menu Pelanggan
def menu_pelanggan():
    while True:
        print("\n===== Menu Pelanggan =====")
        print("1. Beli Barang")
        print("2. Lihat Detail Transaksi")
        print("3. Kembali ke Menu Awal")
        pilihan = input("Pilih menu pelanggan: ")

        if pilihan == "1":
            beli_barang()
        elif pilihan == "2":
            lihat_detail_transaksi_pelanggan()
        elif pilihan == "3":
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

# Fungsi Beli Barang untuk pelanggan
def beli_barang():
    print("\n===== Masukkan Data Pelanggan =====")
    id_pelanggan = input("Masukkan ID Pelanggan: ")
    nama = input("Masukkan Nama: ")
    alamat = input("Masukkan Alamat: ")
    no_telp = input("Masukkan No. Telepon: ")
    email = input("Masukkan Email: ")

    # Tambah pelanggan baru jika belum ada di database
    pelanggan = session.query(DataPelanggan).filter_by(id_pelanggan=id_pelanggan).first()
    if not pelanggan:
        pelanggan_baru = DataPelanggan(
            id_pelanggan=id_pelanggan,
            nama=nama,
            alamat=alamat,
            no_telp=no_telp,
            email=email
        )
        session.add(pelanggan_baru)
        session.commit()
        print("Pelanggan baru berhasil ditambahkan.")

    # Pilih barang untuk dibeli dengan input nama barang
    nama_barang = input("Masukkan Nama Barang yang ingin dibeli: ")
    barang = session.query(DataBarang).filter_by(nama_barang=nama_barang).first()

    if not barang:
        print("Barang tidak ditemukan.")
        return

    jumlah_beli = int(input(f"Masukkan jumlah barang yang ingin dibeli (stock tersedia: {barang.stock}): "))

    if jumlah_beli > barang.stock:
        print("Stock tidak mencukupi.")
        return

    subtotal = jumlah_beli * barang.harga
    print(f"Subtotal: {subtotal}")

    id_transaksi = input("Masukkan ID Transaksi: ")
    total = subtotal  # Diskon atau penyesuaian lainnya dapat ditambahkan di sini
    diskon = 0
    bayar = total - diskon

    # Menambahkan ke tabel transaksi
    transaksi_baru = DataTransaksi(
        id_transaksi=id_transaksi,
        id_pelanggan=id_pelanggan,
        tanggal=datetime.date.today(),
        total=total,
        diskon=diskon,
        bayar=bayar
    )
    session.add(transaksi_baru)

    # Mengurangi stock barang
    barang.stock -= jumlah_beli

    # Menambahkan detail transaksi
    detail_transaksi_baru = DataDetailTransaksi(
        id_pelanggan=id_pelanggan,
        id_barang=barang.id_barang,
        id_transaksi=id_transaksi,
        jumlah_beli=jumlah_beli,
        subtotal=subtotal
    )
    session.add(detail_transaksi_baru)

    session.commit()
    print("Pembelian berhasil.")

# Pelanggan dapat melihat detail transaksi mereka sendiri
def lihat_detail_transaksi_pelanggan():
    id_pelanggan = input("Masukkan ID Pelanggan: ")
    detail_transaksi = session.query(DataDetailTransaksi).filter_by(id_pelanggan=id_pelanggan).all()

    if detail_transaksi:
        for detail in detail_transaksi:
            barang = session.query(DataBarang).filter_by(id_barang=detail.id_barang).first()
            print(f"ID Transaksi: {detail.id_transaksi}, Nama Barang: {barang.nama_barang}, Jumlah Beli: {detail.jumlah_beli}, Subtotal: {detail.subtotal}")
    else:
        print("Tidak ada detail transaksi untuk pelanggan ini.")

# Fungsi untuk menambahkan data barang awal (hardcoded)
def tambah_data_barang_awal():
    barang_awal = [
        DataBarang(id_barang="1", nama_barang="T-shirt", harga=295000, stock=50, id_jenis_barang="JNS001"),
        DataBarang(id_barang="2", nama_barang="Jeans", harga=450000, stock=30, id_jenis_barang="JNS001"),
        DataBarang(id_barang="3", nama_barang="Jacket", harga=700000, stock=20, id_jenis_barang="JNS001"),
        DataBarang(id_barang="4", nama_barang="Sneakers", harga=600000, stock=40, id_jenis_barang="JNS002"),
        DataBarang(id_barang="5", nama_barang="Printer", harga=1200000, stock=15, id_jenis_barang="JNS003")
    ]

    jenis_barang_awal = [
        DataJenis(id_jenis_barang="JNS001", nama_jenis="Clothes"),
        DataJenis(id_jenis_barang="JNS002", nama_jenis="Shoes"),
        DataJenis(id_jenis_barang="JNS003", nama_jenis="electronic")
    ]

    # Cek apakah data sudah ada, jika belum tambahkan
    if not session.query(DataBarang).first():
        for barang in barang_awal:
            session.add(barang)

    if not session.query(DataJenis).first():
        for jenis in jenis_barang_awal:
            session.add(jenis)

    session.commit()
    print("Data barang awal berhasil ditambahkan.")

# Main program
if __name__ == "__main__":
    # Tambah data barang hardcoded ke dalam database saat pertama kali menjalankan program
    tambah_data_barang_awal()
    
    # Menampilkan menu utama
    menu_awal()
