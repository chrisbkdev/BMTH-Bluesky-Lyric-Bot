# Bring Me the Horizon Lyric Bot for Bluesky

A Python bot that posts lyric lines from Bring Me the Horizon songs to Bluesky once every hour.

## Features

- Posts random lyric lines from BMTH songs every hour
- Tracks posted lyrics to avoid immediate repeats
- Automatically resets when all lyrics have been posted
- Simple configuration via environment variables

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Bluesky Credentials

1. Go to [Bluesky](https://bsky.app) and log in
2. Go to Settings → App Passwords
3. Create a new app password (this is your `BLUESKY_PASSWORD`)
4. Your handle is your Bluesky username (e.g., `yourname.bsky.social`)

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
BLUESKY_HANDLE=your-handle.bsky.social
BLUESKY_PASSWORD=your-app-password
```

**Important:** Never commit your `.env` file to version control. It's already in `.gitignore`.

### 4. Run the Bot

```bash
python bot.py
```

The bot will:
- Post an initial lyric immediately
- Then post a new lyric every hour
- Continue running until you stop it (Ctrl+C)

## How It Works

- The bot loads lyrics from `lyrics.json`
- It randomly selects a lyric line that hasn't been posted recently
- Posts it to Bluesky using the AT Protocol
- Tracks posted lyrics to ensure variety
- When all lyrics have been posted, it resets and starts over

## Running in the Background

### Windows (PowerShell)

```powershell
Start-Process python -ArgumentList "bot.py" -WindowStyle Hidden
```

### Linux/Mac

```bash
nohup python bot.py > bot.log 2>&1 &
```

Or use a process manager like `pm2` or `supervisor`.

## Customizing Lyrics

Edit `lyrics.json` to add or modify songs and lyrics. The format is:

```json
{
  "songs": [
    {
      "title": "Song Name",
      "lyrics": [
        "Line 1",
        "Line 2",
        "Line 3"
      ]
    }
  ]
}
```

## Troubleshooting

- **Authentication errors**: Make sure your handle and app password are correct in `.env`
- **No lyrics posted**: Check that `lyrics.json` exists and is valid JSON
- **Bot stops posting**: Check your internet connection and Bluesky service status

## License

This bot is for personal/educational use. Make sure you comply with Bluesky's Terms of Service and any applicable copyright laws regarding song lyrics.

