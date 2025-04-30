import sqlite3

def create_table():
    conn=sqlite3.connect('Visitas.db')
    cursor=conn.cursor()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS Visitas(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   document TEXT,
                   morador TEXT,
                   tvisita TEXT,
                   veiculo TEXT,
                   placa TEXT,
                   entrada TEXT,
                   saida TEXT)
                   ''')
    conn.commit()
    conn.close()

def fetch_visitas():
    conn= sqlite3.connect('Visitas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Visitas ORDER BY id DESC')
    visitas=cursor.fetchall()
    conn.close()
    return visitas

def insert_visitas(name,document,morador,tvisita,veiculo,placa,entrada,saida):
    conn=sqlite3.connect('Visitas.db')
    cursor =  conn.cursor()
    cursor.execute('INSERT INTO Visitas ( name,document,morador,tvisita,veiculo,placa,entrada,saida) VALUES (?,?,?,?,?,?,?,?)',
                   (name,document,morador,tvisita,veiculo,placa,entrada,saida))
    conn.commit()
    conn.close()

def delete_visitas(id):
    conn = sqlite3.connect('Visitas.db')
    cursor= conn.cursor()
    cursor.execute("DELETE FROM visitas WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update_visitas(id,new_name,new_document,new_morador,new_tvisita,new_veiculo,new_placa,new_entrada,new_saida):
    conn = sqlite3.connect('Visitas.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE visitas SET name=?, document=?, morador=?, tvisita=?, veiculo=?, placa=?, entrada=?, saida=? WHERE id =?",
                   (new_name,new_document,new_morador,new_tvisita,new_veiculo,new_placa,new_entrada,new_saida, id))
                              
    conn.commit()
    conn.close()

def update_saida(id, new_saida):
    conn = sqlite3.connect('Visitas.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Visitas SET saida=? WHERE id=?", (new_saida, id))
    conn.commit()
    conn.close()
    
def id_exists(id):
    conn = sqlite3.connect('Visitas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Visitas WHERE id=?", (id,))
    result= cursor.fetchone()
    conn.close()
    return result[0] > 0

create_table()

def search_visitas(term):
    conn = sqlite3.connect('Visitas.db')
    cursor = conn.cursor()
    like_term = f'%{term}%'
    cursor.execute('''
        SELECT * FROM Visitas
        WHERE name LIKE ? OR document LIKE ? OR morador LIKE ? OR tvisita LIKE ? OR veiculo LIKE ? OR placa LIKE ?
        ORDER BY id DESC
    ''', (like_term, like_term, like_term, like_term, like_term, like_term))
    results = cursor.fetchall()
    conn.close()
    return results
    