# shebang line
#!/bin/bash -l
cd ~/llm-correct/src/
poetry run python ollama_correct.py

# dunst notification for the wrapper script
notify-send "Wrapper script for LLM correct has finished running"
