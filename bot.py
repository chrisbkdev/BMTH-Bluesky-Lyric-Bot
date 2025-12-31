import os
import json
import random
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv
from atproto import Client, models

# Load environment variables
load_dotenv()

class BMTHLyricBot:
    def __init__(self):
        self.client = None
        self.lyrics = []
        self.posted_lyrics = set()
        self.load_lyrics()
        
    def load_lyrics(self):
        """Load lyrics from JSON file"""
        try:
            with open('lyrics.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for song in data['songs']:
                    for lyric in song['lyrics']:
                        if lyric.strip():  # Only add non-empty lines
                            self.lyrics.append(lyric.strip())
            print(f"Loaded {len(self.lyrics)} lyric lines from {len(data['songs'])} songs")
        except FileNotFoundError:
            print("Error: lyrics.json not found!")
            raise
        except json.JSONDecodeError:
            print("Error: Invalid JSON in lyrics.json!")
            raise
    
    def authenticate(self):
        """Authenticate with Bluesky"""
        handle = os.getenv('BLUESKY_HANDLE')
        password = os.getenv('BLUESKY_PASSWORD')
        
        if not handle or not password:
            raise ValueError("BLUESKY_HANDLE and BLUESKY_PASSWORD must be set in .env file")
        
        self.client = Client()
        self.client.login(handle, password)
        print(f"Successfully authenticated as {handle}")
    
    def get_random_lyric(self):
        """Get a random lyric that hasn't been posted recently"""
        if not self.lyrics:
            raise ValueError("No lyrics available!")
        
        # If we've posted all lyrics, reset the set
        if len(self.posted_lyrics) >= len(self.lyrics):
            print("All lyrics have been posted. Resetting...")
            self.posted_lyrics.clear()
        
        # Get a random lyric that hasn't been posted
        available_lyrics = [lyric for lyric in self.lyrics if lyric not in self.posted_lyrics]
        
        if not available_lyrics:
            # Fallback: if somehow all are posted, just pick any
            available_lyrics = self.lyrics
        
        selected_lyric = random.choice(available_lyrics)
        self.posted_lyrics.add(selected_lyric)
        
        return selected_lyric
    
    def post_lyric(self):
        """Post a random lyric to Bluesky"""
        try:
            if not self.client:
                self.authenticate()
            
            lyric = self.get_random_lyric()
            
            # Create the post
            post_text = lyric
            
            # Post to Bluesky
            self.client.send_post(text=post_text)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Posted: {lyric[:50]}...")
            
        except Exception as e:
            print(f"Error posting lyric: {e}")
            # Try to re-authenticate on next attempt
            self.client = None
    
    def run(self):
        """Start the bot and schedule posts"""
        print("Starting BMTH Lyric Bot...")
        
        # Authenticate
        self.authenticate()
        
        # Post immediately on start
        print("Posting initial lyric...")
        self.post_lyric()
        
        # Schedule posts every hour
        schedule.every().hour.do(self.post_lyric)
        
        print("Bot is running. Posts scheduled every hour.")
        print("Press Ctrl+C to stop.")
        
        # Keep the bot running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\nBot stopped by user.")

if __name__ == "__main__":
    bot = BMTHLyricBot()
    bot.run()

