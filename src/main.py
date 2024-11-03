from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.her import Her
from src.message import Message
from src.model import ModelIdentifier
from src.utils import copy_code_to_clipboard

app = FastAPI()


class UserRequest(BaseModel):
    model_alias: str
    user_prompt: str


@app.get("/")
async def home():

    return "Welcome to the FastAPI app!"


def error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    return wrapper


@error_handler
@app.post("/chat")
async def process_request(request: UserRequest) -> dict[str, str]:
    model_id = ModelIdentifier(model_alias=request.model_alias)
    her = Her()
    model_message: Message = her.invoke(
        model_id=model_id, user_prompt=request.user_prompt
    )
    copy_code_to_clipboard(model_message.content)

    return model_message.__dict__


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
