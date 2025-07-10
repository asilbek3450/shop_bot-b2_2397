import sqlite3

conn = sqlite3.connect('shop.db')
cur = conn.cursor()

def create_tables():
    komanda1 = """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ism VARCHAR(100) NOT NULL,
        telefon VARCHAR(20) NOT NULL,
        user_id INTEGER NOT NULL UNIQUE)"""
        
    komanda2 = """CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomi VARCHAR(100) NOT NULL UNIQUE)"""
        
    komanda3 = """CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomi VARCHAR(100) NOT NULL,
        narxi REAL NOT NULL,
        rasmi VARCHAR(500) NOT NULL,
        malumot TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(id))"""
        
    cur.execute(komanda1)
    cur.execute(komanda2)
    cur.execute(komanda3)
    conn.commit()


def add_user(ism, telefon, user_id):
    komanda = "INSERT INTO users (ism, telefon, user_id) VALUES (?, ?, ?)"
    cur.execute(komanda, (ism, telefon, user_id))
    conn.commit()
    
def search_user_by_id(user_id):
    komanda = "SELECT * FROM users WHERE user_id = ?"
    cur.execute(komanda, (user_id,))
    return cur.fetchone()  # Agar foydalanuvchi topilsa, ma'lumotlarni qaytaradi, aks holda None qaytaradi


def add_category_to_db(nomi):
    komanda = "INSERT INTO categories (nomi) VALUES (?)"
    try:
        cur.execute(komanda, (nomi,))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # Agar kategoriya allaqachon mavjud bo'lsa, xatolik qaytaradi
    return True  # Kategoriya muvaffaqiyatli qo'shildi