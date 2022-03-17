from flask import Flask
import os
import subprocess

app = Flask(__name__)

@app.route("/")
def get_data():
    subprocess.Popen(['python', f'{os.getcwd()}/script.py'])
    return "<h1>Успешно запущено!</h1>"

app.debug = True
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)