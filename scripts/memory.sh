#!/bin/bash

# プロジェクトのルートディレクトリに移動
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." >/dev/null 2>&1 && pwd)"
cd "$PROJECT_ROOT"

# history.jsonlを表示
echo "\033[36mSystem prompt:\033[0m"
head -n 1 logs/history.jsonl

# 各ターンを表示
for i in {1..3}; do
    start=$((2*i))
    if [ $(wc -l < logs/history.jsonl) -ge $((start+1)) ]; then
        echo "\n\033[36mTurn $i:\033[0m"
        tail -n +$start logs/history.jsonl | head -n 2
    fi
done