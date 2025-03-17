import pyttsx3
import threading
import os
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)
OUTPUT_FILE = "output.mp3"

def speak_and_save(text, voice_id):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[voice_id].id)

    engine.say(text)
    engine.runAndWait()
    engine.save_to_file(text, OUTPUT_FILE)    

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/text-to-speech", methods=["POST"])
def text_to_speech():
    text = request.form.get("text")
    voice = request.form.get("voice", "male")  

    if not text:
        return jsonify({"error": "Please enter text!"}), 400

    voice_id = 0 if voice == "male" else 1

    threading.Thread(target=speak_and_save, args=(text, voice_id), daemon=True).start()

    return jsonify({"message": "Speaking...", "download_url": "/download-audio"})

@app.route("/download-audio")
def download_audio():
    if os.path.exists(OUTPUT_FILE):
        return send_file(OUTPUT_FILE, as_attachment=True)
    return jsonify({"error": "No audio file available"}), 404

if __name__ == "__main__":
    app.run(debug=False, threaded=True)



"""import pyttsx3
import threading
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()  

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/text-to-speech", methods=["POST"])
def text_to_speech():
    text = request.form.get("text")
    if not text:
        return jsonify({"error": "Please enter text!"}), 400
    
    threading.Thread(target=speak_text, args=(text,), daemon=True).start()

    return jsonify({"message": "Speaking..."})

if __name__ == "__main__":
    app.run(debug=False, threaded=True) 
"""