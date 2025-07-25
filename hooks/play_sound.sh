#!/bin/bash

# Universal audio player script for Claude Code hooks
# Usage: play_sound.sh <audio_file_path>

AUDIO_FILE="$1"

# Check if file path is provided
if [ -z "$AUDIO_FILE" ]; then
    exit 1
fi

# Check if file exists
if [ ! -f "$AUDIO_FILE" ]; then
    exit 1
fi

# Get file extension (convert to lowercase)
EXTENSION="${AUDIO_FILE##*.}"
EXTENSION=$(echo "$EXTENSION" | tr '[:upper:]' '[:lower:]')

# Play audio based on file extension
case "$EXTENSION" in
    ogg|oga|wav|flac|aiff|au)
        # Use paplay for formats supported by PulseAudio
        paplay "$AUDIO_FILE" 2>/dev/null &
        ;;
    mp3)
        # Try different MP3 players in order of preference
        if command -v mpg123 >/dev/null 2>&1; then
            mpg123 -q "$AUDIO_FILE" 2>/dev/null &
        elif command -v mplayer >/dev/null 2>&1; then
            mplayer -really-quiet "$AUDIO_FILE" 2>/dev/null &
        elif command -v mpv >/dev/null 2>&1; then
            mpv --no-terminal --volume=50 "$AUDIO_FILE" 2>/dev/null &
        fi
        ;;
    *)
        # Fallback: try paplay first, then other players
        if paplay "$AUDIO_FILE" 2>/dev/null; then
            :
        elif command -v mplayer >/dev/null 2>&1; then
            mplayer -really-quiet "$AUDIO_FILE" 2>/dev/null &
        elif command -v mpv >/dev/null 2>&1; then
            mpv --no-terminal --volume=50 "$AUDIO_FILE" 2>/dev/null &
        fi
        ;;
esac

exit 0