from flask import Flask, request, url_for, session, redirect, jsonify
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv, dotenv_values
import os
import time
import random

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = os.getenv("SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'spotify-keepup-session'
TOKEN_INFO = "token_info"


# App Routes

@app.route('/test')
def test():
    return jsonify({"message": "test successful!"})


if __name__ == "__main__":
    #app.run(debug=True, use_reloader=False)
    app.run(debug=True)