#!/bin/bash

# Hook script to play notification sound when Claude needs user input
# This script is triggered by the "Notification" hook event

# SOUND_FILE="/home/yoda/.claude/sounds/buzzer-or-wrong-answer-20582.mp3"
SOUND_FILE='/home/yoda/.claude/sounds/complete.ogg'
# Use universal audio player script
/home/yoda/.claude/hooks/play_sound.sh "$SOUND_FILE"

# Exit successfully to allow Claude to continue
exit 0