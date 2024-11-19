from flask import Flask, make_response, request, url_for, session, redirect, jsonify
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv, dotenv_values
import os
import time
import random

load_dotenv()
MAIN_REDIRECT_URL = "http://localhost:5173"
app = Flask(__name__)
CORS(app, supports_credentials=True, origins=MAIN_REDIRECT_URL)

app.secret_key = os.getenv("SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'spotify-keepup-session'
TOKEN_INFO = "token_info"


@app.after_request
def apply_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# App Routes

@app.route('/test')
def test():
    # current_user()
    return jsonify({"message": "test successful!"})


@app.route('/logout')
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})


@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code, as_dict=True)
    session[TOKEN_INFO] = token_info
    print(session)
    
    if TOKEN_INFO in session:
        print("SESSION TOKEN PRESENT")
    else:
        print("NO SESSION TOKEN FOUND")

    response = make_response(jsonify({'url': 'http://localhost:5173/'}))
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
    # return redirect(os.getenv("MAIN_REDIRECT_URL"))
    # return jsonify({'url': 'http://localhost:5173/'})





# Helper Functions

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read,user-top-read,user-follow-read,playlist-read-private,playlist-read-collaborative,playlist-modify-public,playlist-modify-private"
    )


# Run Application

if __name__ == "__main__":
    #app.run(debug=True, use_reloader=False)
    app.run(debug=True)