from typing import Literal, TypedDict, Iterator
from dataclasses import dataclass, asdict

VALID_ROLES = Literal["system", "user", "assistant"]

class MessageDict(TypedDict):
    role: VALID_ROLES
    content: str

@dataclass
class Message:
    role: VALID_ROLES
    content: str

    def __post_init__(self):
        if self.role not in ("system", "user", "assistant"):
            raise ValueError(f"Invalid role: {self.role}")

    @property
    def as_dict(self) -> MessageDict:
        return asdict(self)

class Messages:
    def __init__(self, messages: list[Message]) -> None:
        self._messages: list[Message] = messages

    def __iter__(self) -> Iterator[Message]:
        return iter(self._messages)

    def to_list(self) -> list[MessageDict]:
        return [message.as_dict for message in self]

    def add(self, message: Message) -> None:
        self._messages.append(message)