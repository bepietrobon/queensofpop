import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import time

# ===========================
# 🔐 Configuração do Spotify com Credenciais
# ===========================
SPOTIPY_CLIENT_ID = st.secrets["CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = st.secrets["SECRET_ID"]

@st.cache_resource
def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET
    ))

sp = get_spotify_client()

# ===========================
# 🎤 Buscar ID do Artista (com Cache)
# ===========================
@st.cache_data
def get_artist_id(artist_name):
    result = sp.search(q=artist_name, type="artist", limit=1)
    return result["artists"]["items"][0]["id"] if result["artists"]["items"] else None

# ===========================
# 👥 Buscar Número de Seguidores do Artista
# ===========================
@st.cache_data
def get_artist_followers(artist_id):
    artist_info = sp.artist(artist_id)
    return artist_info["followers"]["total"]

# ===========================
# 🖼️ Buscar Imagem do Artista
# ===========================
@st.cache_data
def get_artist_image(artist_name):
    result = sp.search(q=artist_name, type="artist", limit=1)
    if result["artists"]["items"]:
        return result["artists"]["items"][0]["images"][0]["url"]
    return None

# ===========================
# 💿 Buscar Álbuns do Artista (Removendo Deluxe, Platinum, Live, Acoustic, Karaoke)
# ===========================
@st.cache_data
def get_artist_albums(artist_id):
    albums = sp.artist_albums(artist_id, album_type="album")["items"]
    album_dict = {}
    for album in albums:
        album_name = album["name"]
        # ✅ Mantém apenas álbuns principais e Taylor's Version
        if any(keyword in album_name.lower() for keyword in ["deluxe", "platinum", "live", "acoustic", "karaoke", "special edition", "stadium"]):
            continue
        base_name = album_name.replace("Taylor’s Version", "").replace("Taylor's Version", "").strip()
        if base_name not in album_dict or "Taylor’s Version" in album_name or "Taylor's Version" in album_name:
            album_dict[album_name] = album
    return list(album_dict.values())

# ===========================
# 🎵 Buscar Faixas de um Álbum
# ===========================
@st.cache_data
def get_album_tracks(album_id):
    return sp.album_tracks(album_id)["items"]

# ===========================
# 📊 Buscar Popularidade de Múltiplas Músicas
# ===========================
@st.cache_data
def get_tracks_popularity(track_ids):
    if not track_ids:
        return []
    batches = [track_ids[i:i + 50] for i in range(0, len(track_ids), 50)]
    popularity_list = []
    for batch in batches:
        time.sleep(0.5)  # Pequeno delay para evitar Rate Limit
        tracks_info = sp.tracks(batch)["tracks"]
        popularity_list.extend([track["popularity"] for track in tracks_info])
    return popularity_list