import sqlite3
from datetime import datetime, timezone

Nome_BANCO = 'encurtador.db'

def horario_utc():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

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
            usuario_id TEXT NOT NULL,
            created_at DATETIME
        )
    ''')
    colunas = {coluna['name'] for coluna in cursor.execute('PRAGMA table_info(urls)')}
    if 'created_at' not in colunas:
        cursor.execute('ALTER TABLE urls ADD COLUMN created_at DATETIME')
    conn.commit()
    conn.close()

def salvar_url(codigo, url_original, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO urls (codigo, url_original, usuario_id, created_at) VALUES (?, ?, ?, ?)',
        (codigo, url_original, usuario_id, horario_utc())
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
    cursor.execute(
        'SELECT * FROM urls WHERE usuario_id = ? ORDER BY julianday(created_at) DESC, id DESC',
        (usuario_id,)
    )
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