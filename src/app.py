from flask import Flask, request  # , jsonify

from src.her import Her
from src.message import Message
from src.model import ModelIdentifier

app = Flask(__name__)
app.json.ensure_ascii = False


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        model_id = ModelIdentifier(model_alias=request.json["model_alias"])
        user_prompt: str = request.json["user_prompt"]
        her = Her()
        model_message: Message = her.invoke(
            model_id=model_id, user_prompt=user_prompt
        )
        return model_message.content, 200
    return "Welcome to the Flask app!"


if __name__ == "__main__":
    app.run(debug=True)
