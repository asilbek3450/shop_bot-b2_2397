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


def get_all_categories():
    komanda = "SELECT * FROM categories"
    cur.execute(komanda)
    return cur.fetchall()  # Barcha kategoriyalarni qaytaradi


def get_category_id_by_name(nomi):
    komanda = "SELECT id FROM categories WHERE nomi = ?"
    cur.execute(komanda, (nomi,))
    result = cur.fetchone()
    return result[0] if result else None  # Agar kategoriya topilsa, ID ni qaytaradi, aks holda None qaytaradi


def add_product_to_db(nomi, narxi, rasmi, malumot, category_id):
    komanda = """INSERT INTO products (nomi, narxi, rasmi, malumot, category_id) 
                 VALUES (?, ?, ?, ?, ?)"""
    try:
        cur.execute(komanda, (nomi, narxi, rasmi, malumot, category_id))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    
    
def get_all_products(category_id):
    komanda = "SELECT * FROM products WHERE category_id = ?"
    cur.execute(komanda, (category_id,))
    return cur.fetchall()  # Berilgan kategoriya ID bo'yicha barcha mahsulotlarni qaytaradi


def get_product_id_by_name(nomi):
    komanda = "SELECT id FROM products WHERE nomi = ?"
    cur.execute(komanda, (nomi,))
    result = cur.fetchone()
    return result[0] if result else None  # Agar mahsulot topilsa, ID ni qaytaradi, aks holda None qaytaradi


def get_product_by_id(product_id):
    komanda = "SELECT * FROM products WHERE id = ?"
    cur.execute(komanda, (product_id,))
    return cur.fetchone()  # Berilgan mahsulot ID bo'yicha mahsulot ma'lumotlarini qaytaradi