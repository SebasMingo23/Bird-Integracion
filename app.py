from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/bird', methods=['POST'])
def receive_bird_data():
    data = request.get_json()

    # Validación simple
    if not data or not all(k in data for k in ("nombre", "apellido", "email")):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    nombre = data["nombre"]
    apellido = data["apellido"]
    email = data["email"]

    print(f"🟦 Recibido: {nombre} {apellido} - {email}")

    return jsonify({
        "status": "ok",
        "mensaje": f"¡Gracias, {nombre}! Tus datos fueron recibidos correctamente."
    }), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)


