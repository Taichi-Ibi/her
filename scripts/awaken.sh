#!/bin/bash

set -e

# プロジェクトのルートディレクトリに移動
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." >/dev/null 2>&1 && pwd)"
cd "$PROJECT_ROOT"

# 仮想環境をアクティベート
source .venv/bin/activate

# 環境変数の設定（必要に応じて）
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# FastAPIアプリケーションを起動
exec uvicorn src.main:app --reload --host 0.0.0.0 --port 6666