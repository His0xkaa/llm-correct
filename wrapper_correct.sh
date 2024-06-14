#!/usr/bin/env bash

# run the project
poetry run python -m llmcorrect

# dunst notification for the wrapper script
notify-send "Wrapper script for LLM correct has finished running"
