import logging
import re

from src.memory import Memory
from src.message import Message, Messages
from src.model import ModelSelector, ModelIdentifier
from src.prompt import Prompt
from src.utils import load_jsonl_file

logging.basicConfig(level=logging.INFO)


class Her:
    def __init__(self) -> None:
        self.history_path = "logs/history.jsonl"
        self.chat_messages = Messages(messages=[])
        self.judge_messages = Messages(messages=[])
        self.prompt = Prompt()
        self.memory = Memory()

    def _prep_messages(self, user_prompt: str) -> Messages:
        self.memory.load()
        self.history = self.memory.history
        judge_model = ModelSelector(model_id=ModelIdentifier("flm")).model
        self.judge_messages.extend(
            messages=Messages(
                messages=[
                    Message(role="system", content=self.prompt.judge_prompt),
                    Message(
                        role="user",
                        content="\n\n".join(
                            [
                                self.history[1:].to_context(title="Message1"),
                                Messages(
                                    messages=[Message(role="user", content=user_prompt)]
                                ).to_context(title="Message2"),
                            ]
                        ),
                    ),
                ]
            )
        )
        judge_message = judge_model.invoke(messages=self.judge_messages)
        logging.info(judge_message.__dict__)
        if bool(re.search(r"\bTrue\b", judge_message.content)):
            print("Continue conversation")
            self.history.append(Message(role="user", content=user_prompt))
            return self.history
        else:
            print("Start new conversation")
            return Messages(
                messages=[
                    Message(role="system", content=self.prompt.system_prompt),
                    Message(role="user", content=user_prompt),
                ]
            )

    def invoke(self, model_id: ModelIdentifier, user_prompt: str) -> Message:
        messages = self._prep_messages(user_prompt=user_prompt)
        chat_model = ModelSelector(model_id=model_id).model
        model_response = chat_model.invoke(messages=messages)
        messages.append(model_response)
        for message in messages:
            logging.info(message.__dict__)
        self.memory.save(messages=messages)
        return model_response
