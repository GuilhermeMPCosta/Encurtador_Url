from flask import Flask
from routes import rotas_bp
import database

app = Flask(__name__)

database.inicializar_banco()

app.register_blueprint(rotas_bp)

if __name__ == '__main__':
    app.run(debug=True)