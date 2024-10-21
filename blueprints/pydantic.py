from flask import Blueprint, jsonify, request
from pydantic import BaseModel, ValidationError, validator

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


class Account(BaseModel):
    username: str
    password: str

    @validator("password", always=True)
    @classmethod
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValidationError("too short")
        return password


# Example: `curl "http://127.0.0.1:5000/p/query-string/password?username=account&password=pa55w0rd"`
@pydantic_blueprint.route("/query-string/password", methods=["GET"])
def password():
    try:
        # 驗證 JSON 資料
        user = Account(**request.args)
        return jsonify(
            {"message": f"Hello {user.username}, your password is {user.password}"}
        )
    except ValidationError as e:
        return jsonify(e.errors()), 400
