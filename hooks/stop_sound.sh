#!/bin/bash

# Hook script to play completion sound when Claude finishes working
# This script is triggered by the "Stop" hook event

SOUND_FILE="/home/yoda/.claude/sounds/gospel-choir-heavenly-transition-3-186880.mp3"

# Use universal audio player script
/home/yoda/.claude/hooks/play_sound.sh "$SOUND_FILE"

# Exit successfully to allow Claude to continue
exit 0