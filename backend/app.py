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
# CORS(app)

app.secret_key = os.getenv("SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'spotify-keepup-session'
TOKEN_INFO = "token_info"


# @app.after_request
# def apply_cors_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
#     response.headers['Access-Control-Allow-Credentials'] = 'true'
#     return response

# App Routes

@app.route('/test')
def test():
    # current_user()
    return jsonify({"message": "test successful!"})


@app.route('/logout')
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})


@app.route('/is_logged_in')
def is_logged_in():
    print(session)
    if (TOKEN_INFO in session):
        print("logged_in: True")
        return jsonify({"logged_in": True})
    print("logged_in: False")
    return jsonify({"logged_in": False})


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

    return jsonify({"message": "redirect finished"})
    # response = make_response(jsonify({'url': 'http://localhost:5173/'}))
    # return response
    # return redirect(os.getenv("MAIN_REDIRECT_URL"))
    # return jsonify({'url': 'http://localhost:5173/'})


@app.route('/artistsYouLike')
def artistsYouLike():
    try:
        token_info = get_token()
    except:
        print("USER NOT LOGGED IN")
        return redirect("/login")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # user_id = sp.current_user()['id']

    # get artists from current user top tracks
    trendingArtists = set()
    for track in sp.current_user_top_tracks(limit=30, offset=0)['items']:
        for artist in track['artists']:
            trendingArtists.add(artist['id'])

    # get most diff. songs listened to artists all-time and 
    # already-listened to songs (for exclusion)
    topArtists = {}
    topTracks = []
    i = 0
    while True and i < 20:
        tracks = sp.current_user_top_tracks(limit=50, offset=50 * i)['items']
        i += 1
        for track in tracks:
            artists = []
            for artist in track['artists']:
                artists += [(artist['id'], artist['name'])]
                topArtists[artist['id']] = 1 + topArtists.get(artist['id'], 0)

            topTracks += [(track['name'], track['id'], 
                           track['album']['images'][2]['url'], artists)]
            
        if (len(tracks) < 50):
            break

    # get songs from listened-to artists
    topArtists = sorted(topArtists.items(), key=lambda item: item[1], reverse=True)

    # create final artist list (3 steps)
    # 1. up to 5 artists from sample of most-listened to artists
    artistsToUse = set()
    topTenth = len(topArtists) // 10
    if topTenth >= 5:
        for artist in random.sample(topArtists[:topTenth], 5):
            artistsToUse.add(artist[0])
    else:
        artistsToUse.update(artist for artist in topArtists[:5]) 

    # 2. up to 5 artists from recently Liked songs
    startSize = len(artistsToUse)
    items = sp.current_user_saved_tracks(limit=50, offset=0)['items']
    random.shuffle(items)
    for item in items:
        for artist in item['track']['artists']:
            artistsToUse.add(artist['id'])
            if len(artistsToUse) >= startSize + 5:
                break
        if len(artistsToUse) >= startSize + 5:
            break

    # 3. fill rest up to 20 from artists from user current high frequency tracks
    while len(artistsToUse) < 20:
        for track in topTracks:
            for artist in track[3]:
                artistsToUse.add(artist[0])
                if len(artistsToUse) >= 20:
                    break
            if len(artistsToUse) >= 20:
                break
    
    artists_to_use = list(artistsToUse) 
    
    return jsonify(artists_to_use)

# testing version
@app.route('/getTracksFromArtists')
def getTracksFromArtists():
    try:
        token_info = get_token()
    except:
        print("USER NOT LOGGED IN")
        return redirect("/login")   

    sp = spotipy.Spotify(auth=token_info['access_token'])
    liked_ids = getLiked()
    liked_ids = [track["track"]["id"] for track in liked_ids]

    # sample artist ids from call to /artistsYouLike. 
    # Replace with request body retrieval / URL data
    artists = ["7kk9WfnMdCB0K2oEz1ISYD","10erGh5UbLL0KsXf1eRfGC",
                "7jVv8c5Fj3E9VhNjxT4snq","6cqXqS5Iemewz8MolkBTdY",
                "0BT8c47gNjriVYP4vMUe9v","4gwpcMTbLWtBUlOijbVpuu",
                "28lO8lCOqFvDB5la90xKUW","6AjW1aE0OlIoRGdnwbHgP2",
                "3VbB6AbCIBTjy7tS2ha410","1Y5AYn8VTrTR3f8HXQQQug",
                "189oT2Q0iCTjqIA8Oqu2fx","246dkjvS1zLTtiykXe5h60",
                "2QOIawHpSlOwXDvSqQ9YJR","5K4W6rqBFWDnAN6FQUkS6x",
                "6aXEStrH1JobocPqZ3XLeW","3Ww8GMbCDMAGwJJ2hd7z7z",
                "292sg99iIOc93zcd30r4Oz","3Op7D6tFVJCOHW6EAV0ck1",
                "5gOgXi3bI04vka9LmISO1G","6vz9KUVgEo1gXIobqiwJ15"]
    
    tracks = []

    for artist in artists:
        added = 0
        top_tracks = sp.artist_top_tracks(artist_id=artist)
        for track in top_tracks["tracks"]:
            if track["id"] not in liked_ids:
                tracks.append(track["uri"])
                added += 1
            if added >= 3:
                break

    return tracks


@app.route('/createPlaylist')
def createPlaylist():
    try:
        token_info = get_token()
    except:
        print("USER NOT LOGGED IN")
        return redirect("/login")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_id = sp.current_user()['id']
    playlist_id = sp.user_playlist_create(user=user_id, name="KeepUp", public=False, collaborative=False)["id"]
    
    return jsonify({"playlist_id": playlist_id})


@app.route('/addToPlaylist')
def addToPlaylist():
    try:
        token_info = get_token()
    except:
        print("USER NOT LOGGED IN")
        return redirect("/login")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlist_id = "1odL3hqdHz7OLpNuSCIPmY" # for testing
    
    # sample tracks from call to /getTracksFromArtists.
    # Replace with request body retrieval / URL data
    test_tracks = ["spotify:track:1zZK2VSV3hywsKWwJzZoyi", "spotify:track:0tmHYs1StVJP38j8kuHHj4",
                    "spotify:track:2S8JdROxVVL4auiFkzr6mc","spotify:track:1SC5rEoYDGUK4NfG82494W",
                    "spotify:track:2YpeDb67231RjR0MgVLzsG","spotify:track:0F7FA14euOIX8KcbEturGH",
                    "spotify:track:5PGmV8qPfRbHc76LIMkCTv","spotify:track:58LzXtlKG07waYQjSG0rFp",
                    "spotify:track:2s1xecLywCRK5sE03md9da","spotify:track:4mikQuKYBRYqwZ4mxOFbtT",
                    "spotify:track:7843tZFBpDbHt8h1Hqi6tU","spotify:track:0V2VVbM3D2vYzwEexAREjw",
                    "spotify:track:3dY1DlC1nDUDtiIKaQ0Ynu","spotify:track:6tXtNrcKGZdaRlEwRuz4e0",
                    "spotify:track:2Ijitr9PXxd3iSwrnK3eAE","spotify:track:2APCw2ZdDumK8vl6NZuBe8",
                    "spotify:track:4IRwrnqPK6Ik29p6QS3t9d","spotify:track:2JoN55H0713j8D4PlGXgK4",
                    "spotify:track:0woYKOagY34VuFUAKMvoMy","spotify:track:4rFsxbbkLBh8jswH4HxD7a",
                    "spotify:track:5npIL1FmDdtzjLUpLUZ9w7","spotify:track:2L5ZLwbqYIBKq5ZdqUxgZg",
                    "spotify:track:1rzXMehi59zCgIW38Txd6O","spotify:track:1Yd5sQRnDkKWRXDZnvFGhl",
                    "spotify:track:0o8mdI1vf5ly2qpCxNJlC1","spotify:track:5uI7OuSoyjSZvfLFhWTSaw",
                    "spotify:track:0Mtjq8Q6Z7gPVhqKkUPHtI","spotify:track:5IZXB5IKAD2qlvTPJYDCFB",
                    "spotify:track:2OzhQlSqBEmt7hmkYxfT6m","spotify:track:21jGcNKet2qwijlDFuPiPb",
                    "spotify:track:3Dgmyz32dxvtxvUTPS0CUI","spotify:track:0ROMalDdNg3L2HoZP4qFyJ",
                    "spotify:track:7HB1REjjalFLSXgXlAAwFs","spotify:track:4EWCNWgDS8707fNSZ1oaA5",
                    "spotify:track:5TRPicyLGbAF2LGBFbHGvO","spotify:track:4OssqCixV2Xsxd43wMIQyS",
                    "spotify:track:4lZXwUlC7Xxw56QJGSOEKE","spotify:track:1evd9ocxQIiRwYlFDZmTjF",
                    "spotify:track:159SoP5NrhRgvcV2Bzqego","spotify:track:2TmUt0ofWMa02MdYkKhK4C",
                    "spotify:track:1mbLvyFNIifliPtmMmRQN9","spotify:track:4PtJNlcpEGyNAkYy44m5fI",
                    "spotify:track:1KrpXYLMCJ8GaDSz61FQNU","spotify:track:3cLqK3LPVrTIzfENVmYLoU",
                    "spotify:track:0iq3MFEbuKTWJgdhwdOwXI","spotify:track:2jnOUdpaFKr9koG1Vtbj6v",
                    "spotify:track:2vJXkBYTfhmszE7ggfDc9E","spotify:track:57scbUX9utATbRFaYUWOnE",
                    "spotify:track:3FoEL2ozgfVP8TlwjvjbNL","spotify:track:6qCbhkc1nXf7ltP5hzitPm",
                    "spotify:track:52mwBczd6DywxW0yNeoZto","spotify:track:3ffUoOFNLBkHhQ9x0j8zkI",
                    "spotify:track:5qGHMDEUWSn8vVRyIgGXTi","spotify:track:2dtkeMCTY4a7INBZ9ZteqX"]

    sp.playlist_add_items(playlist_id, test_tracks)
    
    return jsonify({"message": "songs should be added"})    


# Helper Functions

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read,user-top-read,user-follow-read,playlist-read-private,playlist-read-collaborative,playlist-modify-public,playlist-modify-private"
    )


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    # sp_oauth = create_spotify_oauth()
    # token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


def getLiked():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect("/login")
    sp = spotipy.Spotify(auth=token_info['access_token'])
    all_songs = []
    i = 0
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=50 * i)['items']
        i += 1
        all_songs += items
        if (len(items) < 50):
            break
    return all_songs


# Run Application

if __name__ == "__main__":
    #app.run(debug=True, use_reloader=False)
    app.run(debug=True)