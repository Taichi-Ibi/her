from abc import ABC, abstractmethod

import anthropic
import google.generativeai as genai
import google.ai.generativelanguage as glm
import groq

from src.message import Message, Messages
from src.utils import load_yaml_file, rename_key


class GeneratorConfig:
    def __init__(self) -> None:
        config_path = "src/config/generator_config.yaml"
        self._generator_config: dict[str, int | float] = load_yaml_file(config_path)

    def to_anthropic(self) -> dict[str, int | float]:
        return {**self._generator_config}

    def to_google(self) -> dict[str, int | float]:
        return rename_key(
            self._generator_config, old_key="max_tokens", new_key="max_output_tokens"
        )

    def to_groq(self) -> dict[str, int | float]:
        return {**self._generator_config}


class BaseModel(ABC):

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.generator_config = GeneratorConfig()

    @abstractmethod
    def invoke(self):
        pass


class AnthropicModel(BaseModel):

    @property
    def client(self) -> anthropic.Anthropic:
        return anthropic.Anthropic()

    def invoke(self, messages: Messages) -> Message:
        chat_completion = self.client.messages.create(
            model=self.model_name,
            system=messages.system_prompt,
            messages=messages.to_list()[1:],
            **self.generator_config,
        )
        model_content = chat_completion.content[0].text.strip()
        return Message(role="assistant", content=model_content)


class GoogleModel(BaseModel):

    @property
    def client(self) -> genai.GenerativeModel:
        return genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generator_config.to_google(),
        )

    def invoke(self, messages: Messages) -> Message:
        glm_messages: list[glm.Content] = messages.to_glm()
        chat = self.client.start_chat(history=glm_messages[:-1])
        model_content = chat.send_message(content=glm_messages[-1])
        return Message(role="assistant", content=model_content.text.strip())


class GroqModel(BaseModel):
    @property
    def client(self) -> groq.Groq:
        return groq.Groq()

    def invoke(self, messages: Messages) -> Message:
        chat_completion = self.client.chat.completions.create(
            messages=messages.to_list(),
            model=self.model_name,
            **self.generator_config.to_groq(),
        )
        model_content = chat_completion.choices[0].message.content.strip()
        return Message(role="assistant", content=model_content)


class ModelIdentifier:
    model_alias_dict = load_yaml_file("src/config/model/model_alias.yaml")

    def __init__(self, model_alias: str) -> None:
        _model_id = self.model_alias_dict[model_alias]
        self.model_provider, self.model_name = _model_id.split("/")


class ModelSelector:
    def __init__(self, model_id: ModelIdentifier) -> None:
        self.model_provider = model_id.model_provider
        self.model_name = model_id.model_name
        match self.model_provider:
            case "anthropic":
                self.model = AnthropicModel(model_name=self.model_name)
            case "google":
                self.model = GoogleModel(model_name=self.model_name)
            case "groq":
                self.model = GroqModel(model_name=self.model_name)
            case _:
                raise ValueError(f"Invalid model provider: {self.model_provider}")
