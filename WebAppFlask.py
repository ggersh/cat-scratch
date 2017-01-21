from flask import Flask, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/pythonApp.py")
def hello():
    word = request.args.get('word', '')
    print word
    os.system("Streaming.py "+ word)
    return "Hello World!"

if __name__ == "__main__":
    app.run()
