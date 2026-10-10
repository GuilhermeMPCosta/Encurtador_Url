from flask import Flask
from routes import rotas_bp
import database
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

database.inicializar_banco()

app.register_blueprint(rotas_bp)

if __name__ == '__main__':
    app.run(debug=True)