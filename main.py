from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import asyncio
import edge_tts

app = Flask(__name__)
CORS(app, origins=["https://mintcream-elk-986360.hostingersite.com"])  # <- AQUI

os.makedirs("audio", exist_ok=True)

async def generar_audio(texto, archivo):
    voice = "es-ES-AlvaroNeural"
    communicate = edge_tts.Communicate(texto, voice)
    await communicate.save(archivo)

@app.route('/voz', methods=['POST'])
def voz():
    data = request.get_json()
    texto = data.get("texto", "").strip()
    if not texto:
        return jsonify({"error": "Texto vacío"}), 400

    archivo_audio = "audio/salida.mp3"
    asyncio.run(generar_audio(texto, archivo_audio))

    return jsonify({"audio": f"/{archivo_audio}?t={os.path.getmtime(archivo_audio)}"})

@app.route('/audio/<path:filename>')
def audio(filename):
    return send_from_directory("audio", filename)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
