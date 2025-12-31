import os
import json
import random
import pickle
from datetime import datetime
from dotenv import load_dotenv
from atproto import Client

# Load environment variables
load_dotenv()

def load_lyrics():
    """Load lyrics from JSON file"""
    lyrics = []
    try:
        with open('lyrics.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for song in data['songs']:
                for lyric in song['lyrics']:
                    if lyric.strip():
                        lyrics.append(lyric.strip())
        print(f"Loaded {len(lyrics)} lyric lines from {len(data['songs'])} songs")
        return lyrics
    except FileNotFoundError:
        print("Error: lyrics.json not found!")
        raise
    except json.JSONDecodeError:
        print("Error: Invalid JSON in lyrics.json!")
        raise

def load_posted_lyrics(cache_file='posted_lyrics.pkl'):
    """Load set of posted lyrics from cache file"""
    try:
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return set()

def save_posted_lyrics(posted_lyrics, cache_file='posted_lyrics.pkl'):
    """Save set of posted lyrics to cache file"""
    with open(cache_file, 'wb') as f:
        pickle.dump(posted_lyrics, f)

def get_random_lyric(lyrics, posted_lyrics):
    """Get a random lyric that hasn't been posted recently"""
    if not lyrics:
        raise ValueError("No lyrics available!")
    
    # If we've posted all lyrics, reset the set
    if len(posted_lyrics) >= len(lyrics):
        print("All lyrics have been posted. Resetting...")
        posted_lyrics.clear()
    
    # Get a random lyric that hasn't been posted
    available_lyrics = [lyric for lyric in lyrics if lyric not in posted_lyrics]
    
    if not available_lyrics:
        # Fallback: if somehow all are posted, just pick any
        available_lyrics = lyrics
    
    selected_lyric = random.choice(available_lyrics)
    posted_lyrics.add(selected_lyric)
    
    return selected_lyric, posted_lyrics

def post_lyric():
    """Post a random lyric to Bluesky"""
    handle = os.getenv('BLUESKY_HANDLE')
    password = os.getenv('BLUESKY_PASSWORD')
    
    if not handle or not password:
        raise ValueError("BLUESKY_HANDLE and BLUESKY_PASSWORD must be set as environment variables")
    
    # Load lyrics
    lyrics = load_lyrics()
    
    # Load posted lyrics from cache
    posted_lyrics = load_posted_lyrics()
    
    # Get a random lyric
    lyric, posted_lyrics = get_random_lyric(lyrics, posted_lyrics)
    
    # Authenticate and post
    client = Client()
    client.login(handle, password)
    client.send_post(text=lyric)
    
    # Save posted lyrics
    save_posted_lyrics(posted_lyrics)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Successfully posted: {lyric}")
    
    return lyric

if __name__ == "__main__":
    try:
        post_lyric()
    except Exception as e:
        print(f"Error: {e}")
        raise

