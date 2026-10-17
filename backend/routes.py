import string
import random
from datetime import datetime, timezone
from flask import Blueprint, make_response, request, jsonify,redirect,render_template
import database
import uuid

rotas_bp = Blueprint('rotas',__name__)

def timestamp_utc_iso(valor):
    if not valor:
        return None
    data = datetime.fromisoformat(valor.replace('Z', '+00:00'))
    if data.tzinfo is None:
        data = data.replace(tzinfo=timezone.utc)
    return data.astimezone(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

def gerar_codigo_curto(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

@rotas_bp.route('/')
def index():
    return render_template('index.html')

@rotas_bp.route('/encurtar', methods=['POST'])
def encurtar():
    dados = request.get_json() or {}
    url_original = dados.get('url')

    if not url_original:
        return jsonify({'erro': 'A URL é obrigatória'}), 400

    usuario_id = request.cookies.get('usuario_id')
    novo_usuario = False
    if not usuario_id:
        usuario_id = str(uuid.uuid4())
        novo_usuario = True

    codigo = gerar_codigo_curto()
    database.salvar_url(codigo, url_original, usuario_id)
    url_criada = database.buscar_por_codigo(codigo)

    resposta = make_response(jsonify({
        'url_encurtada': f"http://localhost:5000/{codigo}",
        'codigo': codigo,
        'created_at': timestamp_utc_iso(url_criada['created_at'])
    }), 201)

    if novo_usuario:
        resposta.set_cookie('usuario_id', usuario_id, max_age=31536000, path='/',samesite='Lax')  # Cookie válido por 365 dias

    return resposta

@rotas_bp.route('/<codigo>')
def redirecionar(codigo):
    url = database.buscar_por_codigo(codigo)
    if url:
        database.incrementar_clique(codigo)
        return redirect(url['url_original'])
    return jsonify({'error': 'Código não encontrado'}), 404

@rotas_bp.route('/<codigo>/stats')
def estatisticas(codigo):
    url = database.buscar_por_codigo(codigo)
    if url:
        return jsonify({
            'codigo': url['codigo'],
            'url_original': url['url_original'],
            'cliques': url['cliques']
        })
    return jsonify({'error': 'Código não encontrado'}), 404

@rotas_bp.route('/meus-urls', methods=['GET'])
def meu_urls():
    usuario_id = request.cookies.get('usuario_id')
    if not usuario_id:
        return jsonify([])

    links = database.listar_urls(usuario_id)
    links_lista = [dict(link) for link in links]
    for link in links_lista:
        link['created_at'] = timestamp_utc_iso(link['created_at'])
    print(f"Links encontrados para o usuário {usuario_id}: {links_lista}")
    return jsonify(links_lista)