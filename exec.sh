#!/bin/bash

BYELLOW=$'\e[1;33m'
NC=$'\e[0m'
RED=$'\e[0;31m'

# Set the terminal title
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS Terminal
  echo -ne "\033]0;$1\007"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
  # Linux (xterm-compatible)
  echo -ne "\033]0;$1\007"
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
  # Windows (Git Bash or similar)
  echo -ne "\e]0;$1\a"
fi

echo "Running command: ${BYELLOW}$1${NC}"
printf "\n"
eval "$1"
read -n 1 -s -r -p $"Press ${RED}Enter (⏎)${NC} to continue..."
printf "\033c"
exit 0