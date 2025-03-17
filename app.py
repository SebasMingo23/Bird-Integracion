from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

app = Flask(__name__)

# 📌 Configuración de Rate Limiting (máximo 100 solicitudes por IP cada 15 min)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per 15 minutes"]
)

# 📌 Configurar Logging para monitoreo de solicitudes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.route('/test', methods=['POST'])
@limiter.limit("10 per minute")  # 🔒 Limitación específica para este endpoint
def test_api():
    try:
        # 📌 Obtener datos JSON
        data = request.get_json()

        # 📌 Validación básica de datos
        if not data:
            logging.warning(f"Solicitud sin datos de {request.remote_addr}")
            return jsonify({"error": "No se enviaron datos"}), 400

        # 📌 Registro de la solicitud exitosa
        logging.info(f"Solicitud válida de {request.remote_addr}: {data}")

        return jsonify({
            "message": "Datos recibidos correctamente",
            "data": data
        }), 200

    except Exception as e:
        logging.error(f"Error en la API: {str(e)}")
        return jsonify({"error": "Ocurrió un error en el servidor"}), 500

if __name__ == '__main__':
    # 📌 Configurar host y puerto de manera segura
    app.run(host='0.0.0.0', port=8080, debug=False)

