import string
import random
from flask import Blueprint, request, jsonify,redirect

rotas_bp = Blueprint('rotas',__name__)

banco_de_dados = {}

def gerar_codigo_curto(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

@rotas_bp.route('/encurtar', methods=['POST'])
def encurtar():
    dados = request.get_json()
    url_original = dados.get('url')

    codigo = gerar_codigo_curto()
    banco_de_dados[codigo] = {
        'url_original': url_original,
        'cliques': 0
    }

    return jsonify({
        'url_encurtada': f"http://localhost:5000/{codigo}",
        'codigo':codigo
    }),201

@rotas_bp.route('/<codigo>')
def redirecionar(codigo):
    if codigo in banco_de_dados:
        banco_de_dados[codigo]['cliques'] += 1
        return redirect(banco_de_dados[codigo]['url_original'])
    return jsonify({'error': 'Código não encontrado'}), 404

@rotas_bp.route('/<codigo>/stats')
def estatisticas(codigo):
    if codigo in banco_de_dados:
        return jsonify({
            'url_original': banco_de_dados[codigo]['url_original'],
            'cliques': banco_de_dados[codigo]['cliques']
        })
    return jsonify({'error': 'Código não encontrado'}), 404