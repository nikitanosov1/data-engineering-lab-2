# whisper-service/app.py
import os
import tempfile
import subprocess
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)


@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Сохраняем входной файл
        ext = os.path.splitext(file.filename)[1] or ".mp4"
        input_path = os.path.join(tmp_dir, "input" + ext)
        file.save(input_path)

        # Запускаем auto_subtitle
        result = subprocess.run([
            "/usr/local/bin/auto_subtitle",
            input_path,
            "-o", tmp_dir,
            "--output_srt", "true",      # явно включаем .srt
            "--srt_only", "true",   # нужны только субтитры .srt, без видео с этими субтитрами
        ], capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({
                "error": "Transcription failed",
                "stderr": result.stderr,
                "stdout": result.stdout
            }), 500

        # Ищем .srt файл
        srt_files = [f for f in os.listdir(tmp_dir) if f.endswith(".srt")]
        if not srt_files:
            return jsonify({"error": "No .srt file generated"}), 500

        srt_path = os.path.join(tmp_dir, srt_files[0])
        return send_file(srt_path, mimetype='text/plain', as_attachment=True, download_name='subtitles.srt')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
