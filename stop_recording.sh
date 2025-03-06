#!/bin/bash

# Adjust this based on how the recording starts.
# Example: If ffmpeg is used, kill all instances.
pkill -f "ffmpeg" || echo "Failed to stop recording"

exit 0
