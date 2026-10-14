import os
from flask import Flask
from routes import rotas_bp
import database
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '../frontend')

app = Flask(__name__,template_folder=FRONTEND_DIR,
            static_folder=FRONTEND_DIR)
CORS(app)

database.inicializar_banco()

app.register_blueprint(rotas_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)