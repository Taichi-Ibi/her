from typing import Iterator, Literal, TypedDict
from dataclasses import dataclass, asdict

import google.ai.generativelanguage as glm

VALID_ROLES = Literal["system", "user", "assistant"]


class MessageDict(TypedDict):
    role: VALID_ROLES
    content: str


@dataclass
class Message:
    role: VALID_ROLES
    content: str

    def __post_init__(self):
        if self.role not in {"system", "user", "assistant"}:
            raise ValueError(f"Invalid role: {self.role}")

    @property
    def as_dict(self) -> MessageDict:
        return asdict(self)


class Messages:
    def __init__(self, messages: list[Message]) -> None:
        self._messages: list[Message] = messages

    def __iter__(self) -> Iterator[Message]:
        return iter(self._messages)

    def __len__(self) -> int:
        return len(self._messages)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Messages(self._messages[key])
        return self._messages[key]

    def __add__(self, other: 'Messages') -> 'Messages':
        return Messages(self._messages + other._messages)

    def __iadd__(self, other: 'Messages') -> 'Messages':
        self._messages.extend(other._messages)
        return self

    def to_list(self) -> list[MessageDict]:
        return [message.as_dict for message in self]

    def append(self, message: Message) -> None:
        self._messages.append(message)

    def extend(self, messages: list[Message]) -> None:
        self._messages.extend(messages)

    def to_context(self, title: str) -> str:
        return f"```{title}\n{str(self.to_list())}```"

    @property
    def system_prompt(self) -> str:
        return self._messages[0].content

    def to_glm(self) -> list[glm.Content]:
        """GPT形式 -> Gemini形式"""
        system_message, *chat_messages = self._messages
        glm_messages = []
        glm_messages.extend(
            [
                # system prompt
                glm.Content(
                    role="user",
                    parts=[glm.Part(text=system_message.content)],
                ),
                # dummy model response
                glm.Content(
                    role="model",
                    parts=[
                        glm.Part(text="こんにちは！どのようにお手伝いしましょうか？")
                    ],
                ),
            ]
        )
        glm_messages.extend(
            [
                glm.Content(
                    role="model" if m.role == "assistant" else "user",
                    parts=[glm.Part(text=m.content)],
                )
                for m in chat_messages
            ]
        )
        return glm_messages
