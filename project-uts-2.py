from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import PrimaryKeyConstraint

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
