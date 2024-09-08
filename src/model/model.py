from abc import ABC, abstractmethod
from typing import List, Tuple

import google.generativeai as genai
import google.ai.generativelanguage as glm
import groq

from src.message import Message, Messages
from src.utils import load_yaml_file


generator_config = load_yaml_file("src/config/generator_config.yaml")


class ModelIdentifier:
    model_alias_dict = load_yaml_file("src/config/model/model_alias.yaml")

    def __init__(self, model_alias: str) -> None:
        _model_id = self.model_alias_dict[model_alias]
        self.model_provider, self.model_name = _model_id.split("/")


class BaseModel(ABC):

    @abstractmethod
    def invoke(self):
        pass


class AnthropicModel(BaseModel):
    def __init__(self, model_name: str) -> None:
        pass

    def invoke(self, messages: Messages) -> Message:
        pass


class GoogleModel(BaseModel):
    def __init__(self, model_name: str) -> None:
        self.client = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generator_config,
        )

    @staticmethod
    def messages_to_history(
        messages: Messages,
    ) -> Tuple[List[glm.Content], glm.Content]:
        """GPT形式 -> Gemini形式"""
        _messages = messages.to_list()
        system_message, chat_messages = _messages[0], _messages[1:]
        system_history = [
            # system prompt
            glm.Content(
                role="user",
                parts=[glm.Part(text=system_message["content"])],
            ),
            # dummy model response
            glm.Content(
                role="model",
                parts=[glm.Part(text="こんにちは！どのようにお手伝いしましょうか？")],
            ),
        ]
        chat_history = [
            glm.Content(
                role="model" if m["role"] == "assistant" else "user",
                parts=[glm.Part(text=m["content"])],
            )
            for m in chat_messages
        ]
        history = system_history + chat_history
        history, user_content = history[:-1], history[-1]
        return history, user_content

    def invoke(self, messages: Messages) -> Message:
        history, user_content = self.messages_to_history(messages=messages)
        chat = self.client.start_chat(history=history)
        chat.send_message(content=user_content)
        return Message(role="assistant", content=chat.last.text)


class GroqModel(BaseModel):
    def __init__(self, model_name: str) -> None:
        self.client = groq.Groq()
        self.model_name = model_name
        self.generator_config = generator_config

    def invoke(self, messages: Messages) -> Message:
        chat_completion = self.client.chat.completions.create(
            messages=messages.to_list(),
            model=self.model_name,
            **generator_config,
        )
        model_response = chat_completion.choices[0].message.content.strip()
        return Message(role="assistant", content=model_response)


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
