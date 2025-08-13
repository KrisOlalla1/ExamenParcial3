# backend/app.py
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar la base de datos
    db.init_app(app)
    
    # Habilitar CORS para permitir peticiones desde cualquier origen
    CORS(app)
    
    # Registrar blueprint de rutas API
    from routes import bp
    app.register_blueprint(bp, url_prefix='/api')
    
    # Comando CLI para crear las tablas en la base de datos
    @app.cli.command("create-db")
    def create_db():
        with app.app_context():
            db.create_all()
            print("✅ Tablas creadas")
    
    # Ruta raíz con mensaje y estilo simple
    @app.route("/")
    def home():
        return """
        <html>
            <head>
                <title>API Médicos</title>
                <style>
                    body {
                        background-color: #f4f6f8;
                        font-family: Arial, sans-serif;
                        color: #333;
                        text-align: center;
                        padding-top: 50px;
                    }
                    h1 {
                        color: #007BFF;
                    }
                    p {
                        font-size: 18px;
                        color: #555;
                    }
                    .status {
                        display: inline-block;
                        background: #28a745;
                        color: white;
                        padding: 8px 15px;
                        border-radius: 5px;
                        margin-top: 20px;
                        font-weight: bold;
                    }
                </style>
            </head>
            <body>
                <h1>🚀 API Médicos en Línea</h1>
                <p>El servidor está corriendo correctamente.</p>
                <div class="status">Status: OK ✅</div>
            </body>
        </html>
        """
    
    # ✅ Ruta de health check para pruebas automáticas
    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
