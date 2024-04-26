import mysql.connector

def connect_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_struktur"
    )
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pegawai (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        id_pegawai INT NOT NULL,
                        nama VARCHAR(255) NOT NULL
                    )''')
    conn.commit()

def tambah_pegawai(conn, id_pegawai, nama):
    if not cek_id_pegawai(conn, id_pegawai):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pegawai (id_pegawai, nama) VALUES (%s, %s)", (id_pegawai, nama))
        conn.commit()
        print("Pegawai berhasil ditambahkan.")
    else:
        print("ID pegawai sudah terdaftar.")

def tampilkan_pegawai(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, LPAD(id_pegawai, 4, '0'), nama FROM pegawai")
    result = cursor.fetchall()
    if result:
        print("Daftar Pegawai:")
        for row in result:
            print(f"ID: {row[0]}, ID Pegawai: {row[1]}, Nama: {row[2]}")
    else:
        print("Tidak ada pegawai.")

def update_pegawai(conn, id_pegawai, nama_baru, id_baru):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM pegawai WHERE id = %s", (id_pegawai,))
    result = cursor.fetchone()
    if result:
        cursor.execute("UPDATE pegawai SET id_pegawai = %s, nama = %s WHERE id = %s", (id_baru, nama_baru, id_pegawai))
        conn.commit()
        if cursor.rowcount > 0:
            print("Data pegawai berhasil diperbarui.")
        else:
            print("Gagal memperbarui data pegawai.")
    else:
        print("ID pegawai tidak ditemukan.")

def hapus_pegawai(conn, id_pegawai):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pegawai WHERE id_pegawai = %s", (id_pegawai,))
    conn.commit()
    if cursor.rowcount > 0:
        print("Pegawai berhasil dihapus.")
    else:
        print("ID pegawai tidak ditemukan.")

def validasi_id(id_pegawai):
    if len(id_pegawai) != 4 or not id_pegawai.isdigit():
        return False
    return True

def cek_id_pegawai(conn, id_pegawai):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM pegawai WHERE id_pegawai = %s", (id_pegawai,))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False

def main():
    conn = connect_database()
    create_table(conn)

    while True:
        print("\nPilihan Operasi:")
        print("1. Tambah Pegawai")
        print("2. Tampilkan Pegawai")
        print("3. Update Nama Pegawai")
        print("4. Hapus Pegawai")
        print("5. Keluar")

        pilihan = input("Masukkan pilihan (1/2/3/4/5): ")

        if pilihan == "1":
            while True:
                id_pegawai = input("Masukkan ID pegawai (4 digit): ")
                if validasi_id(id_pegawai):
                    break
                else:
                    print("ID pegawai harus berupa 4 digit angka.")

            nama = input("Masukkan nama pegawai: ")
            tambah_pegawai(conn, id_pegawai, nama)
        elif pilihan == "2":
            tampilkan_pegawai(conn)
        elif pilihan == "3":
            id_pegawai = input("Masukkan ID pegawai yang akan diupdate: ")
            nama_baru = input("Masukkan nama baru: ")
            id_baru = input("Masukkan ID baru: ")
            update_pegawai(conn, id_pegawai, nama_baru, id_baru)
        elif pilihan == "4":
            id_pegawai = input("Masukkan ID pegawai yang akan dihapus: ")
            hapus_pegawai(conn, id_pegawai)
        elif pilihan == "5":
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan angka 1-5.")

    conn.close()

if __name__ == "__main__":
    main()
