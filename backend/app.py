# backend/app.py
from flask import Flask
from config import Config
from models import db
from routes import bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(bp, url_prefix='/api')

    @app.cli.command("create-db")
    def create_db():
        with app.app_context():
            db.create_all()
            print("✅ Tablas creadas")

    # Ruta raíz con HTML bonito
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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
