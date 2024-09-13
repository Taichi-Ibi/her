from pathlib import Path

class Prompt:
    prompt_dir = Path("src/prompt/system_prompt")
    def __init__(self) -> None:
        pass

    @property
    def system_prompt(self):
        return (self.prompt_dir / "system_prompt.txt").read_text().strip()

    @property
    def judge_prompt(self):
        return (self.prompt_dir / "judge_prompt.txt").read_text().strip()