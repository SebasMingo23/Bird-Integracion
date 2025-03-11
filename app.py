from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test_api():
    data = request.json  # Obtener datos en formato JSON

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    return jsonify({
        "message": "Datos recibidos correctamente",
        "data": data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
