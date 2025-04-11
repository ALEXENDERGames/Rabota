import sqlite3
def init_bd():
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE knigi (
        id_kniga INTEGER PRIMARY KEY,
        nazvanie TEXT NOT NULL,
        avtor TEXT NOT NULL,
        god INTEGER,
        dostupna INTEGER DEFAULT 1
    )''')

    cur.execute('''CREATE TABLE chitateli (
        id_chitatel INTEGER PRIMARY KEY,
        fio TEXT NOT NULL,
        telefon TEXT,
        vzal_knugu INTEGER
    )''')
    conn.commit()
    conn.close()
def dob_kniga(nazv, writer, year):
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO knigi (nazvanie, avtor, god) VALUES (?, ?, ?)', (nazv, writer, year))
    conn.commit()
    conn.close()
def new_chitatel(name, phone_num):
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO chitateli (fio, telefon) VALUES (?, ?)', (name, phone_num))
    conn.commit()
    conn.close()

def vidacha_knigi(id_man, id_book):
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute('UPDATE knigi SET dostupna = 0 WHERE id_kniga = ?', (id_book,))
    cur.execute('UPDATE chitateli SET vzal_knugu = ? WHERE id_chitatel = ?', (id_book, id_man))
    conn.commit()
    conn.close()

def vernut_knigu(id_book):
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute('UPDATE knigi SET dostupna = 1 WHERE id_kniga = ?', (id_book,))
    cur.execute('UPDATE chitateli SET vzal_knugu = NULL WHERE vzal_knugu = ?', (id_book,))
    conn.commit()
    conn.close()

def spisok_dostupnih():
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM knigi WHERE dostupna = 1')
    result = cur.fetchall()
    conn.close()
    return result


def chto_na_rukah(id_man):
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    cur.execute('SELECT vzal_knugu FROM chitateli WHERE id_chitatel = ?', (id_man,))
    book_id = cur.fetchone()

    if book_id and book_id[0]:
        cur.execute('SELECT * FROM knigi WHERE id_kniga = ?', (book_id[0],))
        result = cur.fetchall()
    else:
        result = []

    conn.close()
    return result


def poisk_po_bd(search_term):
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    term = f'%{search_term}%'
    cur.execute('SELECT * FROM knigi WHERE nazvanie LIKE ? OR avtor LIKE ?', (term, term))
    result = cur.fetchall()
    conn.close()
    return result
init_bd()
dob_kniga("Война и мир", "Л. Толстой", 1867)
dob_kniga("Ведьмак", "А. Сопковский", 1865)
dob_kniga("Властелин колец", "Р. Толкин", 1948)
new_chitatel("В. Путин", "+79991112233")
new_chitatel("Д. Трамп", "+79994445566")
vidacha_knigi(1, 1)
print("Доступные книги:")
for book in spisok_dostupnih():
    print(f"{book[1]} ({book[2]})")
vernut_knigu(1)
print("\nПосле возврата:")
for book in spisok_dostupnih():
    print(f"{book[1]} ({book[2]})")