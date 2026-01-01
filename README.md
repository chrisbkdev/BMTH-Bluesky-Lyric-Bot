# Bring Me the Horizon Lyric Bot for Bluesky

A Python bot that posts lyric lines from Bring Me the Horizon songs to Bluesky once every hour.

## Features

- Posts random lyric lines from BMTH songs every hour
- Tracks posted lyrics to avoid immediate repeats
- Automatically resets when all lyrics have been posted
- Simple configuration via environment variables



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

## License

This bot is for personal/educational use. Make sure you comply with Bluesky's Terms of Service and any applicable copyright laws regarding song lyrics.


