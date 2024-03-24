import os
import spotipy
import logging 

from flask import Flask, render_template, url_for, request, session, redirect
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
logging.basicConfig(level=logging.INFO)

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI', 'http://localhost:5000/callback')

@app.route('/')
def index():
  logged_in = 'token_info' in session
  return render_template('index.html', logged_in=logged_in)

@app.route('/login')
def login():
  if 'token_info' in session:
    return redirect(url_for('index'))
  else:
    scope = "user-library-read user-read-recently-played user-top-read"
    return redirect(url_for('authorize', scope=scope))

@app.route('/authorize')
def authorize():
  scope = request.args.get('scope', '')
  sp_oauth = create_spotify_oauth(scope)
  auth_url = sp_oauth.get_authorize_url()
  return redirect(auth_url)

@app.route('/callback')
def callback():
  code = request.args.get('code')
  sp_oauth = create_spotify_oauth()
  token_info = sp_oauth.get_access_token(code)
  if token_info:
    session['token_info'] = token_info
  else:
    return "Errore durante l'autenticazione co Spotify"
  return redirect(url_for('index'))

# Helpers
def create_spotify_oauth(scope=None):
  return SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
  )

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')