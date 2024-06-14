# shebang line
#!/bin/bash -l
cd /home/user1/llm-correct/
poetry run python ollama_correct.py

# dunst notification for the wrapper script
notify-send "Wrapper script for LLM correct has finished running"
