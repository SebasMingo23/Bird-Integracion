from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

@app.route('/api/bird', methods=['POST'])
def receive_bird_data():
    try:
        data = request.get_json()

        # Lista de campos requeridos
        required_fields = ["nombre", "apellido", "email", "telefono", "ciudad", "carrera", "cedula"]

        # Validación simple de campos
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        # Extraer datos
        nombre = data["nombre"]
        apellido = data["apellido"]
        email = data["email"]
        telefono = data["telefono"]
        ciudad = data["ciudad"]
        carrera = data["carrera"]
        cedula = data["cedula"]

        # Crear log ID y timestamp
        log_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        print(f"[{timestamp}] 🟦 LOG ID: {log_id} | Recibido: {nombre} {apellido} - {email} - {telefono} - {ciudad} - {carrera} - {cedula}")

        return jsonify({
            "status": "ok",
            "log_id": log_id,
            "timestamp": timestamp,
            "mensaje": f"¡Gracias, {nombre}! Tus datos fueron recibidos correctamente."
        }), 200

    except Exception as e:
        error_id = str(uuid.uuid4())
        print(f"🟥 ERROR ID: {error_id} | {str(e)}")
        return jsonify({
            "error": "Ocurrió un error en el servidor",
            "error_id": error_id
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)



