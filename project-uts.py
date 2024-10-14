from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///project-uts.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Tabel User
class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(35), nullable=False, unique=True)
    password = Column(String(35), nullable=False)
    level = Column(String(15), nullable=False)

# Tabel Data Barang
class Barang(Base):
    __tablename__ = 'Data Barang'
    id_barang = Column(Integer, primary_key=True, autoincrement=True)
    nama_barang = Column(String(35), nullable=False)
    harga = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    id_jenis_barang = Column(Integer, ForeignKey('Data Jenis.id_jenis_barang'))
    jenis = relationship("DataJenis", back_populates="barang")

# Tabel Data Jenis Barang
class DataJenis(Base):
    __tablename__ = 'Data Jenis'
    id_jenis_barang = Column(Integer, primary_key=True)
    nama_jenis = Column(String(35), nullable=False)
    barang = relationship("Barang", back_populates="jenis")

# Tabel Data Pelanggan
class Pelanggan(Base):
    __tablename__ = 'Data Pelanggan'
    id_pelanggan = Column(Integer, primary_key=True)
    nama = Column(String(35), nullable=False)
    alamat = Column(String(255), nullable=False)
    no_telp = Column(String(15), nullable=False, unique=True)
    email = Column(String(35), nullable=False, unique=True)
    transaksi = relationship("Transaksi", back_populates="pelanggan")

# Tabel Data Transaksi
class Transaksi(Base):
    __tablename__ = 'Data Transaksi'
    id_transaksi = Column(Integer, primary_key=True)
    id_pelanggan = Column(Integer, ForeignKey('Pelanggan.id_pelanggan'))
    pelanggan = relationship("Pelanggan", back_populates="transaksi")
    tanggal = Column(Date, nullable=False)
    total = Column(Float, nullable=False)
    diskon = Column(Float, nullable=False)
    bayar = Column(Float, nullable=False)

class DetailTransaksi(Base):
    __tablename__ = 'Detail Transaksi'

    id_detail_transaksi = Column(Integer, primary_key=True, autoincrement=True)
    id_pelanggan = Column(Integer, ForeignKey('Data Pelanggan.id_pelanggan'))
    id_barang = Column(Integer, ForeignKey('Data Barang.id_barang'))
    id_transaksi = Column(Integer, ForeignKey('Data Transaksi.id_transaksi'))
    jumlah_beli = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)

    # Relationships (optional, depends on usage)
    pelanggan = relationship("Pelanggan")
    barang = relationship("Barang")
    transaksi = relationship("Transaksi")

# Buat tabel dari class yang sudah dibuat
Base.metadata.create_all(engine)

if __name__ == "__main__":
    print("Test")
