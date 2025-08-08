from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
OUTPUT_DIR = "voices"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/generate-voice", methods=["POST"])
def generate_voice():
    text = request.form.get("text")
    if not text:
        return jsonify({"status": "error", "message": "Texte manquant"}), 400

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    tts = gTTS(text=text, lang='fr')
    tts.save(filepath)

    return jsonify({"status": "success", "file": f"/download/{filename}"})

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
