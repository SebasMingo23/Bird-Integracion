from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Configurar credenciales de Bird (sustituye estos valores por los correctos)
BIRD_API_KEY = "a8d2506d-5ced-4d1b-b8d6-bd24a0be9ab4"  # Reemplázalo con tu API Key real
BIRD_WORKSPACE_ID = "519dea38-2787-426c-80a9-18a91af70ed9"  # ID de tu workspace
BIRD_CAMPAIGN_ID = "xyz789"  # ID de la campaña dinámica en Bird

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if not data or 'phonenumber' not in data:
        return jsonify({"error": "Número de teléfono requerido"}), 400

    # Crear o actualizar contacto en Bird
    contact_payload = {
        "identifiers": [{"key": "phonenumber", "value": data["phonenumber"]}],
        "attributes": {
            "firstName": data.get("firstName", ""),
            "lastName": data.get("lastName", "")
        }
    }

    response = requests.post(
        f"https://api.getbird.com/workspaces/{BIRD_WORKSPACE_ID}/contacts",
        json=contact_payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"AccessKey {BIRD_API_KEY}"
        }
    )

    if response.status_code not in [200, 201]:
        return jsonify({
            "error": "No se pudo crear el contacto en Bird",
            "details": response.json()
        }), response.status_code

    contact_id = response.json().get("id")

    # Enviar contacto a la campaña dinámica en Bird
    campaign_payload = {"contacts": [contact_id]}
    response_campaign = requests.post(
        f"https://api.getbird.com/workspaces/{BIRD_WORKSPACE_ID}/campaigns/{BIRD_CAMPAIGN_ID}/contacts",
        json=campaign_payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"AccessKey {BIRD_API_KEY}"
        }
    )

    if response_campaign.status_code not in [200, 201]:
        return jsonify({
            "error": "No se pudo agregar a la campaña dinámica",
            "details": response_campaign.json()
        }), response_campaign.status_code

    return jsonify({"success": "Contacto agregado a la campaña dinámica en Bird"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


