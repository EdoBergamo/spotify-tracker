# Spotify Tracker

Spotify Tracker is a Flask web application that allows users ti track their recently played songs on Spotify. It utilizes the Spotify API to fetch the user's recently played tracks and displays them on a web page.

## Features
 - Authorization via Spotify API
 - Fetches and displays the user's recently played tracks
 - Fetches and displays the user's top tracks and artists
 - Provides a simple and intuitive web interface

## Installation
 1. Clone the repository:
    ```bash
    git clone https://github.com/EdoBergamo/spotify-tracker.git
    ```

 2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

 3. Set up Spotify API Credentials:
    - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and create a new Application.
    - Copy the Client ID, Client Secret and the Redirect URI and run those commands `export SPOTIPY_CLIENT_ID="your-client-id"`, `export SPOTIPY_CLIENT_SECRET="your-client-secret"` and `export SPOTIPY_REDIRECT_URI="http://localhost:5000/callback"`.
    - Save your changes.

## Usage
 1. Run the Flask server:
    ```bash
    python app.py
    ```

 2. Open your web browser and navigate to `http://localhost:5000/`

 3. Log in at `http://localhost:5000/login`.

 4. Once authorized, the web page will deisplay the 5 most played songs and the 5 most played artists on your Spotify Account.

## Contributing
Contributions are welcome! If you have any suggestions, feature requests or but reports, please [open an issue](https://github.com/EdoBergamo/spotify-tracker/issues) or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.