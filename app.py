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

@app.route('/recent')
def show_recent():
  if 'token_info' not in session:
    return redirect(url_for('login'))
  
  sp = create_spotify_client(session['token_info'])

  if sp:
    recent_tracks = get_recent_tracks(sp)
    return render_template('recent.html', recent_tracks=recent_tracks)
  else:
    return "Errore durante l'autenticazione con spotify"
  
@app.route('/top')
def show_top():
  if 'token_info' not in session:
    return redirect(url_for('login'))

  sp = create_spotify_client(session['token_info'])
  
  if sp:
    top_artists, top_tracks = get_top_artists_and_tracks(sp)
    return render_template('top.html', top_artists=top_artists, top_tracks=top_tracks)
  else:
    return "Errore durante l'autenticazione con spotify"

# Custom Filter
@app.template_filter()
def jinja2_enumerate(iterable):
  return enumerate(iterable)

# Helpers
def create_spotify_oauth(scope=None):
  return SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
  )

def create_spotify_client(token_info):
  try:
    sp_oauth = create_spotify_oauth()
    sp = spotipy.Spotify(auth_manager=sp_oauth)

    if token_info:
      sp_oauth.token_info = token_info
      session.modified = True
    return sp
  except Exception as e:
    logging.error(f"Errore durante l'autenticazione con Spotify: {e}")
    return None

def get_recent_tracks(sp):
  try:
    recent_tracks_data = sp.current_user_recently_played(limit=12)
    recent_tracks = []

    for item in recent_tracks_data['items']:
      track_info = {
        'name': item['track']['name'],
        'artist': item['track']['artists'][0]['name'],
        'album_image': item['track']['album']['images'][0]['url'] if item['track']['album']['images'] else None
      }
      recent_tracks.append(track_info)
    return recent_tracks
  except spotipy.SpotifyException as e:
    logging.error(f"Errore durante il recupero delle tracce recenti: {e}")
    return None

def get_top_artists_and_tracks(sp):
  try:
    top_artists_all_time = sp.current_user_top_artists(limit=12, time_range='long_term')
    top_artists = [artist['name'] for artist in top_artists_all_time['items']]
    
    top_tracks_all_time = sp.current_user_top_tracks(limit=12, time_range='long_term')
    top_tracks = [f"{track['artists'][0]['name']} - {track['name']}" for track in top_tracks_all_time['items']]
    
    return top_artists, top_tracks
  except spotipy.SpotifyException as e:
    logging.error(f"Errore durante il recupero delle top artist e tracce: {e}")
    return None, None

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')