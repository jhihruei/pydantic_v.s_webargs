from flask import Blueprint, jsonify, request
from pydantic import BaseModel, ValidationError

pydantic_blueprint = Blueprint("pydantic_blueprint", __name__, url_prefix="/p")


class UserModel(BaseModel):
    name: str
    age: int


# Example: `curl "http://127.0.0.1:5000/p/query-string?name=Ray&age=18"`
@pydantic_blueprint.route("/query-string", methods=["GET"])
def hello_world():
    try:
        # 驗證 JSON 資料
        user = UserModel(**request.args)
        return jsonify({"message": f"Hello {user.name}, you are {user.age} years old!"})
    except ValidationError as e:
        return jsonify(e.errors()), 400
