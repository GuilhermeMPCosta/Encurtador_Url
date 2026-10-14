import sqlite3

Nome_BANCO = 'encurtador.db'

def get_connection():
    conn = sqlite3.connect(Nome_BANCO)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_banco():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            url_original TEXT NOT NULL,
            cliques INTEGER DEFAULT 0,
            usuario_id TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def salvar_url(codigo, url_original, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO urls (codigo, url_original, usuario_id) VALUES (?, ?, ?)',
        (codigo, url_original, usuario_id)
    )
    conn.commit()
    conn.close()

def buscar_por_codigo(codigo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM urls WHERE codigo = ?', (codigo,))
    url = cursor.fetchone()
    conn.close()
    return url

def listar_urls(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM urls where usuario_id = ?', (usuario_id,))
    urls = cursor.fetchall()
    conn.close()
    return urls

def incrementar_clique(codigo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE urls SET cliques = cliques + 1 WHERE codigo = ?',
        (codigo,)
    )
    conn.commit()
    conn.close()