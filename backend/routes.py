import string
import random
from flask import Blueprint, make_response, request, jsonify,redirect
import database
import uuid

rotas_bp = Blueprint('rotas',__name__)

def gerar_codigo_curto(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

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

    resposta = make_response(jsonify({
        'url_encurtada': f"http://localhost:5000/{codigo}",
        'codigo':codigo
    }), 201)

    if novo_usuario:
        resposta.set_cookie('usuario_id', usuario_id, max_age=31536000)  # Cookie válido por 365 dias

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

@rotas_bp.route('/meus-urls', methods=['POST'])
def meu_urls():
    usuario_id = request.cookies.get('usuario_id')
    if not usuario_id:
        return jsonify([])

    links = database.listar_urls(usuario_id)
    return jsonify(links)