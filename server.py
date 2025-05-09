from flask import Flask, request, jsonify
import subprocess
import os
import requests

app = Flask(__name__)

BOT_TOKEN = "7987953293:AAHr4TdrWAVi1Qf7Lhbi71e3dgxFNnGwcqc"
CHAT_ID = "1762351737"

@app.route('/send-video', methods=['POST'])
def download_and_send():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "URL inválida"}), 400

    try:
        output_template = "downloaded_video.%(ext)s"
        subprocess.run(["yt-dlp", "-f", "best", "-o", output_template, video_url], check=True)

        for file in os.listdir():
            if file.startswith("downloaded_video"):
                send_to_telegram(file)
                os.remove(file)
                break

        return jsonify({"status": "Video enviado"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    with open(file_path, "rb") as f:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"video": f})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
