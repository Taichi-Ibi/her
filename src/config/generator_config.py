from src.utils import load_yaml_file, rename_key

class GeneratorConfig:
    def __init__(self) -> None:
        config_path = "src/config/generator_config.yaml"
        self._generator_config: dict[str, int | float] = load_yaml_file(config_path)

    @property
    def anthropic_config(self) -> dict[str, int | float]:
        return {**self._generator_config}

    @property
    def google_config(self) -> dict[str, int | float]:
        return rename_key(
            self._generator_config, old_key="max_tokens", new_key="max_output_tokens"
        )

    @property
    def groq_config(self) -> dict[str, int | float]:
        return {**self._generator_config}