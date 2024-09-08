from dataclasses import dataclass
from pathlib import Path


@dataclass
class Prompt:
    prompt_dir = Path("src/prompt")
    system_prompt = (prompt_dir / "system_prompt.txt").read_text().strip()
